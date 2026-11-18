import 'dart:convert';
import 'package:flutter/material.dart';

/// Temas visuais selecionáveis pelo usuário
enum AppColorTheme {
  obsidianBlue('Obsidian Blue (Aeroespacial)', Color(0xFF3B82F6), Color(0xFF06B6D4)),
  cyberEmerald('Cyber Emerald (F1 Tático)', Color(0xFF10B981), Color(0xFF22C55E)),
  crimsonFury('Crimson Fury (Combate Alerta)', Color(0xFFEF4444), Color(0xFFF97316)),
  amberStealth('Amber Stealth (Noturno McLaren)', Color(0xFFF59E0B), Color(0xFFEAB308)),
  titaniumMinimal('Titanium Minimal (Monocromático)', Color(0xFFF8FAFC), Color(0xFF94A3B8));

  final String label;
  final Color primaryColor;
  final Color accentColor;
  const AppColorTheme(this.label, this.primaryColor, this.accentColor);
}

/// Orientação dos controles (Destro ou Canhoto)
enum Handedness {
  rightHanded('Destro (Analógico à Esquerda)'),
  leftHanded('Canhoto (Analógico à Direita)');

  final String label;
  const Handedness(this.label);
}

/// Curva de aceleração do analógico
enum StickCurve {
  linear('Linear 1:1 (Direto)'),
  expoSmooth('Exponencial Suave (Precisão no Centro)'),
  aggressive('Agressivo (Torque Rápido)');

  final String label;
  const StickCurve(this.label);
}

/// Ações que podem ser atribuídas aos botões táticos personalizáveis
enum TacticalActionType {
  turn90Left('Giro 90° Esquerda', 'L90', Icons.turn_left_rounded),
  turn90Right('Giro 90° Direita', 'R90', Icons.turn_right_rounded),
  turn180('Meia-Volta 180°', 'R180', Icons.sync_rounded),
  pivotLeft('Pivô Roda Esquerda', 'L_PIVOT', Icons.rotate_left_rounded),
  pivotRight('Pivô Roda Direita', 'R_PIVOT', Icons.rotate_right_rounded),
  toggleWeapon('Alternar Arma / Atuador', 'WEAPON', Icons.shield_rounded),
  hornBuzzer('Buzzer / Sinal Sonoro', 'BUZZ', Icons.volume_up_rounded),
  customCommand('Comando Customizado', 'CUSTOM', Icons.code_rounded);

  final String defaultTitle;
  final String defaultCmd;
  final IconData defaultIcon;
  const TacticalActionType(this.defaultTitle, this.defaultCmd, this.defaultIcon);
}

/// Configuração individual de um botão tático
class TacticalButtonConfig {
  TacticalActionType actionType;
  String customTitle;
  String customCmd;
  int durationMs;

  TacticalButtonConfig({
    required this.actionType,
    String? customTitle,
    String? customCmd,
    this.durationMs = 260,
  })  : customTitle = customTitle ?? actionType.defaultTitle,
        customCmd = customCmd ?? actionType.defaultCmd;

  Map<String, dynamic> toJson() => {
        'actionType': actionType.index,
        'customTitle': customTitle,
        'customCmd': customCmd,
        'durationMs': durationMs,
      };

  factory TacticalButtonConfig.fromJson(Map<String, dynamic> json) {
    final typeIdx = json['actionType'] as int? ?? 0;
    final actionType = TacticalActionType.values[typeIdx.clamp(0, TacticalActionType.values.length - 1)];
    return TacticalButtonConfig(
      actionType: actionType,
      customTitle: json['customTitle'] as String?,
      customCmd: json['customCmd'] as String?,
      durationMs: json['durationMs'] as int? ?? 260,
    );
  }
}

/// Tipos de conexão
enum ConnectionType {
  webSocket,
  http,
  simulation,
}

enum ControlMode {
  joystick360,
  dpad,
}

enum ArenaProfile {
  smoothFloor('Piso Liso (Madeira/MDF)', 220),
  standard('Arena Oficial (Aço)', 260),
  highTraction('Alto Atrito (Borracha)', 330),
  custom('Personalizado', 260);

  final String label;
  final int defaultTurn90Ms;
  const ArenaProfile(this.label, this.defaultTurn90Ms);
}

/// Classe Central de Configurações Totalmente Personalizáveis
class BotConfig {
  // 1. Rede e Comunicação
  String robotIp;
  int wsPort;
  int httpPort;
  int updateIntervalMs; // 10ms a 50ms (padrão: 25ms = 40 FPS)

  // 2. Personalização Visual
  AppColorTheme colorTheme;

  // 3. Ergonomia e Controles
  Handedness handedness;
  bool invertThrottleY; // Inverte Frente / Ré
  bool invertSteeringX; // Inverte Esquerda / Direita
  StickCurve stickCurve;
  double joystickRadius; // 85 a 130px
  double deadzone; // 0.02 a 0.25 (2% a 25%)

  // 4. Afinação de Motores & Trim
  int steeringTrim; // -25% a +25% para compensar puxada lateral
  int speedPercent; // 30% a 100% de teto normal
  int turboSpeedPercent; // 80% a 100% de teto no turbo
  int maxPwm; // 255 (ESP32) ou 1023 (micro:bit)
  bool smoothAcceleration; // Rampa suave de aceleração

  // 5. Arena & Manobras
  int turn90TimeMs;
  ArenaProfile arenaProfile;

  // 6. Botões Táticos Personalizados (Slots 1, 2, 3 e 4)
  List<TacticalButtonConfig> tacticalButtons;

