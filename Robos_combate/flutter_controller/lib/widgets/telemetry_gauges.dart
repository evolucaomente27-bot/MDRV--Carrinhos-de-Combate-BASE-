import 'package:flutter/material.dart';

class TelemetryGauges extends StatelessWidget {
  final int leftPwm;
  final int rightPwm;
  final int maxPwm;
  final int pingMs;
  final bool isConnected;
  final String statusText;

  const TelemetryGauges({
    super.key,
    required this.leftPwm,
    required this.rightPwm,
    required this.maxPwm,
    required this.pingMs,
    required this.isConnected,
    required this.statusText,
  });

  Widget _buildMotorGauge(String title, int pwm) {
    final double pct = (pwm.abs() / maxPwm).clamp(0.0, 1.0);
    final bool isReverse = pwm < 0;
    final bool isStopped = pwm == 0;

    final String directionText = isStopped
        ? 'PARADO'
        : isReverse
            ? 'RÉ'
            : 'AVANÇO';

    final Color barColor = isStopped
        ? const Color(0xFF64748B)
        : isReverse
            ? const Color(0xFFF59E0B)
            : const Color(0xFF00E676);

    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        decoration: BoxDecoration(
          color: const Color(0xFF1E2235),
          borderRadius: BorderRadius.circular(10),
          border: Border.all(color: const Color(0xFF334155)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 11,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF94A3B8),
                  ),
                ),
                Text(
                  directionText,
                  style: TextStyle(
                    fontSize: 10,
                    fontWeight: FontWeight.w900,
                    color: barColor,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 4),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  '${(pct * 100).round()}%',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w900,
                    color: barColor,
                    fontFamily: 'monospace',
                  ),
                ),
                Text(
                  'PWM: $pwm',
                  style: const TextStyle(
                    fontSize: 10,
                    color: Color(0xFF94A3B8),
                    fontFamily: 'monospace',
                  ),
                ),
              ],
            ),
            const SizedBox(height: 6),
            ClipRRect(
              borderRadius: BorderRadius.circular(3),
              child: LinearProgressIndicator(
                value: pct,
                backgroundColor: const Color(0xFF0F172A),
                valueColor: AlwaysStoppedAnimation<Color>(barColor),
                minHeight: 6,
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    Color pingColor = const Color(0xFF00E676);
    if (pingMs > 20) pingColor = const Color(0xFFF59E0B);
    if (pingMs > 60 || !isConnected) pingColor = const Color(0xFFEF4444);

    return Column(
      children: [
        // Linha de Status e Ping
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
          decoration: BoxDecoration(
            color: const Color(0xFF141724),
            borderRadius: BorderRadius.circular(8),
            border: Border.all(color: const Color(0x33FFFFFF)),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: Text(
                  statusText,
                  style: TextStyle(
                    fontSize: 11,
                    fontWeight: FontWeight.w600,
                    color: isConnected ? const Color(0xFF69F0AE) : const Color(0xFFF87171),
                  ),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              Row(
                children: [
                  Icon(Icons.wifi, size: 14, color: pingColor),
                  const SizedBox(width: 4),
                  Text(
                    isConnected ? '$pingMs ms' : '--',
                    style: TextStyle(
                      fontSize: 11,
                      fontWeight: FontWeight.bold,
                      color: pingColor,
                      fontFamily: 'monospace',
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
        const SizedBox(height: 8),
        // Medidores L e R
        Row(
          children: [
            _buildMotorGauge('MOTOR ESQUERDO', leftPwm),
            const SizedBox(width: 8),
            _buildMotorGauge('MOTOR DIREITO', rightPwm),
          ],
        ),
      ],
    );
  }
}
