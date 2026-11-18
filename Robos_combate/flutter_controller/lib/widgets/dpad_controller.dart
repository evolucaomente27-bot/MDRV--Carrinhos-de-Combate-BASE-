import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class DpadController extends StatelessWidget {
  final Function(String dir) onDirectionDown;
  final VoidCallback onDirectionUp;

  const DpadController({
    super.key,
    required this.onDirectionDown,
    required this.onDirectionUp,
  });

  Widget _buildDpadBtn(String dir, String label, {bool isStop = false}) {
    return Listener(
      onPointerDown: (_) {
        HapticFeedback.lightImpact();
        onDirectionDown(dir);
      },
      onPointerUp: (_) {
        onDirectionUp();
      },
      child: Container(
        decoration: BoxDecoration(
          color: isStop ? const Color(0xFFDC2626) : const Color(0xFF1E2235),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: isStop ? const Color(0xFFEF4444) : const Color(0xFF334155),
            width: 1.5,
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.3),
              blurRadius: 4,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Center(
          child: Text(
            label,
            style: TextStyle(
              fontSize: isStop ? 13 : 22,
              fontWeight: FontWeight.w900,
              color: isStop ? Colors.white : const Color(0xFFE2E8F0),
            ),
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 240,
      height: 240,
      child: GridView.count(
        crossAxisCount: 3,
        mainAxisSpacing: 8,
        crossAxisSpacing: 8,
        physics: const NeverScrollableScrollPhysics(),
        children: [
          _buildDpadBtn('G', '↖'),
          _buildDpadBtn('F', '▲'),
          _buildDpadBtn('I', '↗'),
          _buildDpadBtn('L', '◀'),
          _buildDpadBtn('S', 'STOP', isStop: true),
          _buildDpadBtn('R', '▶'),
          _buildDpadBtn('H', '↙'),
          _buildDpadBtn('B', '▼'),
          _buildDpadBtn('J', '↘'),
        ],
      ),
    );
  }
}
