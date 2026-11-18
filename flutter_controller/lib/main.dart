import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'models/bot_models.dart';
import 'services/bot_communication_service.dart';
import 'services/preferences_service.dart';
import 'theme/app_theme.dart';
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
    DeviceOrientation.landscapeLeft,
    DeviceOrientation.landscapeRight,
  ]);
  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.light,
      systemNavigationBarColor: AppTheme.bgDark,
      systemNavigationBarIconBrightness: Brightness.light,
    ),
  );
  runApp(const CombatBotApp());
}

class CombatBotApp extends StatefulWidget {
  const CombatBotApp({super.key});

  @override
  State<CombatBotApp> createState() => _CombatBotAppState();
}

class _CombatBotAppState extends State<CombatBotApp> {
  BotConfig _config = BotConfig();

  @override
  void initState() {
    super.initState();
    _loadSavedConfig();
  }

  Future<void> _loadSavedConfig() async {
    final loaded = await PreferencesService.loadConfig();
    if (mounted) {
      setState(() {
        _config = loaded;
      });
    }
  }

  void _onConfigChanged() {
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Combat Bot Pro Controller',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.buildTheme(_config.colorTheme),
      home: ControllerHomeScreen(
        config: _config,
        onConfigChanged: _onConfigChanged,
      ),
    );
  }
}

class ControllerHomeScreen extends StatefulWidget {
  final BotConfig config;
  final VoidCallback onConfigChanged;

  const ControllerHomeScreen({
    super.key,
    required this.config,
    required this.onConfigChanged,
  });

  @override
  State<ControllerHomeScreen> createState() => _ControllerHomeScreenState();
}

class _ControllerHomeScreenState extends State<ControllerHomeScreen> {
  late final BotCommunicationService _botService;
  ControlMode _controlMode = ControlMode.joystick360;

