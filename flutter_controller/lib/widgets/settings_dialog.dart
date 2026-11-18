import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../models/bot_models.dart';
import '../services/bot_communication_service.dart';
import '../services/preferences_service.dart';
import '../theme/app_theme.dart';

class SettingsDialog extends StatefulWidget {
  final BotConfig config;
  final BotCommunicationService service;
  final VoidCallback onConfigChanged;

  const SettingsDialog({
    super.key,
    required this.config,
    required this.service,
    required this.onConfigChanged,
  });

  @override
  State<SettingsDialog> createState() => _SettingsDialogState();
}

class _SettingsDialogState extends State<SettingsDialog> with SingleTickerProviderStateMixin {
  late TabController _tabController;

  // Estados locais temporários
  late TextEditingController _ipController;
  late ConnectionType _selectedType;
  late AppColorTheme _selectedTheme;
  late Handedness _handedness;
  late bool _invertY;
  late bool _invertX;
  late StickCurve _stickCurve;
  late double _joystickRadius;
  late double _deadzone;
  late int _steeringTrim;
  late int _speedPct;
  late int _turboSpeedPct;
  late bool _smoothAcceleration;
  late int _turn90Ms;
  late int _updateIntervalMs;
  late List<TacticalButtonConfig> _tacticalButtons;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 5, vsync: this);

    final cfg = widget.config;
    _ipController = TextEditingController(text: cfg.robotIp);
    _selectedType = widget.service.connectionType;
    _selectedTheme = cfg.colorTheme;
    _handedness = cfg.handedness;
    _invertY = cfg.invertThrottleY;
    _invertX = cfg.invertSteeringX;
    _stickCurve = cfg.stickCurve;
    _joystickRadius = cfg.joystickRadius;
    _deadzone = cfg.deadzone;
    _steeringTrim = cfg.steeringTrim;
    _speedPct = cfg.speedPercent;
    _turboSpeedPct = cfg.turboSpeedPercent;
    _smoothAcceleration = cfg.smoothAcceleration;
    _turn90Ms = cfg.turn90TimeMs;
    _updateIntervalMs = cfg.updateIntervalMs;

    _tacticalButtons = cfg.tacticalButtons
        .map((b) => TacticalButtonConfig(
              actionType: b.actionType,
              customTitle: b.customTitle,
              customCmd: b.customCmd,
              durationMs: b.durationMs,
            ))
        .toList();
  }

  @override
  void dispose() {
    _tabController.dispose();
    _ipController.dispose();
    super.dispose();
  }

  Future<void> _saveSettings() async {
    final cfg = widget.config;
    cfg.robotIp = _ipController.text.trim();
    cfg.colorTheme = _selectedTheme;
    cfg.handedness = _handedness;
    cfg.invertThrottleY = _invertY;
    cfg.invertSteeringX = _invertX;
    cfg.stickCurve = _stickCurve;
    cfg.joystickRadius = _joystickRadius;
    cfg.deadzone = _deadzone;
    cfg.steeringTrim = _steeringTrim;
    cfg.speedPercent = _speedPct;
    cfg.turboSpeedPercent = _turboSpeedPct;
    cfg.smoothAcceleration = _smoothAcceleration;
    cfg.turn90TimeMs = _turn90Ms;
    cfg.updateIntervalMs = _updateIntervalMs;
    cfg.tacticalButtons = _tacticalButtons;

    await PreferencesService.saveConfig(cfg);
    widget.service.connect(type: _selectedType);
    widget.onConfigChanged();

    if (mounted) {
      Navigator.of(context).pop();
    }
  }

  Future<void> _resetDefaults() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: AppTheme.surfaceCard,
        title: const Text('Restaurar Padrões?'),
        content: const Text('Todas as personalizações de botões, cores e sensibilidade serão redefinidas para o padrão.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(false),
            child: const Text('Cancelar', style: TextStyle(color: AppTheme.textSecondary)),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: AppTheme.crimsonDanger),
            onPressed: () => Navigator.of(ctx).pop(true),
            child: const Text('Restaurar'),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      final defaultCfg = await PreferencesService.resetToDefaults();
      setState(() {
        _ipController.text = defaultCfg.robotIp;
        _selectedTheme = defaultCfg.colorTheme;
        _handedness = defaultCfg.handedness;
        _invertY = defaultCfg.invertThrottleY;
        _invertX = defaultCfg.invertSteeringX;
        _stickCurve = defaultCfg.stickCurve;
        _joystickRadius = defaultCfg.joystickRadius;
        _deadzone = defaultCfg.deadzone;
        _steeringTrim = defaultCfg.steeringTrim;
        _speedPct = defaultCfg.speedPercent;
        _turboSpeedPct = defaultCfg.turboSpeedPercent;
        _smoothAcceleration = defaultCfg.smoothAcceleration;
        _turn90Ms = defaultCfg.turn90TimeMs;
        _updateIntervalMs = defaultCfg.updateIntervalMs;
        _tacticalButtons = defaultCfg.tacticalButtons;
      });
      HapticFeedback.heavyImpact();
    }
  }

  Widget _buildThemeTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Selecione a identidade visual do controle:',
            style: TextStyle(fontSize: 12, color: AppTheme.textSecondary),
          ),
          const SizedBox(height: 12),
          ...AppColorTheme.values.map((theme) {
            final isSelected = _selectedTheme == theme;
            return Container(
              margin: const EdgeInsets.only(bottom: 8),
              decoration: BoxDecoration(
                color: isSelected ? theme.primaryColor.withValues(alpha: 0.15) : AppTheme.surfaceInput,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(
                  color: isSelected ? theme.primaryColor : AppTheme.borderSubtle,
                  width: isSelected ? 1.5 : 1.0,
                ),
              ),
              child: ListTile(
                contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 2),
                leading: Container(
                  width: 24,
                  height: 24,
                  decoration: BoxDecoration(
                    color: theme.primaryColor,
                    shape: BoxShape.circle,
                    boxShadow: [
                      BoxShadow(color: theme.primaryColor.withValues(alpha: 0.5), blurRadius: 8),
                    ],
                  ),
                ),
                title: Text(
                  theme.label,
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: isSelected ? FontWeight.w800 : FontWeight.w500,
                    color: isSelected ? Colors.white : AppTheme.textPrimary,
                  ),
                ),
                trailing: isSelected
                    ? Icon(Icons.check_circle_rounded, color: theme.primaryColor, size: 20)
                    : null,
                onTap: () {
                  HapticFeedback.selectionClick();
                  setState(() => _selectedTheme = theme);
                },
              ),
            );
          }),
        ],
      ),
    );
  }

  Widget _buildErgonomicsTab() {
    final primaryColor = _selectedTheme.primaryColor;

    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // 1. MÃO DO CONTROLE (DESTRO VS CANHOTO)
          const Text('Orientação das Mãos (Modo Console):', style: TextStyle(fontSize: 12, color: AppTheme.textSecondary)),
          const SizedBox(height: 8),
          Row(
            children: Handedness.values.map((h) {
              final isSel = _handedness == h;
              return Expanded(
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 4),
                  child: OutlinedButton(
                    style: OutlinedButton.styleFrom(
                      backgroundColor: isSel ? primaryColor.withValues(alpha: 0.2) : AppTheme.surfaceInput,
                      side: BorderSide(color: isSel ? primaryColor : AppTheme.borderSubtle),
                      padding: const EdgeInsets.symmetric(vertical: 10),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                    ),
                    onPressed: () => setState(() => _handedness = h),
                    child: Text(
                      h.label,
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 11,
                        fontWeight: isSel ? FontWeight.w800 : FontWeight.w500,
                        color: isSel ? Colors.white : AppTheme.textSecondary,
                      ),
                    ),
                  ),
                ),
              );
            }).toList(),
          ),

          const SizedBox(height: 14),

          // 2. INVERSÃO DE EIXOS
          SwitchListTile(
            contentPadding: EdgeInsets.zero,
            title: const Text('Inverter Avanço / Ré (Eixo Y)', style: TextStyle(fontSize: 12, color: AppTheme.textPrimary)),
            subtitle: const Text('Puxar para trás avança, empurrar dá ré', style: TextStyle(fontSize: 10, color: AppTheme.textMuted)),
            value: _invertY,
            activeThumbColor: primaryColor,
            onChanged: (val) => setState(() => _invertY = val),
          ),

          SwitchListTile(
            contentPadding: EdgeInsets.zero,
            title: const Text('Inverter Esquerda / Direita (Eixo X)', style: TextStyle(fontSize: 12, color: AppTheme.textPrimary)),
            subtitle: const Text('Inverte o sentido de giro da direção', style: TextStyle(fontSize: 10, color: AppTheme.textMuted)),
            value: _invertX,
            activeThumbColor: primaryColor,
            onChanged: (val) => setState(() => _invertX = val),
          ),

          const SizedBox(height: 10),

          // 3. CURVA DO ANALÓGICO
          const Text('Curva de Sensibilidade (Expo):', style: TextStyle(fontSize: 12, color: AppTheme.textSecondary)),
          const SizedBox(height: 6),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10),
            decoration: BoxDecoration(
              color: AppTheme.surfaceInput,
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: AppTheme.borderSubtle),
            ),
            child: DropdownButtonHideUnderline(
              child: DropdownButton<StickCurve>(
                value: _stickCurve,
                dropdownColor: AppTheme.surfaceCardElevated,
                isExpanded: true,
                style: const TextStyle(color: AppTheme.textPrimary, fontSize: 12),
                items: StickCurve.values.map((curve) {
                  return DropdownMenuItem(value: curve, child: Text(curve.label));
                }).toList(),
                onChanged: (val) {
                  if (val != null) setState(() => _stickCurve = val);
                },
              ),
            ),
          ),

          const SizedBox(height: 14),

          // 4. RAIO DO ANALÓGICO
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Tamanho do Analógico:', style: TextStyle(fontSize: 12, color: AppTheme.textSecondary)),
              Text('${_joystickRadius.round()} px', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: primaryColor)),
            ],
          ),
          Slider(
            value: _joystickRadius,
            min: 85,
            max: 135,
            divisions: 10,
            activeColor: primaryColor,
            onChanged: (val) => setState(() => _joystickRadius = val),
          ),

          // 5. ZONA MORTA
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Zona Morta (Deadzone):', style: TextStyle(fontSize: 12, color: AppTheme.textSecondary)),
              Text('${(_deadzone * 100).round()}%', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: primaryColor)),
            ],
          ),
          Slider(
            value: _deadzone,
            min: 0.02,
            max: 0.25,
            divisions: 23,
            activeColor: primaryColor,
            onChanged: (val) => setState(() => _deadzone = val),
          ),
        ],
      ),
    );
  }

  Widget _buildMotorsTab() {
    final primaryColor = _selectedTheme.primaryColor;

    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // 1. TRIM DE DIREÇÃO
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Trim de Direção (Alinhamento Reto):', style: TextStyle(fontSize: 12, color: AppTheme.textSecondary)),
              Row(
                children: [
                  Text(
                    _steeringTrim == 0
                        ? '0% (Neutro)'
                        : _steeringTrim > 0
                            ? '+$_steeringTrim% (Comp. DIR)'
                            : '$_steeringTrim% (Comp. ESQ)',
                    style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppTheme.amberWarning, fontFamily: 'monospace'),
                  ),
                  if (_steeringTrim != 0) ...[
                    IconButton(
                      icon: const Icon(Icons.refresh_rounded, size: 16, color: AppTheme.textMuted),
                      tooltip: 'Zerar Trim',
                      padding: EdgeInsets.zero,
                      constraints: const BoxConstraints(),
                      onPressed: () => setState(() => _steeringTrim = 0),
                    ),
                  ],
                ],
              ),
            ],
          ),
          const Text('Compensa robôs que puxam para o lado por diferença de motores', style: TextStyle(fontSize: 9.5, color: AppTheme.textMuted)),
          Slider(
            value: _steeringTrim.toDouble(),
            min: -25,
            max: 25,
            divisions: 50,
            activeColor: AppTheme.amberWarning,
            inactiveColor: AppTheme.borderSubtle,
            onChanged: (val) => setState(() => _steeringTrim = val.round()),
          ),

          const SizedBox(height: 12),

          // 2. TETO DE POTÊNCIA NORMAL
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Teto de Potência Normal:', style: TextStyle(fontSize: 12, color: AppTheme.textSecondary)),
              Text('$_speedPct%', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: primaryColor)),
            ],
          ),
          Slider(
            value: _speedPct.toDouble(),
            min: 30,
            max: 100,
            divisions: 14,
            activeColor: primaryColor,
            onChanged: (val) => setState(() => _speedPct = val.round()),
          ),

          // 3. TETO DO OVERDRIVE TURBO
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Potência do Overdrive Turbo:', style: TextStyle(fontSize: 12, color: AppTheme.textSecondary)),
              Text('$_turboSpeedPct%', style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppTheme.violetTurbo)),
            ],
          ),
          Slider(
            value: _turboSpeedPct.toDouble(),
            min: 80,
            max: 100,
            divisions: 4,
            activeColor: AppTheme.violetTurbo,
            onChanged: (val) => setState(() => _turboSpeedPct = val.round()),
          ),

          // 4. RAMPA DE ACELERAÇÃO SUAVE
          SwitchListTile(
            contentPadding: EdgeInsets.zero,
            title: const Text('Rampa de Aceleração Suave (Anti-Derrapagem)', style: TextStyle(fontSize: 12, color: AppTheme.textPrimary)),
            subtitle: const Text('Evita trancos violentos e derrapagens ao acelerar do zero', style: TextStyle(fontSize: 10, color: AppTheme.textMuted)),
            value: _smoothAcceleration,
            activeThumbColor: primaryColor,
            onChanged: (val) => setState(() => _smoothAcceleration = val),
          ),
        ],
      ),
    );
  }

  Widget _buildTacticalButtonsTab() {
    final primaryColor = _selectedTheme.primaryColor;

    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Personalize as ações dos 4 slots de botões do painel:',
            style: TextStyle(fontSize: 11.5, color: AppTheme.textSecondary),
          ),
          const SizedBox(height: 10),
          ...List.generate(_tacticalButtons.length, (idx) {
            final btn = _tacticalButtons[idx];

            return Container(
              margin: const EdgeInsets.only(bottom: 12),
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: AppTheme.surfaceInput,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: AppTheme.borderSubtle),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(4),
                        decoration: BoxDecoration(
                          color: primaryColor.withValues(alpha: 0.15),
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: Text(
                          'SLOT ${idx + 1}',
                          style: TextStyle(fontSize: 9.5, fontWeight: FontWeight.w800, color: primaryColor),
                        ),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: DropdownButtonHideUnderline(
                          child: DropdownButton<TacticalActionType>(
                            value: btn.actionType,
                            dropdownColor: AppTheme.surfaceCardElevated,
                            isExpanded: true,
                            style: const TextStyle(color: AppTheme.textPrimary, fontSize: 12, fontWeight: FontWeight.w700),
                            items: TacticalActionType.values.map((act) {
                              return DropdownMenuItem(
                                value: act,
                                child: Row(
                                  children: [
                                    Icon(act.defaultIcon, size: 14, color: primaryColor),
                                    const SizedBox(width: 8),
                                    Text(act.defaultTitle),
                                  ],
                                ),
                              );
                            }).toList(),
                            onChanged: (newAct) {
                              if (newAct != null) {
                                setState(() {
                                  btn.actionType = newAct;
                                  btn.customTitle = newAct.defaultTitle;
                                  btn.customCmd = newAct.defaultCmd;
                                });
                              }
                            },
                          ),
                        ),
                      ),
                    ],
                  ),

                  const SizedBox(height: 8),

                  // TÍTULO PERSONALIZADO DO BOTÃO
                  TextFormField(
                    initialValue: btn.customTitle,
                    style: const TextStyle(color: AppTheme.textPrimary, fontSize: 11),
                    decoration: InputDecoration(
                      labelText: 'Nome no Botão',
                      labelStyle: const TextStyle(color: AppTheme.textMuted, fontSize: 11),
                      filled: true,
                      fillColor: AppTheme.surfaceCard,
                      contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                      enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(6),
                        borderSide: const BorderSide(color: AppTheme.borderSubtle),
                      ),
                    ),
                    onChanged: (val) => btn.customTitle = val,
                  ),

                  // SE FOR MANOBRA COM TEMPO
                  if (btn.actionType == TacticalActionType.turn90Left ||
                      btn.actionType == TacticalActionType.turn90Right ||
                      btn.actionType == TacticalActionType.turn180) ...[
                    const SizedBox(height: 6),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('Duração do Pulso:', style: TextStyle(fontSize: 10.5, color: AppTheme.textMuted)),
                        Text('${btn.durationMs} ms', style: const TextStyle(fontSize: 10.5, fontWeight: FontWeight.bold, color: AppTheme.accentCyan, fontFamily: 'monospace')),
                      ],
                    ),
                    Slider(
                      value: btn.durationMs.toDouble().clamp(100, 800),
                      min: 100,
                      max: 800,
                      divisions: 28,
                      activeColor: AppTheme.accentCyan,
                      onChanged: (val) => setState(() => btn.durationMs = val.round()),
                    ),
                  ],
                ],
              ),
            );
          }),
        ],
      ),
    );
  }

  Widget _buildNetworkTab() {
    final primaryColor = _selectedTheme.primaryColor;

    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Protocolo de Comunicação:', style: TextStyle(fontSize: 12, color: AppTheme.textSecondary)),
          const SizedBox(height: 6),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 2),
            decoration: BoxDecoration(
              color: AppTheme.surfaceInput,
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: AppTheme.borderSubtle),
            ),
            child: DropdownButtonHideUnderline(
              child: DropdownButton<ConnectionType>(
                value: _selectedType,
                dropdownColor: AppTheme.surfaceCardElevated,
                isExpanded: true,
                style: const TextStyle(color: AppTheme.textPrimary, fontSize: 12),
                items: const [
                  DropdownMenuItem(value: ConnectionType.webSocket, child: Text('WebSockets nativo ws:// (<5ms - ESP32 V2)')),
                  DropdownMenuItem(value: ConnectionType.http, child: Text('HTTP REST /drive (ESP32 V1)')),
                  DropdownMenuItem(value: ConnectionType.simulation, child: Text('Simulação Local (Bancada offline)')),
                ],
                onChanged: (val) {
                  if (val != null) setState(() => _selectedType = val);
                },
              ),
            ),
          ),

          const SizedBox(height: 12),

          TextField(
            controller: _ipController,
            style: const TextStyle(color: AppTheme.textPrimary, fontSize: 13, fontFamily: 'monospace'),
            decoration: InputDecoration(
              labelText: 'Endereço IP do Robô',
              labelStyle: const TextStyle(color: AppTheme.textMuted, fontSize: 12),
              filled: true,
              fillColor: AppTheme.surfaceInput,
              contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
              enabledBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(8),
                borderSide: const BorderSide(color: AppTheme.borderSubtle),
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(8),
                borderSide: BorderSide(color: primaryColor),
              ),
            ),
          ),

          const SizedBox(height: 6),

          Row(
            children: [
              ActionChip(
                label: const Text('ESP32 AP (192.168.4.1)', style: TextStyle(fontSize: 10, color: AppTheme.textSecondary)),
                backgroundColor: AppTheme.surfaceInput,
                side: const BorderSide(color: AppTheme.borderSubtle),
                onPressed: () => setState(() => _ipController.text = '192.168.4.1'),
              ),
              const SizedBox(width: 6),
              ActionChip(
                label: const Text('Localhost', style: TextStyle(fontSize: 10, color: AppTheme.textSecondary)),
                backgroundColor: AppTheme.surfaceInput,
                side: const BorderSide(color: AppTheme.borderSubtle),
                onPressed: () => setState(() => _ipController.text = '127.0.0.1'),
              ),
            ],
          ),

          const SizedBox(height: 12),

          // TAXA DE ATUALIZAÇÃO
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Taxa de Transmissão contínua:', style: TextStyle(fontSize: 12, color: AppTheme.textSecondary)),
              Text('$_updateIntervalMs ms (${(1000 / _updateIntervalMs).round()} FPS)',
                  style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: primaryColor, fontFamily: 'monospace')),
            ],
          ),
          Slider(
            value: _updateIntervalMs.toDouble(),
            min: 10,
            max: 50,
            divisions: 8,
            activeColor: primaryColor,
            onChanged: (val) => setState(() => _updateIntervalMs = val.round()),
          ),

          const SizedBox(height: 14),

          // BOTÃO RESTAURAR PADRÕES
          Center(
            child: TextButton.icon(
              style: TextButton.styleFrom(foregroundColor: AppTheme.crimsonDanger),
              icon: const Icon(Icons.restore_rounded, size: 16),
              label: const Text('Restaurar Padrões de Fábrica', style: TextStyle(fontSize: 11, fontWeight: FontWeight.w700)),
              onPressed: _resetDefaults,
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final primaryColor = _selectedTheme.primaryColor;

    return Dialog(
      backgroundColor: AppTheme.surfaceCard,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: const BorderSide(color: AppTheme.borderSubtle),
      ),
      insetPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 20),
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 520, maxHeight: 620),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              // CABEÇALHO COM FECHAR
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: [
                      Icon(Icons.tune_rounded, color: primaryColor, size: 20),
                      const SizedBox(width: 8),
                      const Text(
                        'CENTRAL DE PERSONALIZAÇÃO',
                        style: TextStyle(
                          fontSize: 13,
                          fontWeight: FontWeight.w800,
                          letterSpacing: 0.6,
                          color: AppTheme.textPrimary,
                        ),
                      ),
                    ],
                  ),
                  IconButton(
                    icon: const Icon(Icons.close_rounded, color: AppTheme.textMuted, size: 20),
                    padding: EdgeInsets.zero,
                    constraints: const BoxConstraints(),
                    onPressed: () => Navigator.of(context).pop(),
                  ),
                ],
              ),

              const SizedBox(height: 8),

              // ABAS DE PERSONALIZAÇÃO
              TabBar(
                controller: _tabController,
                isScrollable: true,
                tabAlignment: TabAlignment.start,
                indicatorColor: primaryColor,
                labelColor: primaryColor,
                unselectedLabelColor: AppTheme.textMuted,
                labelStyle: const TextStyle(fontSize: 11, fontWeight: FontWeight.w800),
                unselectedLabelStyle: const TextStyle(fontSize: 11, fontWeight: FontWeight.w500),
                tabs: const [
                  Tab(text: 'CORES'),
                  Tab(text: 'ERGONOMIA'),
                  Tab(text: 'MOTORES & TRIM'),
                  Tab(text: 'BOTÕES TÁTICOS'),
                  Tab(text: 'REDE'),
                ],
              ),

              const SizedBox(height: 8),

              // CORPO DAS ABAS
              Expanded(
                child: TabBarView(
                  controller: _tabController,
                  children: [
                    _buildThemeTab(),
                    _buildErgonomicsTab(),
                    _buildMotorsTab(),
                    _buildTacticalButtonsTab(),
                    _buildNetworkTab(),
                  ],
                ),
              ),

              const SizedBox(height: 10),
              const Divider(color: AppTheme.borderSubtle, height: 1),
              const SizedBox(height: 10),

              // BOTÕES SALVAR / CANCELAR
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton(
                      style: OutlinedButton.styleFrom(
                        foregroundColor: AppTheme.textSecondary,
                        side: const BorderSide(color: AppTheme.borderSubtle),
                        padding: const EdgeInsets.symmetric(vertical: 11),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                      ),
                      onPressed: () => Navigator.of(context).pop(),
                      child: const Text('CANCELAR', style: TextStyle(fontSize: 11, fontWeight: FontWeight.w700)),
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: primaryColor,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 11),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                      ),
                      onPressed: _saveSettings,
                      child: const Text('SALVAR PERSONALIZAÇÃO', style: TextStyle(fontSize: 11, fontWeight: FontWeight.w700)),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
