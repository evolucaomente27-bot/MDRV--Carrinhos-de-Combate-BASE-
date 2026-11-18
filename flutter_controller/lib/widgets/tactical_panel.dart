import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../models/bot_models.dart';
import '../theme/app_theme.dart';

class TacticalPanel extends StatelessWidget {
  final bool isTurbo;
  final bool isArmed;
  final List<TacticalButtonConfig> buttons;
  final AppColorTheme colorTheme;
  final Function(bool active) onTurboChanged;
  final Function(TacticalButtonConfig btn) onTacticalAction;
  final Function(String wheelCmd) onWheelPivotDown;
  final VoidCallback onWheelPivotUp;
  final VoidCallback onWeaponToggle;

  const TacticalPanel({
    super.key,
    required this.isTurbo,
    required this.isArmed,
    required this.buttons,
    required this.colorTheme,
    required this.onTurboChanged,
    required this.onTacticalAction,
    required this.onWheelPivotDown,
    required this.onWheelPivotUp,
    required this.onWeaponToggle,
  });

  Widget _buildButton(TacticalButtonConfig btn, Color themeColor) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: () {
          HapticFeedback.mediumImpact();
          onTacticalAction(btn);
        },
        borderRadius: BorderRadius.circular(10),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 8),
          decoration: BoxDecoration(
            color: AppTheme.surfaceCard,
            borderRadius: BorderRadius.circular(10),
            border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(btn.actionType.defaultIcon, size: 15, color: themeColor),
              const SizedBox(width: 6),
              Flexible(
                child: FittedBox(
                  fit: BoxFit.scaleDown,
                  child: Text(
                    btn.customTitle,
                    style: const TextStyle(
                      fontSize: 11,
                      fontWeight: FontWeight.w700,
                      color: AppTheme.textPrimary,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final primaryColor = colorTheme.primaryColor;
    final accentColor = colorTheme.accentColor;

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        // 1. GATILHO OVERDRIVE TURBO LIMPO
        GestureDetector(
          onLongPressStart: (_) {
            HapticFeedback.heavyImpact();
            onTurboChanged(true);
          },
          onLongPressEnd: (_) {
            HapticFeedback.lightImpact();
            onTurboChanged(false);
          },
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 120),
            padding: const EdgeInsets.symmetric(vertical: 11, horizontal: 16),
            decoration: BoxDecoration(
              color: isTurbo ? AppTheme.violetTurbo : AppTheme.surfaceCard,
              borderRadius: BorderRadius.circular(10),
              border: Border.all(
                color: isTurbo ? Colors.white.withValues(alpha: 0.6) : Colors.white.withValues(alpha: 0.05),
              ),
              boxShadow: isTurbo
                  ? [
                      BoxShadow(
                        color: AppTheme.violetTurbo.withValues(alpha: 0.4),
                        blurRadius: 14,
                      ),
                    ]
                  : [],
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  Icons.bolt_rounded,
                  size: 17,
                  color: isTurbo ? Colors.white : AppTheme.violetTurbo,
                ),
                const SizedBox(width: 8),
                Text(
                  isTurbo ? 'OVERDRIVE ATIVO' : 'SEGURE P/ TURBO',
                  style: TextStyle(
                    fontSize: 11.5,
                    fontWeight: FontWeight.w800,
                    letterSpacing: 0.8,
                    color: isTurbo ? Colors.white : AppTheme.textPrimary,
                  ),
                ),
              ],
            ),
          ),
        ),

        const SizedBox(height: 8),

        // 2. BOTÕES TÁTICOS (GRADE 2X2 MINIMALISTA)
        if (buttons.isNotEmpty) ...[
          Row(
            children: [
              Expanded(child: _buildButton(buttons[0], primaryColor)),
              if (buttons.length > 1) ...[
                const SizedBox(width: 8),
                Expanded(child: _buildButton(buttons[1], accentColor)),
              ],
            ],
          ),
        ],

        if (buttons.length > 2) ...[
          const SizedBox(height: 8),
          Row(
            children: [
              Expanded(child: _buildButton(buttons[2], accentColor)),
              if (buttons.length > 3) ...[
                const SizedBox(width: 8),
                Expanded(child: _buildButton(buttons[3], primaryColor)),
              ],
            ],
          ),
        ],

        const SizedBox(height: 8),

        // 3. CHAVE DE ARMA MINIMALISTA
        InkWell(
          onTap: () {
            HapticFeedback.heavyImpact();
            onWeaponToggle();
          },
          borderRadius: BorderRadius.circular(10),
          child: Container(
            padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 12),
            decoration: BoxDecoration(
              color: isArmed ? AppTheme.crimsonDanger.withValues(alpha: 0.15) : AppTheme.surfaceCard,
              borderRadius: BorderRadius.circular(10),
              border: Border.all(
                color: isArmed ? AppTheme.crimsonDanger.withValues(alpha: 0.6) : Colors.white.withValues(alpha: 0.05),
              ),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  isArmed ? Icons.shield_rounded : Icons.shield_outlined,
                  size: 15,
                  color: isArmed ? AppTheme.crimsonDanger : AppTheme.textMuted,
                ),
                const SizedBox(width: 8),
                Text(
                  isArmed ? 'ARMA ATIVA' : 'ARMA SEGURA',
                  style: TextStyle(
                    fontSize: 10.5,
                    fontWeight: FontWeight.w800,
                    letterSpacing: 0.6,
                    color: isArmed ? AppTheme.crimsonDanger : AppTheme.textSecondary,
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
