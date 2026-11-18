import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:web_socket_channel/web_socket_channel.dart';
import '../models/bot_models.dart';

class BotCommunicationService extends ChangeNotifier {
  final BotConfig config;
  ConnectionType connectionType = ConnectionType.webSocket;

  WebSocketChannel? _wsChannel;
  StreamSubscription? _wsSubscription;
  Timer? _reconnectTimer;
  Timer? _heartbeatTimer;
  Timer? _pingTimer;

  DateTime? _pingSentTime;
  int _currentPingMs = 0;

  int _targetLeftPwm = 0;
  int _targetRightPwm = 0;
  int _lastSentLeftPwm = 0;
  int _lastSentRightPwm = 0;

  bool _isConnecting = false;
  bool _isConnected = false;
  bool _isTurboActive = false;
  bool _isArmed = false;
  String _statusMessage = 'Aguardando conexão...';

  // Getters
  bool get isConnected => _isConnected;
  bool get isConnecting => _isConnecting;
  bool get isTurboActive => _isTurboActive;
  bool get isArmed => _isArmed;
  int get pingMs => _currentPingMs;
  int get leftPwm => _targetLeftPwm;
  int get rightPwm => _targetRightPwm;
  String get statusMessage => _statusMessage;

  BotCommunicationService({required this.config}) {
    _startTransmissionLoop();
  }

  /// Inicia conexão com o robô
  Future<void> connect({ConnectionType? type}) async {
    if (type != null) connectionType = type;

    if (connectionType == ConnectionType.simulation) {
      _isConnected = true;
      _isConnecting = false;
      _statusMessage = 'Modo Simulação Ativo';
      _currentPingMs = 1;
      notifyListeners();
      return;
    }

    if (connectionType == ConnectionType.webSocket) {
      await _connectWebSocket();
    } else if (connectionType == ConnectionType.http) {
      await _testHttpConnection();
    }
  }

  /// Conecta via WebSockets persistente
  Future<void> _connectWebSocket() async {
    _isConnecting = true;
    _statusMessage = 'Conectando WebSocket em ws://${config.robotIp}:${config.wsPort}/ws...';
    notifyListeners();

    _cleanupWebSocket();

    try {
      final wsUrl = Uri.parse('ws://${config.robotIp}:${config.wsPort}/ws');
      _wsChannel = WebSocketChannel.connect(wsUrl);

      await _wsChannel!.ready;
      _isConnected = true;
      _isConnecting = false;
      _statusMessage = '🟢 Conectado via WebSocket (<5ms)';
      notifyListeners();

      _wsSubscription = _wsChannel!.stream.listen(
        (message) => _handleIncomingMessage(message.toString()),
        onDone: () => _handleDisconnection('WebSocket desconectado'),
        onError: (err) => _handleDisconnection('Erro de conexão WebSocket: $err'),
      );

      _startPingMonitoring();
    } catch (e) {
      _handleDisconnection('Falha ao conectar: $e');
    }
  }

  void _handleIncomingMessage(String msg) {
    if (msg.startsWith('T:')) {
      // Telemetria do ESP32: "T:<left>,<right>"
      final parts = msg.substring(2).split(',');
      if (parts.length == 2) {
        // Confirmação recebida
      }
    } else if (msg == 'PONG' || msg == 'P') {
      if (_pingSentTime != null) {
        _currentPingMs = DateTime.now().difference(_pingSentTime!).inMilliseconds;
        notifyListeners();
      }
    }
  }

  void _handleDisconnection(String reason) {
    _isConnected = false;
    _isConnecting = false;
    _statusMessage = '🔴 $reason';
    _currentPingMs = 0;
    notifyListeners();

    _reconnectTimer?.cancel();
    if (connectionType == ConnectionType.webSocket) {
      _reconnectTimer = Timer(const Duration(seconds: 2), () {
        if (!_isConnected) connect();
      });
    }
  }

  void _cleanupWebSocket() {
    _wsSubscription?.cancel();
    _wsSubscription = null;
    _wsChannel?.sink.close();
    _wsChannel = null;
    _pingTimer?.cancel();
  }

