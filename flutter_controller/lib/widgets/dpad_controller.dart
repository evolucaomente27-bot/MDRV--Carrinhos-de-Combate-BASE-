import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../theme/app_theme.dart';

class DpadController extends StatefulWidget {
  final Function(String direction) onDirectionDown;
  final VoidCallback onDirectionUp;

  const DpadController({
    super.key,
    required this.onDirectionDown,
    required this.onDirectionUp,
  });

  @override
  State<DpadController> createState() => _DpadControllerState();
}

class _DpadControllerState extends State<DpadController> {
  String? _activeDirection;

  void _handlePressDown(String dir) {
    if (_activeDirection == dir) return;
    HapticFeedback.lightImpact();
    setState(() => _activeDirection = dir);
    widget.onDirectionDown(dir);
  }

  void _handlePressUp() {
    if (_activeDirection == null) return;
    HapticFeedback.selectionClick();
    setState(() => _activeDirection = null);
    widget.onDirectionUp();
  }

  Widget _buildKey({
    required String dir,
    required IconData icon,
    BorderRadius? borderRadius,
  }) {
    final bool isActive = _activeDirection == dir;

    return Listener(
      onPointerDown: (_) => _handlePressDown(dir),
      onPointerUp: (_) => _handlePressUp(),
      onPointerCancel: (_) => _handlePressUp(),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 100),
        decoration: BoxDecoration(
          color: isActive ? AppTheme.primaryBlue : const Color(0xFF161922),
          borderRadius: borderRadius ?? BorderRadius.circular(8),
          border: Border.all(
            color: isActive ? AppTheme.primaryBlue : Colors.white.withValues(alpha: 0.05),
          ),
        ),
        child: Center(
          child: Icon(
            icon,
            size: 28,
            color: isActive ? Colors.white : AppTheme.textSecondary,
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: SizedBox(
        width: 190,
        height: 190,
        child: Stack(
          children: [
            // CIMA (Frente)
            Align(
              alignment: Alignment.topCenter,
              child: SizedBox(
                width: 60,
                height: 60,
                child: _buildKey(
                  dir: 'F',
                  icon: Icons.keyboard_arrow_up_rounded,
                  borderRadius: const BorderRadius.vertical(top: Radius.circular(12)),
                ),
              ),
            ),

            // ESQUERDA
            Align(
              alignment: Alignment.centerLeft,
              child: SizedBox(
                width: 60,
                height: 60,
                child: _buildKey(
                  dir: 'L',
                  icon: Icons.keyboard_arrow_left_rounded,
                  borderRadius: const BorderRadius.horizontal(left: Radius.circular(12)),
                ),
              ),
            ),

            // CENTRO (Núcleo decorativo)
            Align(
              alignment: Alignment.center,
              child: Container(
                width: 52,
                height: 52,
                decoration: BoxDecoration(
                  color: AppTheme.bgDark,
                  shape: BoxShape.circle,
                  border: Border.all(color: Colors.white.withValues(alpha: 0.04)),
                ),
                child: Center(
                  child: Container(
                    width: 12,
                    height: 12,
                    decoration: BoxDecoration(
                      color: Colors.white.withValues(alpha: 0.1),
                      shape: BoxShape.circle,
                    ),
                  ),
                ),
              ),
            ),

            // DIREITA
            Align(
              alignment: Alignment.centerRight,
              child: SizedBox(
                width: 60,
                height: 60,
                child: _buildKey(
                  dir: 'R',
                  icon: Icons.keyboard_arrow_right_rounded,
                  borderRadius: const BorderRadius.horizontal(right: Radius.circular(12)),
                ),
              ),
            ),

            // BAIXO (Ré)
            Align(
              alignment: Alignment.bottomCenter,
              child: SizedBox(
                width: 60,
                height: 60,
                child: _buildKey(
                  dir: 'B',
                  icon: Icons.keyboard_arrow_down_rounded,
                  borderRadius: const BorderRadius.vertical(bottom: Radius.circular(12)),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
