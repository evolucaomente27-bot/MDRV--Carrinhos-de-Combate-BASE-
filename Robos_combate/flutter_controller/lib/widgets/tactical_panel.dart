import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class TacticalPanel extends StatelessWidget {
  final bool isTurbo;
  final bool isArmed;
  final int turn90TimeMs;
  final Function(bool active) onTurboChanged;
  final Function(String maneuver, int durationMs) onManeuverTriggered;
  final Function(String wheelCmd) onWheelPivotDown;
  final VoidCallback onWheelPivotUp;
  final VoidCallback onWeaponToggle;

  const TacticalPanel({
    super.key,
    required this.isTurbo,
    required this.isArmed,
    required this.turn90TimeMs,
    required this.onTurboChanged,
    required this.onManeuverTriggered,
    required this.onWheelPivotDown,
    required this.onWheelPivotUp,
    required this.onWeaponToggle,
  });

  Widget _buildTacticalBtn({
    required String title,
    required String subtitle,
    required VoidCallback onTap,
    Color borderColor = const Color(0xFF38BDF8),
    Color textColor = const Color(0xFF38BDF8),
  }) {
    return Expanded(
      child: InkWell(
        onTap: () {
          HapticFeedback.mediumImpact();
          onTap();
        },
        borderRadius: BorderRadius.circular(10),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 4),
          decoration: BoxDecoration(
            color: const Color(0xFF1E2235),
            borderRadius: BorderRadius.circular(10),
            border: Border.all(color: borderColor, width: 1.5),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                title,
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w900,
                  color: textColor,
                ),
              ),
              const SizedBox(height: 2),
              Text(
                subtitle,
                style: const TextStyle(
                  fontSize: 9,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF94A3B8),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildWheelBtn(String label, String cmd) {
    return Expanded(
      child: Listener(
        onPointerDown: (_) {
          HapticFeedback.lightImpact();
          onWheelPivotDown(cmd);
        },
        onPointerUp: (_) => onWheelPivotUp(),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 8),
          decoration: BoxDecoration(
            color: const Color(0xFF1E2235),
            borderRadius: BorderRadius.circular(6),
            border: Border.all(color: const Color(0xFF475569)),
          ),
          child: Center(
            child: Text(
              label,
              style: const TextStyle(
                fontSize: 10,
                fontWeight: FontWeight.w800,
                color: Color(0xFFE2E8F0),
              ),
            ),
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // BOTÃO TURBO OVERDRIVE
        Listener(
          onPointerDown: (_) {
            HapticFeedback.heavyImpact();
            onTurboChanged(true);
          },
          onPointerUp: (_) {
            HapticFeedback.mediumImpact();
            onTurboChanged(false);
          },
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 100),
            width: double.infinity,
            padding: const EdgeInsets.symmetric(vertical: 14),
            decoration: BoxDecoration(
              gradient: isTurbo
                  ? const LinearGradient(
                      colors: [Color(0xFFFF9100), Color(0xFFFF3D00)],
                    )
                  : const LinearGradient(
                      colors: [Color(0xFFE11D48), Color(0xFFBE123C)],
                    ),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(
                color: isTurbo ? const Color(0xFFFFD600) : const Color(0xFFFB7185),
                width: 2,
              ),
              boxShadow: [
                BoxShadow(
                  color: isTurbo
                      ? const Color(0xFFFF3D00).withValues(alpha: 0.6)
                      : const Color(0xFFE11D48).withValues(alpha: 0.3),
                  blurRadius: isTurbo ? 16 : 8,
                  offset: const Offset(0, 4),
                ),
              ],
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  isTurbo ? Icons.bolt : Icons.local_fire_department,
                  color: Colors.white,
                  size: 22,
                ),
                const SizedBox(width: 8),
                Text(
                  isTurbo ? 'TURBO 100% FORÇADO!' : 'FORÇAR MOTOR (TURBO 100%)',
                  style: const TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.w900,
                    letterSpacing: 1.5,
                    color: Colors.white,
                  ),
                ),
              ],
            ),
          ),
        ),

        const SizedBox(height: 10),

        // MANOBRAS TÁTICAS RÁPIDAS (90° / 180°)
        const Text(
          'MANOBRAS AUTOMÁTICAS',
          style: TextStyle(
            fontSize: 10,
            fontWeight: FontWeight.w800,
            color: Color(0xFF94A3B8),
            letterSpacing: 1.2,
          ),
        ),
        const SizedBox(height: 6),
        Row(
          children: [
            _buildTacticalBtn(
              title: '↰ 90°',
              subtitle: 'ESQUERDA',
              onTap: () => onManeuverTriggered('T90L', turn90TimeMs),
            ),
            const SizedBox(width: 8),
            _buildTacticalBtn(
              title: '🔄 180°',
              subtitle: 'MEIA-VOLTA',
              borderColor: const Color(0xFFF59E0B),
              textColor: const Color(0xFFFBBF24),
              onTap: () => onManeuverTriggered('T180', (turn90TimeMs * 2.1).round()),
            ),
            const SizedBox(width: 8),
            _buildTacticalBtn(
              title: '90° ↱',
              subtitle: 'DIREITA',
              onTap: () => onManeuverTriggered('T90R', turn90TimeMs),
            ),
          ],
        ),

        const SizedBox(height: 10),

        // PIVÔ DE RODA ÚNICA
        const Text(
          'PIVÔ DE RODA ÚNICA (PONTO FIXO)',
          style: TextStyle(
            fontSize: 10,
            fontWeight: FontWeight.w800,
            color: Color(0xFF94A3B8),
            letterSpacing: 1.2,
          ),
        ),
        const SizedBox(height: 6),
        Row(
          children: [
            Expanded(
              child: Container(
                padding: const EdgeInsets.all(6),
                decoration: BoxDecoration(
                  color: const Color(0x1AFFFFFF),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: const Color(0x1FFFFFFF)),
                ),
                child: Column(
                  children: [
                    const Text('RODA ESQ', style: TextStyle(fontSize: 9, fontWeight: FontWeight.bold, color: Color(0xFFCBD5E1))),
                    const SizedBox(height: 4),
                    Row(
                      children: [
                        _buildWheelBtn('FRENTE', 'LF'),
                        const SizedBox(width: 4),
                        _buildWheelBtn('RÉ', 'LB'),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(width: 8),
            Expanded(
              child: Container(
                padding: const EdgeInsets.all(6),
                decoration: BoxDecoration(
                  color: const Color(0x1AFFFFFF),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: const Color(0x1FFFFFFF)),
                ),
                child: Column(
                  children: [
                    const Text('RODA DIR', style: TextStyle(fontSize: 9, fontWeight: FontWeight.bold, color: Color(0xFFCBD5E1))),
                    const SizedBox(height: 4),
                    Row(
                      children: [
                        _buildWheelBtn('FRENTE', 'RF'),
                        const SizedBox(width: 4),
                        _buildWheelBtn('RÉ', 'RB'),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),

        const SizedBox(height: 10),

        // DISPARO DE ARMA (OPCIONAL)
        InkWell(
          onTap: () {
            HapticFeedback.heavyImpact();
            onWeaponToggle();
          },
          borderRadius: BorderRadius.circular(10),
          child: Container(
            width: double.infinity,
            padding: const EdgeInsets.symmetric(vertical: 10),
            decoration: BoxDecoration(
              color: isArmed ? const Color(0xFFDC2626) : const Color(0xFF1E2235),
              borderRadius: BorderRadius.circular(10),
              border: Border.all(
                color: isArmed ? const Color(0xFFEF4444) : const Color(0xFF475569),
              ),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  isArmed ? Icons.warning : Icons.shield_outlined,
                  size: 16,
                  color: isArmed ? Colors.white : const Color(0xFF94A3B8),
                ),
                const SizedBox(width: 8),
                Text(
                  isArmed ? '⚔️ ARMA DISPARADA (ATIVA)!' : '🛡️ ARMA EM ESPERA (DESARMADA)',
                  style: TextStyle(
                    fontSize: 11,
                    fontWeight: FontWeight.w800,
                    color: isArmed ? Colors.white : const Color(0xFF94A3B8),
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