  /// Teste de conexão HTTP (Modo HTTP / ESP32 V1)
  Future<void> _testHttpConnection() async {
    _isConnecting = true;
    _statusMessage = 'Verificando HTTP http://${config.robotIp}:${config.httpPort}/drive...';
    notifyListeners();

    try {
      final url = Uri.parse('http://${config.robotIp}:${config.httpPort}/drive?l=0&r=0');
      final res = await http.get(url).timeout(const Duration(seconds: 2));
      if (res.statusCode == 200) {
        _isConnected = true;
        _isConnecting = false;
        _statusMessage = '🟢 Conectado via HTTP';
      } else {
        throw Exception('Status code: ${res.statusCode}');
      }
    } catch (e) {
      _isConnected = false;
      _isConnecting = false;
      _statusMessage = '🔴 Erro HTTP: $e';
    }
    notifyListeners();
  }

  /// Monitoramento periódico de Latência / Ping
  void _startPingMonitoring() {
    _pingTimer?.cancel();
    _pingTimer = Timer.periodic(const Duration(milliseconds: 1000), (timer) {
      if (_isConnected && _wsChannel != null) {
        _pingSentTime = DateTime.now();
        _wsChannel!.sink.add('P');
      }
    });
  }

  /// Loop de Transmissão contínua com taxa estável (ex: 25ms = 40 FPS)
  void _startTransmissionLoop() {
    _heartbeatTimer?.cancel();
    _heartbeatTimer = Timer.periodic(Duration(milliseconds: config.updateIntervalMs), (timer) {
      if (!_isConnected && connectionType != ConnectionType.simulation) return;

      // Envia comando contínuo
      if (_targetLeftPwm != _lastSentLeftPwm || _targetRightPwm != _lastSentRightPwm) {
        _sendDrivePacket(_targetLeftPwm, _targetRightPwm);
      } else if (_targetLeftPwm == 0 && _targetRightPwm == 0) {
        // Envia heartbeat em repouso
        if (timer.tick % 8 == 0) {
          _sendDrivePacket(0, 0);
        }
      }
    });
  }

  /// Aplica a curva de resposta ao eixo
  double _applyCurve(double val) {
    if (val == 0.0) return 0.0;
    switch (config.stickCurve) {
      case StickCurve.linear:
        return val;
      case StickCurve.expoSmooth:
        // Exponencial suave: 65% cúbico + 35% linear (precisão cirúrgica no centro)
        return (val * val.abs() * 0.65) + (val * 0.35);
      case StickCurve.aggressive:
        return (val.sign * (val.abs() * 0.5 + 0.5)).clamp(-1.0, 1.0);
    }
  }

  /// Atualiza o vetor de velocidade do joystick analógico com personalizações
  void updateJoystickVelocity(double normV, double normW) {
    // 1. Aplica inversão de eixos
    double v = config.invertThrottleY ? -normV : normV;
    double w = config.invertSteeringX ? -normW : normW;

    // 2. Zona Morta (Deadzone)
    if (v.abs() < config.deadzone && w.abs() < config.deadzone) {
      _targetLeftPwm = 0;
      _targetRightPwm = 0;
    } else {
      // 3. Aplica Curva do Analógico
      v = _applyCurve(v);
      w = _applyCurve(w);

      // 4. Algoritmo Arcade Drive Mixing
      double left = v + w;
      double right = v - w;

      // 5. Trim de Direção (Compensação mecânica)
      if (config.steeringTrim != 0 && (v != 0 || w != 0)) {
        final trimFactor = config.steeringTrim / 100.0;
        left *= (1.0 + trimFactor);
        right *= (1.0 - trimFactor);
      }

      final maxVal = left.abs() > right.abs() ? left.abs() : right.abs();
      if (maxVal > 1.0) {
        left /= maxVal;
        right /= maxVal;
      }

      final maxSpeed = _isTurboActive ? config.effectiveTurboSpeed : config.effectiveMaxSpeed;
      final targetL = (left * maxSpeed).round();
      final targetR = (right * maxSpeed).round();

      // 6. Rampa de Aceleração Suave (Opcional)
      if (config.smoothAcceleration) {
        const maxStep = 55;
        _targetLeftPwm += (targetL - _targetLeftPwm).clamp(-maxStep, maxStep);
        _targetRightPwm += (targetR - _targetRightPwm).clamp(-maxStep, maxStep);
      } else {
        _targetLeftPwm = targetL;
        _targetRightPwm = targetR;
      }

      _targetLeftPwm = _targetLeftPwm.clamp(-config.maxPwm, config.maxPwm);
      _targetRightPwm = _targetRightPwm.clamp(-config.maxPwm, config.maxPwm);
    }
    notifyListeners();
  }

