import 'package:shared_preferences/shared_preferences.dart';
import '../models/bot_models.dart';

class PreferencesService {
  static const String _configKey = 'combat_bot_config_v1';

  /// Carrega as configurações salvas ou retorna a padrão
  static Future<BotConfig> loadConfig() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final jsonStr = prefs.getString(_configKey);
      if (jsonStr != null && jsonStr.isNotEmpty) {
        return BotConfig.deserialize(jsonStr);
      }
    } catch (_) {
      // Retorna padrão em caso de erro
    }
    return BotConfig();
  }

  /// Salva as configurações de forma persistente
  static Future<bool> saveConfig(BotConfig config) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      return await prefs.setString(_configKey, config.serialize());
    } catch (_) {
      return false;
    }
  }

  /// Restaura as configurações originais de fábrica
  static Future<BotConfig> resetToDefaults() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove(_configKey);
    } catch (_) {}
    return BotConfig();
  }
}