  BotConfig({
    this.robotIp = '192.168.4.1',
    this.wsPort = 80,
    this.httpPort = 80,
    this.updateIntervalMs = 25,
    this.colorTheme = AppColorTheme.obsidianBlue,
    this.handedness = Handedness.rightHanded,
    this.invertThrottleY = false,
    this.invertSteeringX = false,
    this.stickCurve = StickCurve.expoSmooth,
    this.joystickRadius = 110.0,
    this.deadzone = 0.06,
    this.steeringTrim = 0,
    this.speedPercent = 100,
    this.turboSpeedPercent = 100,
    this.maxPwm = 255,
    this.smoothAcceleration = false,
    this.turn90TimeMs = 260,
    this.arenaProfile = ArenaProfile.standard,
    List<TacticalButtonConfig>? tacticalButtons,
  }) : tacticalButtons = tacticalButtons ??
            [
              TacticalButtonConfig(
                actionType: TacticalActionType.turn90Left,
                customTitle: 'GIRO 90°',
                durationMs: 260,
              ),
              TacticalButtonConfig(
                actionType: TacticalActionType.turn180,
                customTitle: 'MEIA-VOLTA 180°',
                durationMs: 520,
              ),
              TacticalButtonConfig(
                actionType: TacticalActionType.pivotLeft,
                customTitle: 'PIVÔ ESQ',
              ),
              TacticalButtonConfig(
                actionType: TacticalActionType.pivotRight,
                customTitle: 'PIVÔ DIR',
              ),
            ];

  int get effectiveMaxSpeed => (maxPwm * (speedPercent / 100)).round();
  int get effectiveTurboSpeed => (maxPwm * (turboSpeedPercent / 100)).round();

  Map<String, dynamic> toJson() => {
        'robotIp': robotIp,
        'wsPort': wsPort,
        'httpPort': httpPort,
        'updateIntervalMs': updateIntervalMs,
        'colorTheme': colorTheme.index,
        'handedness': handedness.index,
        'invertThrottleY': invertThrottleY,
        'invertSteeringX': invertSteeringX,
        'stickCurve': stickCurve.index,
        'joystickRadius': joystickRadius,
        'deadzone': deadzone,
        'steeringTrim': steeringTrim,
        'speedPercent': speedPercent,
        'turboSpeedPercent': turboSpeedPercent,
        'maxPwm': maxPwm,
        'smoothAcceleration': smoothAcceleration,
        'turn90TimeMs': turn90TimeMs,
        'arenaProfile': arenaProfile.index,
        'tacticalButtons': tacticalButtons.map((b) => b.toJson()).toList(),
      };

  factory BotConfig.fromJson(Map<String, dynamic> json) {
    final cfg = BotConfig();
    if (json.containsKey('robotIp')) cfg.robotIp = json['robotIp'] as String;
    if (json.containsKey('wsPort')) cfg.wsPort = json['wsPort'] as int;
    if (json.containsKey('httpPort')) cfg.httpPort = json['httpPort'] as int;
    if (json.containsKey('updateIntervalMs')) cfg.updateIntervalMs = json['updateIntervalMs'] as int;

    if (json.containsKey('colorTheme')) {
      final idx = json['colorTheme'] as int;
      cfg.colorTheme = AppColorTheme.values[idx.clamp(0, AppColorTheme.values.length - 1)];
    }
    if (json.containsKey('handedness')) {
      final idx = json['handedness'] as int;
      cfg.handedness = Handedness.values[idx.clamp(0, Handedness.values.length - 1)];
    }
    if (json.containsKey('invertThrottleY')) cfg.invertThrottleY = json['invertThrottleY'] as bool;
    if (json.containsKey('invertSteeringX')) cfg.invertSteeringX = json['invertSteeringX'] as bool;
    if (json.containsKey('stickCurve')) {
      final idx = json['stickCurve'] as int;
      cfg.stickCurve = StickCurve.values[idx.clamp(0, StickCurve.values.length - 1)];
    }
    if (json.containsKey('joystickRadius')) cfg.joystickRadius = (json['joystickRadius'] as num).toDouble();
    if (json.containsKey('deadzone')) cfg.deadzone = (json['deadzone'] as num).toDouble();
    if (json.containsKey('steeringTrim')) cfg.steeringTrim = json['steeringTrim'] as int;
    if (json.containsKey('speedPercent')) cfg.speedPercent = json['speedPercent'] as int;
    if (json.containsKey('turboSpeedPercent')) cfg.turboSpeedPercent = json['turboSpeedPercent'] as int;
    if (json.containsKey('maxPwm')) cfg.maxPwm = json['maxPwm'] as int;
    if (json.containsKey('smoothAcceleration')) cfg.smoothAcceleration = json['smoothAcceleration'] as bool;
    if (json.containsKey('turn90TimeMs')) cfg.turn90TimeMs = json['turn90TimeMs'] as int;
    if (json.containsKey('arenaProfile')) {
      final idx = json['arenaProfile'] as int;
      cfg.arenaProfile = ArenaProfile.values[idx.clamp(0, ArenaProfile.values.length - 1)];
    }
    if (json.containsKey('tacticalButtons')) {
      final rawList = json['tacticalButtons'] as List<dynamic>;
      cfg.tacticalButtons = rawList.map((e) => TacticalButtonConfig.fromJson(e as Map<String, dynamic>)).toList();
    }
    return cfg;
  }

  String serialize() => jsonEncode(toJson());
  static BotConfig deserialize(String str) => BotConfig.fromJson(jsonDecode(str) as Map<String, dynamic>);
}

/// Estado de telemetria
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
}