  /// Envio do pacote de tração (WebSocket ou HTTP)
  void _sendDrivePacket(int left, int right) {
    _lastSentLeftPwm = left;
    _lastSentRightPwm = right;

    if (connectionType == ConnectionType.simulation) {
      return;
    }

    if (connectionType == ConnectionType.webSocket && _wsChannel != null) {
      // Formato compacto do ESP32 V2: "D:l,r" (ex: "D:255,-120")
      _wsChannel!.sink.add('D:$left,$right');
    } else if (connectionType == ConnectionType.http) {
      final url = Uri.parse('http://${config.robotIp}:${config.httpPort}/drive?l=$left&r=$right');
      http.get(url).catchError((_) => http.Response('', 500));
    }
  }

  /// Envia comando tático discreto
  void sendCommand(String dir, {int? speed, int? durationMs}) {
    final spd = speed ?? (_isTurboActive ? config.effectiveTurboSpeed : config.effectiveMaxSpeed);
    final dur = durationMs ?? 0;

    _statusMessage = 'Executando: $dir ($dur ms)';
    notifyListeners();

    if (connectionType == ConnectionType.simulation) return;

    if (connectionType == ConnectionType.webSocket && _wsChannel != null) {
      _wsChannel!.sink.add('C:$dir:$spd:$dur');
    } else if (connectionType == ConnectionType.http) {
      final url = Uri.parse('http://${config.robotIp}:${config.httpPort}/cmd?dir=$dir&speed=$spd&duration=$dur');
      http.get(url).catchError((_) => http.Response('', 500));
    }
  }

  /// Executa uma ação de botão tático personalizável
  void executeTacticalAction(TacticalButtonConfig btn) {
    switch (btn.actionType) {
      case TacticalActionType.turn90Left:
        sendCommand('L90', durationMs: btn.durationMs);
        break;
      case TacticalActionType.turn90Right:
        sendCommand('R90', durationMs: btn.durationMs);
        break;
      case TacticalActionType.turn180:
        sendCommand('R180', durationMs: btn.durationMs);
        break;
      case TacticalActionType.pivotLeft:
        sendCommand('L_PIVOT');
        break;
      case TacticalActionType.pivotRight:
        sendCommand('R_PIVOT');
        break;
      case TacticalActionType.toggleWeapon:
        toggleWeapon();
        break;
      case TacticalActionType.hornBuzzer:
        sendCommand('BUZZ', durationMs: 150);
        break;
      case TacticalActionType.customCommand:
        sendCommand(btn.customCmd, durationMs: btn.durationMs);
        break;
    }
  }

  /// Ativa/Desativa o modo Turbo (Overdrive)
  void setTurbo(bool active) {
    _isTurboActive = active;
    _statusMessage = active ? '⚡ TURBO ATIVO (Potência Máxima)!' : 'Controle Normal';
    notifyListeners();
  }

  /// Alterna estado da arma / atuador
  void toggleWeapon() {
    _isArmed = !_isArmed;
    sendCommand(_isArmed ? 'ARMA_ON' : 'ARMA_OFF');
    notifyListeners();
  }

  /// Parada imediata de emergência (Emergency Stop)
  void emergencyStop() {
    _targetLeftPwm = 0;
    _targetRightPwm = 0;
    _isTurboActive = false;
    _isArmed = false;
    _sendDrivePacket(0, 0);
    sendCommand('STOP');
    notifyListeners();
  }

  @override
  void dispose() {
    _cleanupWebSocket();
    _reconnectTimer?.cancel();
    _heartbeatTimer?.cancel();
    super.dispose();
  }
}
