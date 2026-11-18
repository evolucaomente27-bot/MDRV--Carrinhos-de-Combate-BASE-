import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class AnalogJoystick extends StatefulWidget {
  final double radius;
  final double stickRadius;
  final bool isTurbo;
  final Function(double normV, double normW) onChanged;
  final VoidCallback onReleased;

  const AnalogJoystick({
    super.key,
    this.radius = 110,
    this.stickRadius = 40,
    this.isTurbo = false,
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

  @override
  void initState() {
    super.initState();
    _animController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 150),
    )..addListener(() {
        setState(() {
          _stickPosition = _releaseAnimation.value;
        });
      });
  }

  void _onPointerDown(PointerDownEvent event, BoxConstraints constraints) {
    _animController.stop();
    HapticFeedback.lightImpact();
    _updateStick(event.localPosition, constraints);
  }

  void _onPointerMove(PointerMoveEvent event, BoxConstraints constraints) {
    _updateStick(event.localPosition, constraints);
  }

  void _onPointerUp(PointerUpEvent event) {
    HapticFeedback.selectionClick();
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

    final maxDistance = widget.radius - (widget.stickRadius * 0.4);

    if (distance <= maxDistance) {
      _stickPosition = delta;
    } else {
      // Limita na circunferência
      _stickPosition = Offset(
        (delta.dx / distance) * maxDistance,
        (delta.dy / distance) * maxDistance,
      );
      HapticFeedback.selectionClick();
    }

    // Normaliza (-1.0 a +1.0)
    // Invertemos Y porque para cima no Flutter Y é negativo
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
                painter: _JoystickPainter(
                  stickPosition: _stickPosition,
                  radius: widget.radius,
                  stickRadius: widget.stickRadius,
                  isTurbo: widget.isTurbo,
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}

class _JoystickPainter extends CustomPainter {
  final Offset stickPosition;
  final double radius;
  final double stickRadius;
  final bool isTurbo;

  _JoystickPainter({
    required this.stickPosition,
    required this.radius,
    required this.stickRadius,
    required this.isTurbo,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);

    // 1. Base Circular Externa
    final baseGradient = RadialGradient(
      colors: [
        const Color(0xFF1E2235),
        const Color(0xFF121420),
        const Color(0xFF090A10),
      ],
      stops: const [0.0, 0.7, 1.0],
    );

    final basePaint = Paint()
      ..shader = baseGradient.createShader(Rect.fromCircle(center: center, radius: radius))
      ..style = PaintingStyle.fill;
    canvas.drawCircle(center, radius, basePaint);

    // Anel Metálico com Borda
    final borderPaint = Paint()
      ..color = isTurbo ? const Color(0xFFFF3D00) : const Color(0xFF334155)
      ..strokeWidth = isTurbo ? 3.5 : 2.5
      ..style = PaintingStyle.stroke;
    canvas.drawCircle(center, radius, borderPaint);

    // Retículo / Mira Interna
    final crossPaint = Paint()
      ..color = const Color(0x3394A3B8)
      ..strokeWidth = 1.2
      ..style = PaintingStyle.stroke;
    canvas.drawCircle(center, radius * 0.6, crossPaint);
    canvas.drawLine(Offset(center.dx - radius * 0.8, center.dy), Offset(center.dx + radius * 0.8, center.dy), crossPaint);
    canvas.drawLine(Offset(center.dx, center.dy - radius * 0.8), Offset(center.dx, center.dy + radius * 0.8), crossPaint);

    // 2. O Manípulo (Thumbstick)
    final currentStickPos = center + stickPosition;

    // Sombra do manípulo
    canvas.drawCircle(
      currentStickPos + const Offset(0, 4),
      stickRadius,
      Paint()
        ..color = Colors.black.withValues(alpha: 0.5)
        ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 6),
    );

    // Gradiente do Manípulo (Verde Neon ou Laranja Fogo no Turbo)
    final stickGradient = RadialGradient(
      center: const Alignment(-0.3, -0.3),
      colors: isTurbo
          ? [
              const Color(0xFFFF9100),
              const Color(0xFFFF3D00),
              const Color(0xFFB71C1C),
            ]
          : [
              const Color(0xFF69F0AE),
              const Color(0xFF00E676),
              const Color(0xFF007E33),
            ],
    );

    final stickPaint = Paint()
      ..shader = stickGradient.createShader(Rect.fromCircle(center: currentStickPos, radius: stickRadius))
      ..style = PaintingStyle.fill;
    canvas.drawCircle(currentStickPos, stickRadius, stickPaint);

    // Borda do Manípulo
    final stickBorder = Paint()
      ..color = Colors.white.withValues(alpha: 0.7)
      ..strokeWidth = 2.0
      ..style = PaintingStyle.stroke;
    canvas.drawCircle(currentStickPos, stickRadius, stickBorder);

    // Miolo central
    final innerCenterPaint = Paint()
      ..color = Colors.black.withValues(alpha: 0.25)
      ..style = PaintingStyle.fill;
    canvas.drawCircle(currentStickPos, stickRadius * 0.4, innerCenterPaint);
  }

  @override
  bool shouldRepaint(covariant _JoystickPainter oldDelegate) {
    return oldDelegate.stickPosition != stickPosition ||
        oldDelegate.isTurbo != isTurbo;
  }
}
