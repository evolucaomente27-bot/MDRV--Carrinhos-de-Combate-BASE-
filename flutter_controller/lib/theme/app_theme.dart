import 'package:flutter/material.dart';
import '../models/bot_models.dart';

/// Sistema de Design Profissional e Dinâmico do Combat Bot Controller
class AppTheme {
  // Cores de Base Sólidas (Carbono & Obsidiana)
  static const Color bgDark = Color(0xFF090D16);
  static const Color surfaceCard = Color(0xFF131A26);
  static const Color surfaceCardElevated = Color(0xFF1A2232);
  static const Color surfaceInput = Color(0xFF0F1520);

  // Bordas e Divisores
  static const Color borderSubtle = Color(0xFF222D3D);
  static const Color borderLight = Color(0xFF334155);

  // Status Globais
  static const Color emeraldSafe = Color(0xFF10B981);
  static const Color amberWarning = Color(0xFFF59E0B);
  static const Color crimsonDanger = Color(0xFFEF4444);
  static const Color violetTurbo = Color(0xFF8B5CF6);

  // Cores Primárias Padrão (Compatibilidade)
  static const Color primaryBlue = Color(0xFF3B82F6);
  static const Color primaryBlueDark = Color(0xFF1D4ED8);
  static const Color accentCyan = Color(0xFF06B6D4);

  // Tipografia
  static const Color textPrimary = Color(0xFFF8FAFC);
  static const Color textSecondary = Color(0xFF94A3B8);
  static const Color textMuted = Color(0xFF64748B);

  /// Retorna as cores dinâmicas para o tema selecionado
  static Color getPrimary(AppColorTheme theme) => theme.primaryColor;
  static Color getAccent(AppColorTheme theme) => theme.accentColor;

  // Decoração de Cartão Padrão
  static BoxDecoration cardDecoration({
    Color? borderColor,
    Color? backgroundColor,
    double borderRadius = 12.0,
  }) {
    return BoxDecoration(
      color: backgroundColor ?? surfaceCard,
      borderRadius: BorderRadius.circular(borderRadius),
      border: Border.all(
        color: borderColor ?? borderSubtle,
        width: 1.0,
      ),
      boxShadow: [
        BoxShadow(
          color: Colors.black.withValues(alpha: 0.25),
          offset: const Offset(0, 4),
          blurRadius: 12,
        ),
      ],
    );
  }

  /// Gera ThemeData dinâmico a partir do AppColorTheme escolhido
  static ThemeData buildTheme(AppColorTheme theme) {
    final primary = theme.primaryColor;
    final accent = theme.accentColor;

    return ThemeData.dark().copyWith(
      scaffoldBackgroundColor: bgDark,
      primaryColor: primary,
      colorScheme: ColorScheme.dark(
        primary: primary,
        secondary: accent,
        surface: surfaceCard,
        error: crimsonDanger,
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: bgDark,
        elevation: 0,
        centerTitle: false,
        scrolledUnderElevation: 0,
      ),
      sliderTheme: SliderThemeData(
        activeTrackColor: primary,
        thumbColor: primary,
        inactiveTrackColor: borderSubtle,
        overlayColor: primary.withValues(alpha: 0.2),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primary,
          foregroundColor: Colors.white,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
        ),
      ),
      textTheme: const TextTheme(
        headlineMedium: TextStyle(
          color: textPrimary,
          fontWeight: FontWeight.w700,
          letterSpacing: 0.5,
        ),
        titleMedium: TextStyle(
          color: textPrimary,
          fontWeight: FontWeight.w600,
          letterSpacing: 0.3,
        ),
        bodyMedium: TextStyle(
          color: textSecondary,
          fontSize: 13,
        ),
      ),
    );
  }

  // Compatibilidade com código anterior
  static ThemeData get darkTheme => buildTheme(AppColorTheme.obsidianBlue);
}
