import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class TelemetryGauges extends StatelessWidget {
  final int leftPwm;
  final int rightPwm;
  final int maxPwm;
  final int pingMs;
  final bool isConnected;
  final String statusText;
  final bool compactMode;
  final int steeringTrim;
  final Color? primaryColor;

  const TelemetryGauges({
    super.key,
    required this.leftPwm,
    required this.rightPwm,
    required this.maxPwm,
    required this.pingMs,
    required this.isConnected,
    required this.statusText,
    this.compactMode = false,
    this.steeringTrim = 0,
    this.primaryColor,
  });

  Widget _buildMeter({
    required String label,
    required int pwm,
    required Color color,
  }) {
    final double pct = (pwm.abs() / maxPwm).clamp(0.0, 1.0);
    final bool isReverse = pwm < 0;
    final bool isZero = pwm == 0;

    final Color accent = isZero
        ? AppTheme.textMuted
        : isReverse
            ? AppTheme.amberWarning
            : color;

    final String sign = isZero ? '' : isReverse ? '-' : '+';
    final String pctStr = '$sign${(pct * 100).round()}%';

    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Text(
          label,
          style: const TextStyle(
            fontSize: 10,
            fontWeight: FontWeight.w700,
            color: AppTheme.textSecondary,
          ),
        ),
        const SizedBox(width: 6),
        SizedBox(
          width: 55,
          child: ClipRRect(
            borderRadius: BorderRadius.circular(2),
            child: LinearProgressIndicator(
              value: pct,
              minHeight: 4,
              backgroundColor: Colors.white.withValues(alpha: 0.08),
              valueColor: AlwaysStoppedAnimation<Color>(accent),
            ),
          ),
        ),
        const SizedBox(width: 6),
        SizedBox(
          width: 36,
          child: Text(
            pctStr,
            style: TextStyle(
              fontSize: 10,
              fontWeight: FontWeight.w700,
              color: accent,
              fontFamily: 'monospace',
            ),
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    final color = primaryColor ?? AppTheme.primaryBlue;

    final Color pingColor = pingMs <= 0
        ? AppTheme.textMuted
        : pingMs < 20
            ? AppTheme.emeraldSafe
            : pingMs < 70
                ? AppTheme.amberWarning
                : AppTheme.crimsonDanger;

    if (compactMode) {
      // Modo Compacto para a coluna central do Landscape
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
        decoration: BoxDecoration(
          color: AppTheme.surfaceCard,
          borderRadius: BorderRadius.circular(10),
          border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Container(
                      width: 6,
                      height: 6,
                      decoration: BoxDecoration(
                        color: isConnected ? AppTheme.emeraldSafe : AppTheme.crimsonDanger,
                        shape: BoxShape.circle,
                      ),
                    ),
                    const SizedBox(width: 5),
                    Text(
                      isConnected ? 'ONLINE' : 'OFFLINE',
                      style: TextStyle(
                        fontSize: 9,
                        fontWeight: FontWeight.w800,
                        color: isConnected ? AppTheme.emeraldSafe : AppTheme.textMuted,
                      ),
                    ),
                  ],
                ),
                Text(
                  pingMs > 0 ? '$pingMs ms' : '-- ms',
                  style: TextStyle(
                    fontSize: 9.5,
                    fontWeight: FontWeight.bold,
                    color: pingColor,
                    fontFamily: 'monospace',
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            _buildMeter(label: 'M1', pwm: leftPwm, color: color),
            const SizedBox(height: 4),
            _buildMeter(label: 'M2', pwm: rightPwm, color: color),
          ],
        ),
      );
    }

    // Modo Normal (Portrait) - Barra horizontal limpa e discreta
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: AppTheme.surfaceCard,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          _buildMeter(label: 'M1', pwm: leftPwm, color: color),
          Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                width: 6,
                height: 6,
                decoration: BoxDecoration(
                  color: isConnected ? AppTheme.emeraldSafe : AppTheme.crimsonDanger,
                  shape: BoxShape.circle,
                ),
              ),
              const SizedBox(width: 4),
              Text(
                pingMs > 0 ? '$pingMs ms' : 'OFFLINE',
                style: TextStyle(
                  fontSize: 9.5,
                  fontWeight: FontWeight.w700,
                  color: isConnected ? pingColor : AppTheme.textMuted,
                  fontFamily: 'monospace',
                ),
              ),
              if (steeringTrim != 0) ...[
                const SizedBox(width: 6),
                Text(
                  'T:${steeringTrim > 0 ? "+$steeringTrim" : "$steeringTrim"}',
                  style: const TextStyle(
                    fontSize: 9,
                    fontWeight: FontWeight.bold,
                    color: AppTheme.amberWarning,
                    fontFamily: 'monospace',
                  ),
                ),
              ],
            ],
          ),
          _buildMeter(label: 'M2', pwm: rightPwm, color: color),
        ],
      ),
    );
  }
}
