/// Modelos de dados e configurações do Combat Bot Controller
enum ConnectionType {
  webSocket,
  http,
  bluetoothSerial,
  simulation,
}

enum ControlMode {
  joystick360,
  dpad,
}

class BotConfig {
  String robotIp;
  int wsPort;
  int httpPort;
  int turn90TimeMs;
  int speedPercent; // 50 a 100%
  int maxPwm; // 255 (ESP32) ou 1023 (micro:bit)
  double deadzone; // 0.05 a 0.20
  int updateIntervalMs; // 25ms padrão (40 FPS)

  BotConfig({
    this.robotIp = '192.168.4.1',
    this.wsPort = 80,
    this.httpPort = 80,
    this.turn90TimeMs = 260,
    this.speedPercent = 100,
    this.maxPwm = 255,
    this.deadzone = 0.08,
    this.updateIntervalMs = 25,
  });

  int get effectiveMaxSpeed => (maxPwm * (speedPercent / 100)).round();
}

class TelemetryState {
  final int leftPwm;
  final int rightPwm;
  final int pingMs;
  final bool isConnected;
  final bool isTurboActive;
  final bool isArmed;
  final String statusMessage;
  final DateTime lastPacketTime;

  const TelemetryState({
    this.leftPwm = 0,
    this.rightPwm = 0,
    this.pingMs = 0,
    this.isConnected = false,
    this.isTurboActive = false,
    this.isArmed = false,
    this.statusMessage = 'Desconectado',
    required this.lastPacketTime,
  });

  TelemetryState copyWith({
    int? leftPwm,
    int? rightPwm,
    int? pingMs,
    bool? isConnected,
    bool? isTurboActive,
    bool? isArmed,
    String? statusMessage,
    DateTime? lastPacketTime,
  }) {
    return TelemetryState(
      leftPwm: leftPwm ?? this.leftPwm,
      rightPwm: rightPwm ?? this.rightPwm,
      pingMs: pingMs ?? this.pingMs,
      isConnected: isConnected ?? this.isConnected,
      isTurboActive: isTurboActive ?? this.isTurboActive,
      isArmed: isArmed ?? this.isArmed,
      statusMessage: statusMessage ?? this.statusMessage,
      lastPacketTime: lastPacketTime ?? this.lastPacketTime,
    );
  }
}
