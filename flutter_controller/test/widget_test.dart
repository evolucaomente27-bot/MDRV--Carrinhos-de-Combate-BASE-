import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/material.dart';
import 'package:combat_bot_controller/main.dart';
import 'package:combat_bot_controller/models/bot_models.dart';
import 'package:combat_bot_controller/services/bot_communication_service.dart';

void main() {
  group('Combat Bot Pro Controller Tests', () {
    testWidgets('UI Smoke Test - Renders Brand, Gauges and E-STOP', (WidgetTester tester) async {
      await tester.pumpWidget(const CombatBotApp());
      await tester.pump();

      expect(find.text('COMBAT BOT PRO'), findsOneWidget);
      expect(find.text('E-STOP • CORTAR MOTORES'), findsOneWidget);
      expect(find.text('JOYSTICK 360°'), findsOneWidget);
      expect(find.text('D-PAD TÁTIL'), findsOneWidget);
    });

    testWidgets('UI Interaction Test - Toggle to D-Pad mode', (WidgetTester tester) async {
      await tester.pumpWidget(const CombatBotApp());
      await tester.pump();

      final dpadButton = find.text('D-PAD TÁTIL');
      expect(dpadButton, findsOneWidget);

      await tester.tap(dpadButton);
      await tester.pump();

      expect(find.byIcon(Icons.keyboard_arrow_up_rounded), findsOneWidget);
      expect(find.byIcon(Icons.keyboard_arrow_down_rounded), findsOneWidget);
    });

    testWidgets('UI Interaction Test - Open Customization Center Dialog with 5 Tabs', (WidgetTester tester) async {
      await tester.pumpWidget(const CombatBotApp());
      await tester.pump();

      final settingsIcon = find.byIcon(Icons.tune_rounded);
      expect(settingsIcon, findsOneWidget);

      await tester.tap(settingsIcon);
      await tester.pumpAndSettle();

      expect(find.text('CENTRAL DE PERSONALIZAÇÃO'), findsOneWidget);
      expect(find.text('CORES'), findsOneWidget);
      expect(find.text('ERGONOMIA'), findsOneWidget);
      expect(find.text('MOTORES & TRIM'), findsOneWidget);
      expect(find.text('BOTÕES TÁTICOS'), findsOneWidget);
      expect(find.text('REDE'), findsOneWidget);

      // Fecha o diálogo
      final cancelButton = find.text('CANCELAR');
      expect(cancelButton, findsOneWidget);
      await tester.tap(cancelButton);
      await tester.pumpAndSettle();
    });

    test('Unit Test - Customization: Axis Inversion & Steering Trim', () {
      final config = BotConfig(
        maxPwm: 255,
        speedPercent: 100,
        deadzone: 0.04,
        stickCurve: StickCurve.linear,
        invertThrottleY: false,
        invertSteeringX: false,
        steeringTrim: 0,
      );
      final service = BotCommunicationService(config: config);

      // Forward normal (normV: 1.0, normW: 0.0) -> +255, +255
      service.updateJoystickVelocity(1.0, 0.0);
      expect(service.leftPwm, 255);
      expect(service.rightPwm, 255);

      // Ativa Inversão de Y (Avanço/Ré)
      config.invertThrottleY = true;
      service.updateJoystickVelocity(1.0, 0.0);
      expect(service.leftPwm, -255);
      expect(service.rightPwm, -255);

      // Desativa inversão e testa Trim de Direção (+10% para corrigir puxada)
      config.invertThrottleY = false;
      config.steeringTrim = 10;
      service.updateJoystickVelocity(1.0, 0.0);
      expect(service.leftPwm > service.rightPwm, true);

      service.dispose();
    });

    test('Unit Test - Customization: Tactical Button Actions Execution', () {
      final config = BotConfig();
      final service = BotCommunicationService(config: config);

      final customBtn = TacticalButtonConfig(
        actionType: TacticalActionType.turn90Left,
        customTitle: 'ESQUADRO ESQ',
        durationMs: 220,
      );

      service.executeTacticalAction(customBtn);
      expect(service.statusMessage.contains('L90'), true);

      service.dispose();
    });

    test('Unit Test - Configuration Serialization & Deserialization', () {
      final original = BotConfig(
        robotIp: '192.168.1.50',
        colorTheme: AppColorTheme.crimsonFury,
        handedness: Handedness.leftHanded,
        invertThrottleY: true,
        invertSteeringX: true,
        stickCurve: StickCurve.aggressive,
        steeringTrim: 12,
        speedPercent: 85,
      );

      final jsonStr = original.serialize();
      final deserialized = BotConfig.deserialize(jsonStr);

      expect(deserialized.robotIp, '192.168.1.50');
      expect(deserialized.colorTheme, AppColorTheme.crimsonFury);
      expect(deserialized.handedness, Handedness.leftHanded);
      expect(deserialized.invertThrottleY, true);
      expect(deserialized.invertSteeringX, true);
      expect(deserialized.stickCurve, StickCurve.aggressive);
      expect(deserialized.steeringTrim, 12);
      expect(deserialized.speedPercent, 85);
    });
  });
}
