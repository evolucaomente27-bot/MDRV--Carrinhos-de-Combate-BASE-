import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'models/bot_models.dart';
import 'services/bot_communication_service.dart';
import 'widgets/analog_joystick.dart';
import 'widgets/dpad_controller.dart';
import 'widgets/telemetry_gauges.dart';
import 'widgets/tactical_panel.dart';
import 'widgets/settings_dialog.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);
  runApp(const CombatBotApp());
}

class CombatBotApp extends StatelessWidget {
  const CombatBotApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Combat Bot Pro Controller',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF0A0B12),
        primaryColor: const Color(0xFF00E676),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF00E676),
          secondary: Color(0xFF0EA5E9),
          surface: Color(0xFF141724),
        ),
      ),
      home: const ControllerHomeScreen(),
    );
  }
}

class ControllerHomeScreen extends StatefulWidget {
  const ControllerHomeScreen({super.key});

  @override
  State<ControllerHomeScreen> createState() => _ControllerHomeScreenState();
}

class _ControllerHomeScreenState extends State<ControllerHomeScreen> {
  late final BotConfig _config;
  late final BotCommunicationService _botService;
  ControlMode _controlMode = ControlMode.joystick360;

  @override
  void initState() {
    super.initState();
    _config = BotConfig();
    _botService = BotCommunicationService(config: _config);

    WidgetsBinding.instance.addPostFrameCallback((_) {
      _botService.connect();
    });
  }

  @override
  void dispose() {
    _botService.dispose();
    super.dispose();
  }

  void _openSettings() {
    showDialog(
      context: context,
      builder: (context) => SettingsDialog(
        config: _config,
        service: _botService,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF0F121E),
        elevation: 0,
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: const Color(0x3300E676),
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Icon(Icons.smart_toy, color: Color(0xFF00E676), size: 20),
            ),
            const SizedBox(width: 10),
            const Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'COMBAT BOT PRO',
                  style: TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w900,
                    letterSpacing: 1.5,
                    color: Colors.white,
                  ),
                ),
                Text(
                  'FLUTTER LOW-LATENCY CONTROLLER',
                  style: TextStyle(
                    fontSize: 8.5,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1.0,
                    color: Color(0xFF94A3B8),
                  ),
                ),
              ],
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh, color: Color(0xFF38BDF8)),
            tooltip: 'Reconectar',
            onPressed: () => _botService.connect(),
          ),
          IconButton(
            icon: const Icon(Icons.settings, color: Color(0xFFE2E8F0)),
            tooltip: 'Configurações',
            onPressed: _openSettings,
          ),
        ],
      ),
      body: SafeArea(
        child: AnimatedBuilder(
          animation: _botService,
          builder: (context, _) {
            return SingleChildScrollView(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              child: Column(
                children: [
                  // 1. MEDIDORES DE TELEMETRIA
                  TelemetryGauges(
                    leftPwm: _botService.leftPwm,
                    rightPwm: _botService.rightPwm,
                    maxPwm: _config.maxPwm,
                    pingMs: _botService.pingMs,
                    isConnected: _botService.isConnected,
                    statusText: _botService.statusMessage,
                  ),

                  const SizedBox(height: 12),

                  // 2. SELETOR DE MODO (JOYSTICK vs D-PAD)
                  Container(
                    padding: const EdgeInsets.all(3),
                    decoration: BoxDecoration(
                      color: const Color(0xFF141724),
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(color: const Color(0xFF334155)),
                    ),
                    child: Row(
                      children: [
                        Expanded(
                          child: InkWell(
                            onTap: () {
                              HapticFeedback.selectionClick();
                              setState(() => _controlMode = ControlMode.joystick360);
                            },
                            borderRadius: BorderRadius.circular(8),
                            child: Container(
                              padding: const EdgeInsets.symmetric(vertical: 8),
                              decoration: BoxDecoration(
                                color: _controlMode == ControlMode.joystick360
                                    ? const Color(0xFF0EA5E9)
                                    : Colors.transparent,
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: Center(
                                child: Text(
                                  '🕹️ JOYSTICK 360°',
                                  style: TextStyle(
                                    fontSize: 11,
                                    fontWeight: FontWeight.w900,
                                    color: _controlMode == ControlMode.joystick360
                                        ? Colors.white
                                        : const Color(0xFF94A3B8),
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ),
                        Expanded(
                          child: InkWell(
                            onTap: () {
                              HapticFeedback.selectionClick();
                              setState(() => _controlMode = ControlMode.dpad);
                            },
                            borderRadius: BorderRadius.circular(8),
                            child: Container(
                              padding: const EdgeInsets.symmetric(vertical: 8),
                              decoration: BoxDecoration(
                                color: _controlMode == ControlMode.dpad
                                    ? const Color(0xFF0EA5E9)
                                    : Colors.transparent,
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: Center(
                                child: Text(
                                  '🎛️ D-PAD DE BOTÕES',
                                  style: TextStyle(
                                    fontSize: 11,
                                    fontWeight: FontWeight.w900,
                                    color: _controlMode == ControlMode.dpad
                                        ? Colors.white
                                        : const Color(0xFF94A3B8),
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),

                  const SizedBox(height: 14),

                  // 3. ÁREA DE DIREÇÃO (JOYSTICK OU D-PAD)
                  _controlMode == ControlMode.joystick360
                      ? AnalogJoystick(
                          radius: 115,
                          stickRadius: 42,
                          isTurbo: _botService.isTurboActive,
                          onChanged: (v, w) => _botService.updateJoystickVelocity(v, w),
                          onReleased: () => _botService.updateJoystickVelocity(0, 0),
                        )
                      : DpadController(
                          onDirectionDown: (dir) => _botService.sendCommand(dir),
                          onDirectionUp: () => _botService.sendCommand('S'),
                        ),

                  const SizedBox(height: 16),

                  // 4. PAINEL TÁTICO DE COMBATE
                  TacticalPanel(
                    isTurbo: _botService.isTurboActive,
                    isArmed: _botService.isArmed,
                    turn90TimeMs: _config.turn90TimeMs,
                    onTurboChanged: (active) => _botService.setTurbo(active),
                    onManeuverTriggered: (maneuver, dur) => _botService.sendCommand(maneuver, durationMs: dur),
                    onWheelPivotDown: (cmd) => _botService.sendCommand(cmd),
                    onWheelPivotUp: () => _botService.sendCommand('S'),
                    onWeaponToggle: () => _botService.toggleWeapon(),
                  ),

                  const SizedBox(height: 14),

                  // 5. BOTÃO DE EMERGÊNCIA
                  SizedBox(
                    width: double.infinity,
                    child: OutlinedButton.icon(
                      style: OutlinedButton.styleFrom(
                        foregroundColor: const Color(0xFFEF4444),
                        side: const BorderSide(color: Color(0xFFEF4444), width: 1.5),
                        padding: const EdgeInsets.symmetric(vertical: 10),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                      ),
                      icon: const Icon(Icons.stop_circle, size: 20),
                      label: const Text(
                        'PARADA DE EMERGÊNCIA (CORTAR MOTORES)',
                        style: TextStyle(fontSize: 11, fontWeight: FontWeight.w900, letterSpacing: 1.0),
                      ),
                      onPressed: () {
                        HapticFeedback.heavyImpact();
                        _botService.emergencyStop();
                      },
                    ),
                  ),
                ],
              ),
            );
          },
        ),
      ),
    );
  }
}
