import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../theme/app_theme.dart';

class AnalogJoystick extends StatefulWidget {
  final double radius;
  final double stickRadius;
  final bool isTurbo;
  final Color? primaryColor;
  final Color? accentColor;
  final Function(double normV, double normW) onChanged;
  final VoidCallback onReleased;

  const AnalogJoystick({
    super.key,
    this.radius = 110,
    this.stickRadius = 38,
    this.isTurbo = false,
    this.primaryColor,
    this.accentColor,
    required this.onChanged,
    required this.onReleased,
  });

  @override
  State<AnalogJoystick> createState() => _AnalogJoystickState();
}

class _AnalogJoystickState extends State<AnalogJoystick> with SingleTickerProviderStateMixin {
  Offset _stickPosition = Offset.zero;
  late AnimationController _animController;
  late Animation<Offset> _releaseAnimation;
  bool _isInteracting = false;

  @override
  void initState() {
    super.initState();
    _animController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 140),
    )..addListener(() {
        setState(() {
          _stickPosition = _releaseAnimation.value;
        });
      });
  }

  void _onPointerDown(PointerDownEvent event, BoxConstraints constraints) {
    _animController.stop();
    HapticFeedback.lightImpact();
    setState(() => _isInteracting = true);
    _updateStick(event.localPosition, constraints);
  }

  void _onPointerMove(PointerMoveEvent event, BoxConstraints constraints) {
    _updateStick(event.localPosition, constraints);
  }

  void _onPointerUp(PointerUpEvent event) {
    HapticFeedback.selectionClick();
    setState(() => _isInteracting = false);

    _releaseAnimation = Tween<Offset>(
      begin: _stickPosition,
      end: Offset.zero,
    ).animate(CurvedAnimation(
      parent: _animController,
      curve: Curves.easeOutCubic,
    ));

    _animController.forward(from: 0.0);
    widget.onChanged(0.0, 0.0);
    widget.onReleased();
  }

  void _updateStick(Offset localPos, BoxConstraints constraints) {
    final center = Offset(constraints.maxWidth / 2, constraints.maxHeight / 2);
    final delta = localPos - center;
    final distance = delta.distance;

    final maxDistance = widget.radius - (widget.stickRadius * 0.45);

    if (distance <= maxDistance) {
      _stickPosition = delta;
    } else {
      _stickPosition = Offset(
        (delta.dx / distance) * maxDistance,
        (delta.dy / distance) * maxDistance,
      );
      HapticFeedback.selectionClick();
    }

    final normV = -(_stickPosition.dy / maxDistance).clamp(-1.0, 1.0);
    final normW = (_stickPosition.dx / maxDistance).clamp(-1.0, 1.0);

    widget.onChanged(normV, normW);
    setState(() {});
  }

  @override
  void dispose() {
    _animController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final totalSize = widget.radius * 2;

    return Center(
      child: LayoutBuilder(
        builder: (context, constraints) {
          return Listener(
            onPointerDown: (e) => _onPointerDown(e, constraints),
            onPointerMove: (e) => _onPointerMove(e, constraints),
            onPointerUp: _onPointerUp,
            onPointerCancel: (_) => _onPointerUp(PointerUpEvent()),
            child: SizedBox(
              width: totalSize,
              height: totalSize,
              child: CustomPaint(
                painter: _CleanJoystickPainter(
                  stickPosition: _stickPosition,
                  radius: widget.radius,
                  stickRadius: widget.stickRadius,
                  isTurbo: widget.isTurbo,
                  isInteracting: _isInteracting,
                  primaryColor: widget.primaryColor ?? AppTheme.primaryBlue,
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}

class _CleanJoystickPainter extends CustomPainter {
  final Offset stickPosition;
  final double radius;
  final double stickRadius;
  final bool isTurbo;
  final bool isInteracting;
  final Color primaryColor;

  _CleanJoystickPainter({
    required this.stickPosition,
    required this.radius,
    required this.stickRadius,
    required this.isTurbo,
    required this.isInteracting,
    required this.primaryColor,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);

    // 1. BASE CIRCULAR ULTRA-LIMPA (Matte Dark)
    final basePaint = Paint()
      ..color = const Color(0xFF11141C)
      ..style = PaintingStyle.fill;
    canvas.drawCircle(center, radius, basePaint);

    // Borda hairline ultra-sutil
    final outerRingPaint = Paint()
      ..color = isTurbo
          ? AppTheme.violetTurbo.withValues(alpha: 0.5)
          : isInteracting
              ? primaryColor.withValues(alpha: 0.3)
              : Colors.white.withValues(alpha: 0.06)
      ..strokeWidth = 1.0
      ..style = PaintingStyle.stroke;
    canvas.drawCircle(center, radius, outerRingPaint);

    // Ponto central de repouso mínimo
    canvas.drawCircle(
      center,
      3.0,
      Paint()..color = Colors.white.withValues(alpha: 0.12),
    );

    // 2. MANÍPULO / THUMB PUCK (Elegante e ergonômico)
    final currentStickPos = center + stickPosition;

    // Sombra suave
    canvas.drawCircle(
      currentStickPos + const Offset(0, 3),
      stickRadius,
      Paint()
        ..color = Colors.black.withValues(alpha: 0.35)
        ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 8),
    );

    // Corpo do Manípulo
    final Color puckColor = isTurbo
        ? AppTheme.violetTurbo
        : isInteracting
            ? primaryColor
            : const Color(0xFF1E2432);

    final puckPaint = Paint()
      ..color = puckColor
      ..style = PaintingStyle.fill;
    canvas.drawCircle(currentStickPos, stickRadius, puckPaint);

    // Borda com brilho sutil
    final puckBorder = Paint()
      ..color = Colors.white.withValues(alpha: isInteracting ? 0.45 : 0.15)
      ..strokeWidth = 1.2
      ..style = PaintingStyle.stroke;
    canvas.drawCircle(currentStickPos, stickRadius, puckBorder);

    // Núcleo central mínimo
    canvas.drawCircle(
      currentStickPos,
      4.0,
      Paint()..color = Colors.white.withValues(alpha: isInteracting ? 0.9 : 0.35),
    );
  }

  @override
  bool shouldRepaint(covariant _CleanJoystickPainter oldDelegate) {
    return oldDelegate.stickPosition != stickPosition ||
        oldDelegate.isTurbo != isTurbo ||
        oldDelegate.isInteracting != isInteracting ||
        oldDelegate.primaryColor != primaryColor;
  }
}
