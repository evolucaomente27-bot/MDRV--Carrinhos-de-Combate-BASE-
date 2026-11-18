import 'package:flutter/material.dart';
import '../models/bot_models.dart';
import '../services/bot_communication_service.dart';

class SettingsDialog extends StatefulWidget {
  final BotConfig config;
  final BotCommunicationService service;

  const SettingsDialog({
    super.key,
    required this.config,
    required this.service,
  });

  @override
  State<SettingsDialog> createState() => _SettingsDialogState();
}

class _SettingsDialogState extends State<SettingsDialog> {
  late TextEditingController _ipController;
  late ConnectionType _selectedType;
  late int _turn90Ms;
  late int _speedPct;
  late double _deadzone;
  late int _updateRate;

  @override
  void initState() {
    super.initState();
    _ipController = TextEditingController(text: widget.config.robotIp);
    _selectedType = widget.service.connectionType;
    _turn90Ms = widget.config.turn90TimeMs;
    _speedPct = widget.config.speedPercent;
    _deadzone = widget.config.deadzone;
    _updateRate = widget.config.updateIntervalMs;
  }

  @override
  void dispose() {
    _ipController.dispose();
    super.dispose();
  }

  void _saveSettings() {
    widget.config.robotIp = _ipController.text.trim();
    widget.config.turn90TimeMs = _turn90Ms;
    widget.config.speedPercent = _speedPct;
    widget.config.deadzone = _deadzone;
    widget.config.updateIntervalMs = _updateRate;

    widget.service.connect(type: _selectedType);
    Navigator.of(context).pop();
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: const Color(0xFF161928),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: const BorderSide(color: Color(0xFF334155)),
      ),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    '⚙️ CONFIGURAÇÕES',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w900,
                      color: Colors.white,
                      letterSpacing: 1.2,
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.close, color: Color(0xFF94A3B8), size: 20),
                    onPressed: () => Navigator.of(context).pop(),
                  ),
                ],
              ),
              const Divider(color: Color(0xFF334155)),
              const SizedBox(height: 10),

              // TIPO DE CONEXÃO
              const Text('Protocolo de Conexão:', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Color(0xFF94A3B8))),
              const SizedBox(height: 6),
              DropdownButtonFormField<ConnectionType>(
                initialValue: _selectedType,
                dropdownColor: const Color(0xFF1E2235),
                style: const TextStyle(color: Colors.white, fontSize: 13),
                decoration: InputDecoration(
                  filled: true,
                  fillColor: const Color(0xFF1E2235),
                  contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: const BorderSide(color: Color(0xFF475569))),
                ),
                items: const [
                  DropdownMenuItem(
                    value: ConnectionType.webSocket,
                    child: Text('⚡ WebSockets (ESP32 V2 - Ultra-Rápido <5ms)'),
                  ),
                  DropdownMenuItem(
                    value: ConnectionType.http,
                    child: Text('🌐 HTTP REST (ESP32 V1 e Fallback)'),
                  ),
                  DropdownMenuItem(
                    value: ConnectionType.simulation,
                    child: Text('🎮 Simulação Local (Sem Robô)'),
                  ),
                ],
                onChanged: (val) {
                  if (val != null) setState(() => _selectedType = val);
                },
              ),

              const SizedBox(height: 14),

              // IP DO ROBÔ
              const Text('Endereço IP do Robô:', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Color(0xFF94A3B8))),
              const SizedBox(height: 6),
              TextField(
                controller: _ipController,
                style: const TextStyle(color: Colors.white, fontSize: 13, fontFamily: 'monospace'),
                decoration: InputDecoration(
                  filled: true,
                  fillColor: const Color(0xFF1E2235),
                  hintText: '192.168.4.1',
                  hintStyle: const TextStyle(color: Color(0xFF64748B)),
                  contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: const BorderSide(color: Color(0xFF475569))),
                ),
              ),

              const SizedBox(height: 14),

              // CALIBRAÇÃO GIRO 90°
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('Tempo do Giro 90°:', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Color(0xFF94A3B8))),
                  Text('$_turn90Ms ms', style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w900, color: Color(0xFF38BDF8))),
                ],
              ),
              Slider(
                value: _turn90Ms.toDouble(),
                min: 150,
                max: 500,
                divisions: 35,
                activeColor: const Color(0xFF38BDF8),
                inactiveColor: const Color(0xFF334155),
                onChanged: (v) => setState(() => _turn90Ms = v.round()),
              ),

              // POTÊNCIA MÁXIMA
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('Potência Máxima dos Motores:', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Color(0xFF94A3B8))),
                  Text('$_speedPct%', style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w900, color: Color(0xFF00E676))),
                ],
              ),
              Slider(
                value: _speedPct.toDouble(),
                min: 50,
                max: 100,
                divisions: 10,
                activeColor: const Color(0xFF00E676),
                inactiveColor: const Color(0xFF334155),
                onChanged: (v) => setState(() => _speedPct = v.round()),
              ),

              // ZONA MORTA (DEADZONE)
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('Zona Morta do Analógico:', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Color(0xFF94A3B8))),
                  Text('${(_deadzone * 100).round()}%', style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w900, color: Color(0xFFF59E0B))),
                ],
              ),
              Slider(
                value: _deadzone,
                min: 0.04,
                max: 0.20,
                divisions: 16,
                activeColor: const Color(0xFFF59E0B),
                inactiveColor: const Color(0xFF334155),
                onChanged: (v) => setState(() => _deadzone = v),
              ),

              const SizedBox(height: 16),

              // BOTÃO SALVAR
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF0EA5E9),
                    padding: const EdgeInsets.symmetric(vertical: 12),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                  ),
                  onPressed: _saveSettings,
                  child: const Text(
                    'SALVAR E APLICAR',
                    style: TextStyle(fontSize: 13, fontWeight: FontWeight.w900, letterSpacing: 1.2, color: Colors.white),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