  @override
  void initState() {
    super.initState();
    _botService = BotCommunicationService(config: widget.config);

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
        config: widget.config,
        service: _botService,
        onConfigChanged: () {
          widget.onConfigChanged();
          setState(() {});
        },
      ),
    );
  }

  Widget _buildModeSelector() {
    final primaryColor = widget.config.colorTheme.primaryColor;

    return Container(
      padding: const EdgeInsets.all(2),
      decoration: BoxDecoration(
        color: AppTheme.surfaceCard,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
      ),
      child: Row(
        children: [
          Expanded(
            child: InkWell(
              onTap: () {
                HapticFeedback.selectionClick();
                setState(() => _controlMode = ControlMode.joystick360);
              },
              borderRadius: BorderRadius.circular(6),
              child: Container(
                padding: const EdgeInsets.symmetric(vertical: 6),
                decoration: BoxDecoration(
                  color: _controlMode == ControlMode.joystick360
                      ? primaryColor
                      : Colors.transparent,
                  borderRadius: BorderRadius.circular(6),
                ),
                child: FittedBox(
                  fit: BoxFit.scaleDown,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        Icons.trip_origin_rounded,
                        size: 13,
                        color: _controlMode == ControlMode.joystick360
                            ? Colors.white
                            : AppTheme.textSecondary,
                      ),
                      const SizedBox(width: 5),
                      Text(
                        'JOYSTICK 360°',
                        style: TextStyle(
                          fontSize: 10,
                          fontWeight: FontWeight.w700,
                          letterSpacing: 0.5,
                          color: _controlMode == ControlMode.joystick360
                            ? Colors.white
                            : AppTheme.textSecondary,
                        ),
                      ),
                    ],
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
              borderRadius: BorderRadius.circular(6),
              child: Container(
                padding: const EdgeInsets.symmetric(vertical: 6),
                decoration: BoxDecoration(
                  color: _controlMode == ControlMode.dpad
                      ? primaryColor
                      : Colors.transparent,
                  borderRadius: BorderRadius.circular(6),
                ),
                child: FittedBox(
                  fit: BoxFit.scaleDown,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        Icons.gamepad_rounded,
                        size: 13,
                        color: _controlMode == ControlMode.dpad
                            ? Colors.white
                            : AppTheme.textSecondary,
                      ),
                      const SizedBox(width: 5),
                      Text(
                        'D-PAD TÁTIL',
                        style: TextStyle(
                          fontSize: 10,
                          fontWeight: FontWeight.w700,
                          letterSpacing: 0.5,
                          color: _controlMode == ControlMode.dpad
                            ? Colors.white
                            : AppTheme.textSecondary,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildEStopButton({bool isFullWidth = true}) {
    return SizedBox(
      width: isFullWidth ? double.infinity : null,
      child: ElevatedButton.icon(
        style: ElevatedButton.styleFrom(
          backgroundColor: AppTheme.crimsonDanger,
          foregroundColor: Colors.white,
          elevation: 0,
          padding: const EdgeInsets.symmetric(vertical: 9, horizontal: 14),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
        icon: const Icon(Icons.power_settings_new_rounded, size: 16),
        label: const Text(
          'E-STOP • CORTAR MOTORES',
          style: TextStyle(
            fontSize: 10.5,
            fontWeight: FontWeight.w800,
            letterSpacing: 0.8,
          ),
        ),
        onPressed: () {
          HapticFeedback.heavyImpact();
          _botService.emergencyStop();
        },
      ),
    );
  }

  Widget _buildPortraitLayout() {
    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Column(
        children: [
          // 1. INSTRUMENTAÇÃO / TELEMETRIA LIMPA
          TelemetryGauges(
            leftPwm: _botService.leftPwm,
            rightPwm: _botService.rightPwm,
            maxPwm: widget.config.maxPwm,
            pingMs: _botService.pingMs,
            isConnected: _botService.isConnected,
            statusText: _botService.statusMessage,
            steeringTrim: widget.config.steeringTrim,
            primaryColor: widget.config.colorTheme.primaryColor,
          ),

          const SizedBox(height: 10),

          // 2. SELETOR DE MODO
          _buildModeSelector(),

          const SizedBox(height: 12),

          // 3. SUPERFÍCIE DE CONTROLE (JOYSTICK OU D-PAD)
          _controlMode == ControlMode.joystick360
              ? AnalogJoystick(
                  radius: widget.config.joystickRadius,
                  stickRadius: (widget.config.joystickRadius * 0.35).clamp(32.0, 48.0),
                  isTurbo: _botService.isTurboActive,
                  primaryColor: widget.config.colorTheme.primaryColor,
                  accentColor: widget.config.colorTheme.accentColor,
                  onChanged: (v, w) => _botService.updateJoystickVelocity(v, w),
                  onReleased: () => _botService.updateJoystickVelocity(0, 0),
                )
              : DpadController(
                  onDirectionDown: (dir) => _botService.sendCommand(dir),
                  onDirectionUp: () => _botService.sendCommand('S'),
                ),

          const SizedBox(height: 12),

          // 4. PAINEL TÁTICO PERSONALIZADO LIMPO
          TacticalPanel(
            isTurbo: _botService.isTurboActive,
            isArmed: _botService.isArmed,
            buttons: widget.config.tacticalButtons,
            colorTheme: widget.config.colorTheme,
            onTurboChanged: (active) => _botService.setTurbo(active),
            onTacticalAction: (btn) => _botService.executeTacticalAction(btn),
            onWheelPivotDown: (cmd) => _botService.sendCommand(cmd),
            onWheelPivotUp: () => _botService.sendCommand('S'),
            onWeaponToggle: () => _botService.toggleWeapon(),
          ),

          const SizedBox(height: 10),

          // 5. PARADA DE EMERGÊNCIA
          _buildEStopButton(isFullWidth: true),

          const SizedBox(height: 8),
        ],
      ),
    );
  }

  Widget _buildLandscapeLayout() {
    final primaryColor = widget.config.colorTheme.primaryColor;
    final accentColor = widget.config.colorTheme.accentColor;

    final joystickWing = Expanded(
      flex: 4,
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          _buildModeSelector(),
          const SizedBox(height: 8),
          Expanded(
            child: Center(
              child: _controlMode == ControlMode.joystick360
                  ? AnalogJoystick(
                      radius: (widget.config.joystickRadius * 0.82).clamp(80.0, 105.0),
                      stickRadius: (widget.config.joystickRadius * 0.30).clamp(28.0, 38.0),
                      isTurbo: _botService.isTurboActive,
                      primaryColor: primaryColor,
                      accentColor: accentColor,
                      onChanged: (v, w) => _botService.updateJoystickVelocity(v, w),
                      onReleased: () => _botService.updateJoystickVelocity(0, 0),
                    )
                  : DpadController(
                      onDirectionDown: (dir) => _botService.sendCommand(dir),
                      onDirectionUp: () => _botService.sendCommand('S'),
                    ),
            ),
          ),
        ],
      ),
    );

    final centerWing = Expanded(
      flex: 3,
      child: Column(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          TelemetryGauges(
            leftPwm: _botService.leftPwm,
            rightPwm: _botService.rightPwm,
            maxPwm: widget.config.maxPwm,
            pingMs: _botService.pingMs,
            isConnected: _botService.isConnected,
            statusText: _botService.statusMessage,
            compactMode: true,
            steeringTrim: widget.config.steeringTrim,
            primaryColor: primaryColor,
          ),
          _buildEStopButton(isFullWidth: true),
        ],
      ),
    );

    final tacticalWing = Expanded(
      flex: 4,
      child: SingleChildScrollView(
        child: TacticalPanel(
          isTurbo: _botService.isTurboActive,
          isArmed: _botService.isArmed,
          buttons: widget.config.tacticalButtons,
          colorTheme: widget.config.colorTheme,
          onTurboChanged: (active) => _botService.setTurbo(active),
          onTacticalAction: (btn) => _botService.executeTacticalAction(btn),
          onWheelPivotDown: (cmd) => _botService.sendCommand(cmd),
          onWheelPivotUp: () => _botService.sendCommand('S'),
          onWeaponToggle: () => _botService.toggleWeapon(),
        ),
      ),
    );

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: widget.config.handedness == Handedness.rightHanded
            ? [joystickWing, const SizedBox(width: 14), centerWing, const SizedBox(width: 14), tacticalWing]
            : [tacticalWing, const SizedBox(width: 14), centerWing, const SizedBox(width: 14), joystickWing],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final isConnected = _botService.isConnected;
    final primaryColor = widget.config.colorTheme.primaryColor;

    return Scaffold(
      appBar: AppBar(
        titleSpacing: 16,
        title: Row(
          children: [
            Container(
              width: 7,
              height: 7,
              decoration: BoxDecoration(
                color: isConnected ? AppTheme.emeraldSafe : AppTheme.crimsonDanger,
                shape: BoxShape.circle,
              ),
            ),
            const SizedBox(width: 8),
            const Text(
              'COMBAT BOT PRO',
              style: TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w800,
                letterSpacing: 1.0,
                color: AppTheme.textPrimary,
              ),
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.sync_rounded, color: AppTheme.textSecondary, size: 18),
            tooltip: 'Reconectar',
            onPressed: () {
              HapticFeedback.lightImpact();
              _botService.connect();
            },
          ),
          IconButton(
            icon: Icon(Icons.tune_rounded, color: primaryColor, size: 18),
            tooltip: 'Personalização & Configurações',
            onPressed: () {
              HapticFeedback.lightImpact();
              _openSettings();
            },
          ),
          const SizedBox(width: 8),
        ],
      ),
      body: SafeArea(
        child: AnimatedBuilder(
          animation: _botService,
          builder: (context, _) {
            return OrientationBuilder(
              builder: (context, orientation) {
                return orientation == Orientation.landscape
                    ? _buildLandscapeLayout()
                    : _buildPortraitLayout();
              },
            );
          },
        ),
      ),
    );
  }
}
