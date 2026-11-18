import os
from playwright.sync_api import sync_playwright

HTML_ESP32 = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; }
  body {
    width: 1920px;
    height: 1080px;
    background-color: #f1f5f9;
    background-image: radial-gradient(#cbd5e1 1.3px, transparent 1.3px);
    background-size: 26px 26px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
  }
  
  .header {
    background: #0f172a;
    color: white;
    padding: 16px 48px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 5px solid #f97316;
    box-shadow: 0 4px 16px rgba(0,0,0,0.18);
  }
  .header h1 { font-size: 30px; letter-spacing: 1px; display: flex; align-items: center; gap: 14px; font-weight: 800; }
  .header .badge {
    background: #f97316;
    color: #fff;
    font-size: 14px;
    font-weight: 800;
    padding: 6px 14px;
    border-radius: 6px;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .header .subtitle { font-size: 16px; color: #94a3b8; margin-top: 2px; }

  svg {
    width: 1920px;
    height: 990px;
    position: absolute;
    top: 86px;
    left: 0;
  }

  .legend-box {
    position: absolute;
    bottom: 28px;
    left: 48px;
    background: rgba(255, 255, 255, 0.97);
    border: 2px solid #cbd5e1;
    border-radius: 14px;
    padding: 18px 26px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.12);
    display: flex;
    flex-direction: column;
    gap: 10px;
    font-size: 14px;
  }
  .legend-title { font-weight: 800; font-size: 16px; color: #0f172a; margin-bottom: 4px; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px; }
  .legend-item { display: flex; align-items: center; gap: 12px; color: #334155; font-size: 13.5px; }
  .legend-color { width: 28px; height: 7px; border-radius: 4px; flex-shrink: 0; }

  .notes-box {
    position: absolute;
    bottom: 28px;
    right: 48px;
    background: #fffbeb;
    border: 2px solid #fde68a;
    border-radius: 14px;
    padding: 18px 28px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.09);
    max-width: 520px;
    font-size: 13.5px;
    color: #92400e;
    line-height: 1.55;
  }
  .notes-box strong { color: #b45309; }
</style>
</head>
<body>

<div class="header">
  <div>
    <h1><span>🤖</span> DIAGRAMA DE MONTAGEM: ESP32 + PONTE H L298N</h1>
    <div class="subtitle">Robô de Batalha / Tração Diferencial com Wi-Fi Web Controller e Failsafe</div>
  </div>
  <div class="badge">Esquema Físico 100% Preciso</div>
</div>

<div class="legend-box">
  <div class="legend-title">Identificação dos Fios e Funções</div>
  <div class="legend-item"><div class="legend-color" style="background:#ef4444;"></div><strong>Vermelho (+12V):</strong> Bateria ➔ Chave Geral ➔ Borne 12V da Ponte H</div>
  <div class="legend-item"><div class="legend-color" style="background:#dc2626;"></div><strong>Vermelho (+5V):</strong> Saída 5V do L298N ➔ Pino VIN do ESP32</div>
  <div class="legend-item"><div class="legend-color" style="background:#0f172a;"></div><strong>Preto (GND):</strong> Terra Unificado (Bateria + L298N GND + ESP32 GND)</div>
  <div class="legend-item"><div class="legend-color" style="background:#10b981;"></div><strong>Verde (PWM):</strong> GPIO 18 do ESP32 ➔ IN1 (Motor Esquerdo Frente)</div>
  <div class="legend-item"><div class="legend-color" style="background:#0284c7;"></div><strong>Azul (PWM):</strong> GPIO 19 do ESP32 ➔ IN2 (Motor Esquerdo Ré)</div>
  <div class="legend-item"><div class="legend-color" style="background:#f59e0b;"></div><strong>Laranja (PWM):</strong> GPIO 22 do ESP32 ➔ IN3 (Motor Direito Frente)</div>
  <div class="legend-item"><div class="legend-color" style="background:#8b5cf6;"></div><strong>Roxo (PWM):</strong> GPIO 23 do ESP32 ➔ IN4 (Motor Direito Ré)</div>
</div>

<div class="notes-box">
  <strong>⚠️ Dicas Cruciais de Montagem:</strong><br>
  1. <strong>GND Unificado:</strong> O fio preto une obrigatoriamente o polo negativo da bateria, o borne GND do L298N e o pino GND do ESP32.<br>
  2. <strong>Jumpers ENA e ENB:</strong> Mantenha os jumpers pretos colocados na ponte H para liberar velocidade por PWM direto nos pinos IN1 a IN4.<br>
  3. <strong>Alimentação do ESP32:</strong> O borne 5V do L298N fornece energia regulada para o pino VIN do ESP32.
</div>

<svg viewBox="0 0 1920 990">
  <defs>
    <filter id="shadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="3" dy="6" stdDeviation="6" flood-opacity="0.22"/>
    </filter>
    <filter id="wire-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="1" dy="3" stdDeviation="2.5" flood-opacity="0.35"/>
    </filter>
    
    <linearGradient id="heatsink-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="50%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>

    <linearGradient id="motor-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#fde047"/>
      <stop offset="70%" stop-color="#eab308"/>
      <stop offset="100%" stop-color="#ca8a04"/>
    </linearGradient>

    <linearGradient id="lipo-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2563eb"/>
      <stop offset="100%" stop-color="#1e40af"/>
    </linearGradient>
  </defs>

  <!-- ======================================================== -->
  <!-- 1. COMPONENTE: ESP32 DEVKIT V1 (X: 180, Y: 100)          -->
  <!-- ======================================================== -->
  <g id="esp32" transform="translate(180, 100)" filter="url(#shadow)">
    <!-- Black PCB Board -->
    <rect x="0" y="0" width="220" height="540" rx="16" fill="#18181b" stroke="#3f3f46" stroke-width="2.5"/>
    
    <!-- Mounting Holes -->
    <circle cx="16" cy="18" r="6" fill="#f1f5f9" stroke="#71717a" stroke-width="2"/>
    <circle cx="204" cy="18" r="6" fill="#f1f5f9" stroke="#71717a" stroke-width="2"/>
    <circle cx="16" cy="522" r="6" fill="#f1f5f9" stroke="#71717a" stroke-width="2"/>
    <circle cx="204" cy="522" r="6" fill="#f1f5f9" stroke="#71717a" stroke-width="2"/>

    <!-- ESP-WROOM-32 Metal RF Shield -->
    <rect x="35" y="30" width="150" height="150" rx="8" fill="#e2e8f0" stroke="#94a3b8" stroke-width="2"/>
    <rect x="50" y="6" width="120" height="28" rx="4" fill="#18181b" stroke="#3f3f46" stroke-width="1"/>
    <!-- Antenna Trace -->
    <path d="M 65,16 H 155 M 75,11 V 24 M 95,11 V 24 M 115,11 V 24 M 135,11 V 24" stroke="#eab308" stroke-width="2.5" fill="none"/>
    <text x="110" y="95" font-size="15" font-weight="900" fill="#0f172a" text-anchor="middle" letter-spacing="1">ESP-WROOM-32</text>
    <text x="110" y="118" font-size="12" font-weight="bold" fill="#475569" text-anchor="middle">Wi-Fi &amp; Bluetooth</text>
    <circle cx="55" cy="50" r="4" fill="#94a3b8"/>

    <!-- USB Connector at bottom -->
    <rect x="80" y="510" width="60" height="34" rx="4" fill="#94a3b8" stroke="#475569" stroke-width="1.5"/>
    <rect x="90" y="528" width="40" height="12" rx="2" fill="#1e293b"/>

    <!-- Board Name -->
    <text x="110" y="230" font-size="16" font-weight="900" fill="#ffffff" text-anchor="middle" letter-spacing="1.5">ESP32 DevKit</text>

    <!-- Buttons -->
    <rect x="38" y="475" width="26" height="18" rx="3" fill="#ef4444"/>
    <text x="51" y="508" font-size="10" font-weight="bold" fill="#94a3b8" text-anchor="middle">EN</text>
    <rect x="156" y="475" width="26" height="18" rx="3" fill="#3b82f6"/>
    <text x="169" y="508" font-size="10" font-weight="bold" fill="#94a3b8" text-anchor="middle">BOOT</text>

    <!-- Left Header Pins (Pinos 3V3, EN, D34 ... GND) -->
    <g font-size="10.5" font-family="monospace" font-weight="bold" fill="#cbd5e1">
      <circle cx="16" cy="70" r="6" fill="#eab308"/><text x="28" y="74">3V3</text>
      <circle cx="16" cy="98" r="6" fill="#eab308"/><text x="28" y="102">EN</text>
      <circle cx="16" cy="126" r="6" fill="#eab308"/><text x="28" y="130">VP</text>
      <circle cx="16" cy="154" r="6" fill="#eab308"/><text x="28" y="158">VN</text>
      <circle cx="16" cy="182" r="6" fill="#eab308"/><text x="28" y="186">D34</text>
      <circle cx="16" cy="210" r="6" fill="#eab308"/><text x="28" y="214">D35</text>
      <circle cx="16" cy="238" r="6" fill="#eab308"/><text x="28" y="242">D32</text>
      <circle cx="16" cy="266" r="6" fill="#eab308"/><text x="28" y="270">D33</text>
      <circle cx="16" cy="294" r="6" fill="#eab308"/><text x="28" y="298">D25</text>
      <circle cx="16" cy="322" r="7" fill="#f97316" stroke="#c2410c" stroke-width="1.5"/><text x="28" y="326" fill="#fdba74">D26(Arma)</text>
      <circle cx="16" cy="350" r="6" fill="#eab308"/><text x="28" y="354">D27</text>
      <circle cx="16" cy="378" r="6" fill="#eab308"/><text x="28" y="382">D14</text>
      <circle cx="16" cy="406" r="6" fill="#eab308"/><text x="28" y="410">D12</text>
      <circle cx="16" cy="434" r="6" fill="#eab308"/><text x="28" y="438">D13</text>
      <circle cx="16" cy="462" r="6" fill="#64748b"/><text x="28" y="466" fill="#94a3b8">GND</text>
    </g>

    <!-- Right Header Pins (VIN, GND, D15 ... D23) -->
    <g font-size="11" font-family="monospace" font-weight="bold">
      <!-- VIN -->
      <circle cx="204" cy="70" r="8" fill="#ef4444" stroke="#991b1b" stroke-width="2"/>
      <text x="168" y="74" fill="#fca5a5" text-anchor="end">VIN</text>
      <!-- GND -->
      <circle cx="204" cy="98" r="8" fill="#0f172a" stroke="#ffffff" stroke-width="2"/>
      <text x="168" y="102" fill="#ffffff" text-anchor="end">GND</text>

      <circle cx="204" cy="126" r="6" fill="#eab308"/><text x="180" y="130" fill="#cbd5e1" text-anchor="end">D15</text>
      <circle cx="204" cy="154" r="6" fill="#3b82f6"/><text x="180" y="158" fill="#93c5fd" text-anchor="end">D2</text>
      <circle cx="204" cy="182" r="6" fill="#eab308"/><text x="180" y="186" fill="#cbd5e1" text-anchor="end">D4</text>
      <circle cx="204" cy="210" r="6" fill="#eab308"/><text x="180" y="214" fill="#cbd5e1" text-anchor="end">RX2</text>
      <circle cx="204" cy="238" r="6" fill="#eab308"/><text x="180" y="242" fill="#cbd5e1" text-anchor="end">TX2</text>
      <circle cx="204" cy="266" r="6" fill="#eab308"/><text x="180" y="270" fill="#cbd5e1" text-anchor="end">D5</text>

      <!-- D18 (IN1) -->
      <circle cx="204" cy="294" r="8" fill="#10b981" stroke="#065f46" stroke-width="2"/>
      <text x="160" y="298" fill="#6ee7b7" text-anchor="end">D18 (IN1)</text>

      <!-- D19 (IN2) -->
      <circle cx="204" cy="322" r="8" fill="#0284c7" stroke="#075985" stroke-width="2"/>
      <text x="160" y="326" fill="#7dd3fc" text-anchor="end">D19 (IN2)</text>

      <circle cx="204" cy="350" r="6" fill="#eab308"/><text x="180" y="354" fill="#cbd5e1" text-anchor="end">D21</text>
      <circle cx="204" cy="378" r="6" fill="#eab308"/><text x="180" y="382" fill="#cbd5e1" text-anchor="end">RX0</text>
      <circle cx="204" cy="406" r="6" fill="#eab308"/><text x="180" y="410" fill="#cbd5e1" text-anchor="end">TX0</text>

      <!-- D22 (IN3) -->
      <circle cx="204" cy="434" r="8" fill="#f59e0b" stroke="#92400e" stroke-width="2"/>
      <text x="160" y="438" fill="#fde68a" text-anchor="end">D22 (IN3)</text>

      <!-- D23 (IN4) -->
      <circle cx="204" cy="462" r="8" fill="#8b5cf6" stroke="#5b21b6" stroke-width="2"/>
      <text x="160" y="466" fill="#ddd6fe" text-anchor="end">D23 (IN4)</text>
    </g>
  </g>

  <!-- ======================================================== -->
  <!-- 2. COMPONENTE: MÓDULO PONTE H L298N (X: 780, Y: 180)      -->
  <!-- ======================================================== -->
  <g id="l298n" transform="translate(780, 180)" filter="url(#shadow)">
    <rect x="0" y="0" width="370" height="390" rx="16" fill="#dc2626" stroke="#991b1b" stroke-width="3.5"/>
    <text x="185" y="36" font-size="20" font-weight="900" fill="#ffffff" text-anchor="middle" letter-spacing="1.5">MÓDULO PONTE H L298N</text>

    <!-- Black Heatsink -->
    <rect x="75" y="55" width="220" height="110" rx="6" fill="url(#heatsink-grad)" stroke="#0f172a" stroke-width="2"/>
    <!-- Heat fins -->
    <line x1="100" y1="55" x2="100" y2="165" stroke="#475569" stroke-width="3.5"/>
    <line x1="130" y1="55" x2="130" y2="165" stroke="#475569" stroke-width="3.5"/>
    <line x1="160" y1="55" x2="160" y2="165" stroke="#475569" stroke-width="3.5"/>
    <line x1="185" y1="55" x2="185" y2="165" stroke="#475569" stroke-width="3.5"/>
    <line x1="210" y1="55" x2="210" y2="165" stroke="#475569" stroke-width="3.5"/>
    <line x1="240" y1="55" x2="240" y2="165" stroke="#475569" stroke-width="3.5"/>
    <line x1="270" y1="55" x2="270" y2="165" stroke="#475569" stroke-width="3.5"/>

    <!-- Electrolytic Capacitors -->
    <circle cx="50" cy="130" r="18" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
    <path d="M 40,115 A 18 18 0 0 1 60,115" stroke="#cbd5e1" stroke-width="3" fill="none"/>
    <circle cx="320" cy="130" r="18" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
    <path d="M 310,115 A 18 18 0 0 1 330,115" stroke="#cbd5e1" stroke-width="3" fill="none"/>

    <!-- Left Blue Screw Terminal (OUT1 & OUT2) -->
    <rect x="-18" y="195" width="58" height="95" rx="6" fill="#1d4ed8" stroke="#1e3a8a" stroke-width="2"/>
    <circle cx="11" cy="220" r="11" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>
    <circle cx="11" cy="265" r="11" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>
    <text x="48" y="225" font-size="13" font-weight="900" fill="#ffffff">OUT1</text>
    <text x="48" y="270" font-size="13" font-weight="900" fill="#ffffff">OUT2</text>

    <!-- Right Blue Screw Terminal (OUT3 & OUT4) -->
    <rect x="330" y="195" width="58" height="95" rx="6" fill="#1d4ed8" stroke="#1e3a8a" stroke-width="2"/>
    <circle cx="359" cy="220" r="11" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>
    <circle cx="359" cy="265" r="11" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>
    <text x="322" y="225" font-size="13" font-weight="900" fill="#ffffff" text-anchor="end">OUT3</text>
    <text x="322" y="270" font-size="13" font-weight="900" fill="#ffffff" text-anchor="end">OUT4</text>

    <!-- Bottom 3-Pin Power Screw Terminal -->
    <rect x="25" y="305" width="145" height="72" rx="8" fill="#1d4ed8" stroke="#1e3a8a" stroke-width="2.5"/>
    
    <!-- 12V Screw -->
    <circle cx="50" cy="335" r="12" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>
    <text x="50" y="366" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">+12V</text>

    <!-- GND Screw -->
    <circle cx="97" cy="335" r="12" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>
    <text x="97" y="366" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">GND</text>

    <!-- 5V Screw -->
    <circle cx="145" cy="335" r="12" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>
    <text x="145" y="366" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">+5V</text>

    <!-- Jumper 5V -->
    <rect x="78" y="272" width="22" height="15" rx="3" fill="#0f172a" stroke="#facc15" stroke-width="1.5"/>
    <text x="89" y="266" font-size="10" font-weight="bold" fill="#fde047" text-anchor="middle">Jumper 5V</text>

    <!-- Logic Pins Header: ENA, IN1, IN2, IN3, IN4, ENB -->
    <rect x="185" y="325" width="170" height="42" rx="5" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    
    <!-- ENA Jumper -->
    <rect x="192" y="318" width="18" height="26" rx="3" fill="#020617" stroke="#facc15" stroke-width="1.5"/>
    <text x="201" y="312" font-size="10" font-weight="900" fill="#fde047" text-anchor="middle">ENA</text>
    <text x="201" y="358" font-size="8" font-weight="bold" fill="#94a3b8" text-anchor="middle">JMP</text>

    <!-- IN1 -->
    <circle cx="230" cy="346" r="7" fill="#10b981" stroke="#065f46" stroke-width="2"/>
    <text x="230" y="312" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">IN1</text>

    <!-- IN2 -->
    <circle cx="256" cy="346" r="7" fill="#0284c7" stroke="#075985" stroke-width="2"/>
    <text x="256" y="312" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">IN2</text>

    <!-- IN3 -->
    <circle cx="282" cy="346" r="7" fill="#f59e0b" stroke="#92400e" stroke-width="2"/>
    <text x="282" y="312" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">IN3</text>

    <!-- IN4 -->
    <circle cx="308" cy="346" r="7" fill="#8b5cf6" stroke="#5b21b6" stroke-width="2"/>
    <text x="308" y="312" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">IN4</text>

    <!-- ENB Jumper -->
    <rect x="328" y="318" width="18" height="26" rx="3" fill="#020617" stroke="#facc15" stroke-width="1.5"/>
    <text x="337" y="312" font-size="10" font-weight="900" fill="#fde047" text-anchor="middle">ENB</text>
    <text x="337" y="358" font-size="8" font-weight="bold" fill="#94a3b8" text-anchor="middle">JMP</text>
  </g>

  <!-- ======================================================== -->
  <!-- 3. COMPONENTE: BATERIA LiPo 7.4V (X: 740, Y: 680)         -->
  <!-- ======================================================== -->
  <g id="battery" transform="translate(720, 670)" filter="url(#shadow)">
    <rect x="0" y="0" width="230" height="115" rx="14" fill="url(#lipo-grad)" stroke="#1e3a8a" stroke-width="3"/>
    <text x="115" y="46" font-size="18" font-weight="900" fill="#ffffff" text-anchor="middle">BATERIA LiPo 2S</text>
    <text x="115" y="72" font-size="16" font-weight="bold" fill="#93c5fd" text-anchor="middle">7.4V - 1500mAh</text>
    <rect x="35" y="84" width="160" height="18" rx="4" fill="#1e3a8a"/>
    <text x="115" y="97" font-size="11" font-weight="bold" fill="#bfdbfe" text-anchor="middle">ALTA DESCARGA (30C)</text>

    <!-- Terminals -->
    <rect x="-12" y="32" width="14" height="16" rx="2" fill="#ef4444"/>
    <rect x="-12" y="70" width="14" height="16" rx="2" fill="#0f172a"/>
  </g>

  <!-- Chave Geral (Kill Switch) -->
  <g id="switch" transform="translate(560, 680)" filter="url(#shadow)">
    <rect x="0" y="0" width="90" height="65" rx="8" fill="#334155" stroke="#1e293b" stroke-width="2.5"/>
    <circle cx="45" cy="32" r="18" fill="#dc2626" stroke="#991b1b" stroke-width="2.5"/>
    <rect x="40" y="10" width="10" height="26" rx="5" fill="#f87171"/>
    <text x="45" y="58" font-size="10" font-weight="900" fill="#ffffff" text-anchor="middle">CHAVE GERAL</text>
  </g>

  <!-- ======================================================== -->
  <!-- 4. MOTORES DC COM RODAS (TT MOTORS)                      -->
  <!-- ======================================================== -->
  <!-- Motor Esquerdo (X: 1480, Y: 130) -->
  <g id="motor-left" transform="translate(1480, 130)" filter="url(#shadow)">
    <rect x="180" y="0" width="70" height="170" rx="14" fill="#0f172a" stroke="#000" stroke-width="3"/>
    <rect x="196" y="25" width="38" height="120" rx="10" fill="#facc15"/>
    <circle cx="215" cy="85" r="14" fill="#0f172a"/>
    <rect x="40" y="35" width="150" height="100" rx="10" fill="url(#motor-grad)" stroke="#a16207" stroke-width="3"/>
    <rect x="0" y="50" width="50" height="70" rx="8" fill="#cbd5e1" stroke="#64748b" stroke-width="2"/>
    <text x="115" y="80" font-size="15" font-weight="900" fill="#713f12" text-anchor="middle">MOTOR ESQUERDO</text>
    <text x="115" y="100" font-size="12" font-weight="bold" fill="#854d0e" text-anchor="middle">(Tração A - OUT1 / OUT2)</text>
    <circle cx="8" cy="68" r="5" fill="#f59e0b" stroke="#b45309" stroke-width="1.5"/>
    <circle cx="8" cy="102" r="5" fill="#f59e0b" stroke="#b45309" stroke-width="1.5"/>
  </g>

  <!-- Motor Direito (X: 1480, Y: 400) -->
  <g id="motor-right" transform="translate(1480, 400)" filter="url(#shadow)">
    <rect x="180" y="0" width="70" height="170" rx="14" fill="#0f172a" stroke="#000" stroke-width="3"/>
    <rect x="196" y="25" width="38" height="120" rx="10" fill="#facc15"/>
    <circle cx="215" cy="85" r="14" fill="#0f172a"/>
    <rect x="40" y="35" width="150" height="100" rx="10" fill="url(#motor-grad)" stroke="#a16207" stroke-width="3"/>
    <rect x="0" y="50" width="50" height="70" rx="8" fill="#cbd5e1" stroke="#64748b" stroke-width="2"/>
    <text x="115" y="80" font-size="15" font-weight="900" fill="#713f12" text-anchor="middle">MOTOR DIREITO</text>
    <text x="115" y="100" font-size="12" font-weight="bold" fill="#854d0e" text-anchor="middle">(Tração B - OUT3 / OUT4)</text>
    <circle cx="8" cy="68" r="5" fill="#f59e0b" stroke="#b45309" stroke-width="1.5"/>
    <circle cx="8" cy="102" r="5" fill="#f59e0b" stroke="#b45309" stroke-width="1.5"/>
  </g>

  <!-- ======================================================== -->
  <!-- 5. FIAÇÃO ELÉTRICA (WIRES)                               -->
  <!-- ======================================================== -->
  <g id="wires" filter="url(#wire-shadow)">
    <!-- Bateria (+) -> Chave Geral -->
    <path d="M 708, 702 H 650" fill="none" stroke="#ef4444" stroke-width="6" stroke-linecap="round"/>

    <!-- Chave Geral -> L298N 12V (830, 515) -->
    <path d="M 560, 712 H 510 V 610 H 830 V 515" fill="none" stroke="#ef4444" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
    
    <!-- Bateria (-) -> L298N GND (877, 515) -->
    <path d="M 708, 740 H 480 V 630 H 877 V 515" fill="none" stroke="#0f172a" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- L298N 5V Out (925, 515) -> ESP32 VIN (384, 170) -->
    <path d="M 925, 515 V 590 H 440 V 170 H 384" fill="none" stroke="#dc2626" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    
    <!-- L298N GND (877, 515) -> ESP32 GND (384, 198) -->
    <path d="M 877, 515 V 570 H 420 V 198 H 384" fill="none" stroke="#0f172a" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- ESP32 D18 (384, 394) -> L298N IN1 (1010, 526) -->
    <path d="M 384, 394 H 660 V 465 H 1010 V 526" fill="none" stroke="#10b981" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- ESP32 D19 (384, 422) -> L298N IN2 (1036, 526) -->
    <path d="M 384, 422 H 680 V 480 H 1036 V 526" fill="none" stroke="#0284c7" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- ESP32 D22 (384, 534) -> L298N IN3 (1062, 526) -->
    <path d="M 384, 534 H 700 V 495 H 1062 V 526" fill="none" stroke="#f59e0b" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- ESP32 D23 (384, 562) -> L298N IN4 (1088, 526) -->
    <path d="M 384, 562 H 720 V 510 H 1088 V 526" fill="none" stroke="#8b5cf6" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- Motor Esquerdo OUT1 & OUT2 -->
    <path d="M 762, 400 H 730 V 145 H 1450 V 198 H 1488" fill="none" stroke="#ef4444" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M 762, 445 H 710 V 130 H 1430 V 232 H 1488" fill="none" stroke="#0f172a" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- Motor Direito OUT3 & OUT4 -->
    <path d="M 1168, 400 H 1320 V 468 H 1488" fill="none" stroke="#ef4444" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M 1168, 445 H 1300 V 502 H 1488" fill="none" stroke="#0f172a" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <!-- Wire Connection Junction Dots -->
  <circle cx="830" cy="515" r="5" fill="#ef4444"/>
  <circle cx="877" cy="515" r="5" fill="#0f172a"/>
  <circle cx="925" cy="515" r="5" fill="#dc2626"/>
  <circle cx="384" cy="170" r="5" fill="#dc2626"/>
  <circle cx="384" cy="198" r="5" fill="#0f172a"/>
  <circle cx="384" cy="394" r="5" fill="#10b981"/>
  <circle cx="384" cy="422" r="5" fill="#0284c7"/>
  <circle cx="384" cy="534" r="5" fill="#f59e0b"/>
  <circle cx="384" cy="562" r="5" fill="#8b5cf6"/>

  <!-- Wire Badges / Callouts -->
  <g font-size="11" font-weight="bold" text-anchor="middle">
    <rect x="440" y="558" width="130" height="20" rx="4" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>
    <text x="505" y="572" fill="#0f172a">GND Comum</text>

    <rect x="440" y="582" width="130" height="20" rx="4" fill="#ffffff" stroke="#dc2626" stroke-width="1.5"/>
    <text x="505" y="596" fill="#dc2626">+5V (L298N ➔ VIN)</text>

    <rect x="740" y="454" width="120" height="18" rx="4" fill="#ffffff" stroke="#10b981" stroke-width="1.5"/>
    <text x="800" y="467" fill="#059669">GPIO 18 ➔ IN1</text>

    <rect x="740" y="474" width="120" height="18" rx="4" fill="#ffffff" stroke="#0284c7" stroke-width="1.5"/>
    <text x="800" y="487" fill="#0284c7">GPIO 19 ➔ IN2</text>

    <rect x="740" y="494" width="120" height="18" rx="4" fill="#ffffff" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="800" y="507" fill="#d97706">GPIO 22 ➔ IN3</text>

    <rect x="740" y="514" width="120" height="18" rx="4" fill="#ffffff" stroke="#8b5cf6" stroke-width="1.5"/>
    <text x="800" y="527" fill="#7c3aed">GPIO 23 ➔ IN4</text>
  </g>
</svg>

</body>
</html>
"""

HTML_ARDUINO = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; }
  body {
    width: 1920px;
    height: 1080px;
    background-color: #f1f5f9;
    background-image: radial-gradient(#cbd5e1 1.3px, transparent 1.3px);
    background-size: 26px 26px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
  }
  
  .header {
    background: #00878F;
    color: white;
    padding: 16px 48px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 5px solid #f59e0b;
    box-shadow: 0 4px 16px rgba(0,0,0,0.18);
  }
  .header h1 { font-size: 30px; letter-spacing: 1px; display: flex; align-items: center; gap: 14px; font-weight: 800; }
  .header .badge {
    background: #f59e0b;
    color: #0f172a;
    font-size: 14px;
    font-weight: 800;
    padding: 6px 14px;
    border-radius: 6px;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .header .subtitle { font-size: 16px; color: #e0f2fe; margin-top: 2px; }

  svg {
    width: 1920px;
    height: 990px;
    position: absolute;
    top: 86px;
    left: 0;
  }

  .legend-box {
    position: absolute;
    bottom: 28px;
    left: 48px;
    background: rgba(255, 255, 255, 0.97);
    border: 2px solid #cbd5e1;
    border-radius: 14px;
    padding: 18px 26px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.12);
    display: flex;
    flex-direction: column;
    gap: 9px;
    font-size: 14px;
  }
  .legend-title { font-weight: 800; font-size: 16px; color: #0f172a; margin-bottom: 4px; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px; }
  .legend-item { display: flex; align-items: center; gap: 12px; color: #334155; font-size: 13.5px; }
  .legend-color { width: 28px; height: 7px; border-radius: 4px; flex-shrink: 0; }

  .notes-box {
    position: absolute;
    bottom: 28px;
    right: 48px;
    background: #eff6ff;
    border: 2px solid #bfdbfe;
    border-radius: 14px;
    padding: 18px 28px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.09);
    max-width: 530px;
    font-size: 13.5px;
    color: #1e3a8a;
    line-height: 1.55;
  }
  .notes-box strong { color: #1d4ed8; }
</style>
</head>
<body>

<div class="header">
  <div>
    <h1><span>🕹️</span> DIAGRAMA DE MONTAGEM: ARDUINO UNO + BLUETOOTH HC-05 + L298N</h1>
    <div class="subtitle">Robô de Batalha / Tração Diferencial com Bluetooth e Divisor de Proteção</div>
  </div>
  <div class="badge">Esquema Físico 100% Preciso</div>
</div>

<div class="legend-box">
  <div class="legend-title">Identificação dos Fios e Funções</div>
  <div class="legend-item"><div class="legend-color" style="background:#ef4444;"></div><strong>Vermelho (+5V):</strong> Alimentação 5V do Arduino e HC-05</div>
  <div class="legend-item"><div class="legend-color" style="background:#0f172a;"></div><strong>Preto (GND):</strong> Terra Comum (Arduino + HC-05 + L298N + Bateria)</div>
  <div class="legend-item"><div class="legend-color" style="background:#3b82f6;"></div><strong>Azul:</strong> HC-05 TXD ➔ Arduino Pino D2 (RX SoftwareSerial)</div>
  <div class="legend-item"><div class="legend-color" style="background:#eab308;"></div><strong>Amarelo:</strong> Arduino Pino D3 (TX) ➔ Divisor 1kΩ/2kΩ ➔ HC-05 RXD (3.3V)</div>
  <div class="legend-item"><div class="legend-color" style="background:#10b981;"></div><strong>Verde (PWM):</strong> Arduino D5 ➔ L298N IN1 (Motor Esquerdo Frente)</div>
  <div class="legend-item"><div class="legend-color" style="background:#06b6d4;"></div><strong>Ciano (PWM):</strong> Arduino D6 ➔ L298N IN2 (Motor Esquerdo Ré)</div>
  <div class="legend-item"><div class="legend-color" style="background:#f97316;"></div><strong>Laranja (PWM):</strong> Arduino D9 ➔ L298N IN3 (Motor Direito Frente)</div>
  <div class="legend-item"><div class="legend-color" style="background:#8b5cf6;"></div><strong>Roxo (PWM):</strong> Arduino D10 ➔ L298N IN4 (Motor Direito Ré)</div>
</div>

<div class="notes-box">
  <strong>⚠️ Divisor de Tensão Protetor (1kΩ e 2kΩ):</strong><br>
  - O pino RXD do HC-05 aceita apenas <strong>3.3V</strong>. Os 5V do Arduino podem danificá-lo a longo prazo.<br>
  - <strong>Resistor 1kΩ:</strong> Conecta o pino D3 do Arduino ao pino RXD do HC-05.<br>
  - <strong>Resistor 2kΩ:</strong> Conecta o pino RXD do HC-05 ao <strong>GND</strong>, reduzindo os 5V para exatos ~3.33V de forma segura!
</div>

<svg viewBox="0 0 1920 990">
  <defs>
    <filter id="shadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="3" dy="6" stdDeviation="6" flood-opacity="0.22"/>
    </filter>
    <filter id="wire-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="1" dy="3" stdDeviation="2.5" flood-opacity="0.35"/>
    </filter>
    <linearGradient id="heatsink-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="50%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="motor-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#fde047"/>
      <stop offset="70%" stop-color="#eab308"/>
      <stop offset="100%" stop-color="#ca8a04"/>
    </linearGradient>
    <linearGradient id="lipo-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2563eb"/>
      <stop offset="100%" stop-color="#1e40af"/>
    </linearGradient>
  </defs>

  <!-- ======================================================== -->
  <!-- 1. COMPONENTE: ARDUINO UNO R3 (X: 100, Y: 130)           -->
  <!-- ======================================================== -->
  <g id="arduino-uno" transform="translate(100, 130)" filter="url(#shadow)">
    <path d="M 0,30 L 30,0 H 330 Q 340,0 340,10 V 460 Q 340,470 330,470 H 10 Q 0,470 0,460 Z" fill="#00878F" stroke="#005f66" stroke-width="3"/>
    
    <!-- USB Port -->
    <rect x="-15" y="45" width="70" height="55" rx="4" fill="#cbd5e1" stroke="#64748b" stroke-width="2"/>
    <rect x="-5" y="58" width="40" height="30" rx="2" fill="#334155"/>

    <!-- DC Barrel Jack -->
    <rect x="-15" y="370" width="80" height="60" rx="6" fill="#1e293b" stroke="#0f172a" stroke-width="2"/>
    <circle cx="20" cy="400" r="12" fill="#0f172a"/>

    <!-- ATmega328P Chip -->
    <rect x="140" y="295" width="150" height="42" rx="4" fill="#18181b" stroke="#3f3f46" stroke-width="1.5"/>
    <circle cx="150" cy="316" r="4" fill="#3f3f46"/>
    <text x="215" y="321" font-size="11" font-weight="bold" fill="#9ca3af" text-anchor="middle" letter-spacing="1">ATmega328P-PU</text>

    <!-- Reset Button -->
    <rect x="280" y="40" width="28" height="28" rx="4" fill="#f87171" stroke="#b91c1c" stroke-width="1.5"/>
    <circle cx="294" cy="54" r="8" fill="#dc2626"/>

    <!-- Arduino Branding -->
    <circle cx="170" cy="190" r="22" fill="#00666d"/>
    <text x="170" y="196" font-size="18" font-weight="bold" fill="#ffffff" text-anchor="middle">∞</text>
    <text x="235" y="185" font-size="22" font-weight="900" fill="#ffffff">ARDUINO</text>
    <text x="235" y="206" font-size="17" font-weight="bold" fill="#facc15">UNO</text>

    <!-- Digital Pins Header (Top) -->
    <rect x="85" y="6" width="245" height="26" rx="4" fill="#18181b"/>
    <g font-size="10.5" font-weight="bold" font-family="monospace" text-anchor="middle">
      <!-- D2 (BT RX) -->
      <circle cx="295" cy="19" r="6.5" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2"/>
      <text x="295" y="44" fill="#93c5fd">D2</text>
      <!-- D3 (BT TX) -->
      <circle cx="270" cy="19" r="6.5" fill="#eab308" stroke="#a16207" stroke-width="2"/>
      <text x="270" y="44" fill="#fde047">D3~</text>
      <!-- D4 -->
      <circle cx="245" cy="19" r="5" fill="#64748b"/>
      <text x="245" y="44" fill="#cbd5e1">D4</text>
      <!-- D5 (IN1 PWM) -->
      <circle cx="220" cy="19" r="6.5" fill="#10b981" stroke="#065f46" stroke-width="2"/>
      <text x="220" y="44" fill="#6ee7b7">D5~</text>
      <!-- D6 (IN2 PWM) -->
      <circle cx="195" cy="19" r="6.5" fill="#06b6d4" stroke="#0e7490" stroke-width="2"/>
      <text x="195" y="44" fill="#67e8f9">D6~</text>
      <!-- D7 -->
      <circle cx="170" cy="19" r="5" fill="#64748b"/><text x="170" y="44" fill="#cbd5e1">D7</text>
      <!-- D8 -->
      <circle cx="150" cy="19" r="5" fill="#64748b"/><text x="150" y="44" fill="#cbd5e1">D8</text>
      <!-- D9 (IN3 PWM) -->
      <circle cx="130" cy="19" r="6.5" fill="#f97316" stroke="#c2410c" stroke-width="2"/>
      <text x="130" y="44" fill="#fdba74">D9~</text>
      <!-- D10 (IN4 PWM) -->
      <circle cx="105" cy="19" r="6.5" fill="#8b5cf6" stroke="#6d28d9" stroke-width="2"/>
      <text x="105" y="44" fill="#c4b5fd">D10~</text>
    </g>

    <!-- Power Header (Bottom) -->
    <rect x="150" y="442" width="180" height="26" rx="4" fill="#18181b"/>
    <g font-size="11" font-weight="bold" font-family="monospace" text-anchor="middle">
      <!-- 5V -->
      <circle cx="215" cy="455" r="7" fill="#ef4444" stroke="#991b1b" stroke-width="2"/>
      <text x="215" y="432" fill="#fca5a5">5V</text>
      <!-- GND -->
      <circle cx="242" cy="455" r="7" fill="#0f172a" stroke="#ffffff" stroke-width="2"/>
      <text x="242" y="432" fill="#ffffff">GND</text>
      <!-- VIN -->
      <circle cx="295" cy="455" r="6" fill="#dc2626"/>
      <text x="295" y="432" fill="#fca5a5">VIN</text>
    </g>
  </g>

  <!-- ======================================================== -->
  <!-- 2. MINI PROTOBOARD COM HC-05 (X: 520, Y: 100)            -->
  <!-- ======================================================== -->
  <g id="breadboard" transform="translate(530, 90)" filter="url(#shadow)">
    <rect x="0" y="0" width="280" height="500" rx="14" fill="#ffffff" stroke="#cbd5e1" stroke-width="3"/>
    <text x="140" y="32" font-size="14" font-weight="900" fill="#475569" text-anchor="middle">PROTOBOARD</text>

    <!-- Power Rails -->
    <line x1="28" y1="55" x2="28" y2="470" stroke="#ef4444" stroke-width="3.5"/>
    <line x1="48" y1="55" x2="48" y2="470" stroke="#3b82f6" stroke-width="3.5"/>
    <text x="28" y="48" font-size="15" font-weight="900" fill="#ef4444" text-anchor="middle">+</text>
    <text x="48" y="48" font-size="15" font-weight="900" fill="#3b82f6" text-anchor="middle">-</text>

    <!-- HC-05 Module -->
    <g id="hc05" transform="translate(80, 240)">
      <rect x="0" y="0" width="140" height="215" rx="8" fill="#1e40af" stroke="#1d4ed8" stroke-width="2.5"/>
      <rect x="18" y="12" width="104" height="38" rx="4" fill="#0f172a"/>
      <path d="M 28,28 H 112 M 38,20 V 36 M 58,20 V 36 M 78,20 V 36 M 98,20 V 36" stroke="#eab308" stroke-width="2.5" fill="none"/>
      
      <rect x="35" y="65" width="70" height="42" rx="3" fill="#0f172a"/>
      <text x="70" y="90" font-size="14" font-weight="900" fill="#ffffff" text-anchor="middle">HC-05</text>
      <text x="70" y="128" font-size="11" font-weight="bold" fill="#93c5fd" text-anchor="middle">Bluetooth Serial</text>

      <circle cx="24" cy="130" r="4" fill="#ef4444"/>

      <!-- 6 Header Pins -->
      <g font-size="10" font-weight="900" font-family="monospace" fill="#ffffff" text-anchor="middle">
        <circle cx="16" cy="198" r="4" fill="#94a3b8"/><text x="16" y="186">ST</text>
        <circle cx="38" cy="198" r="6" fill="#eab308" stroke="#fff" stroke-width="1.5"/><text x="38" y="186" fill="#fde047">RX</text>
        <circle cx="60" cy="198" r="6" fill="#3b82f6" stroke="#fff" stroke-width="1.5"/><text x="60" y="186" fill="#93c5fd">TX</text>
        <circle cx="82" cy="198" r="6" fill="#0f172a" stroke="#fff" stroke-width="1.5"/><text x="82" y="186">GND</text>
        <circle cx="104" cy="198" r="6" fill="#ef4444" stroke="#fff" stroke-width="1.5"/><text x="104" y="186" fill="#fca5a5">VCC</text>
        <circle cx="124" cy="198" r="4" fill="#94a3b8"/><text x="124" y="186">EN</text>
      </g>
    </g>

    <!-- Resistor 1 (1kΩ) -->
    <g id="r1" transform="translate(118, 100)">
      <line x1="0" y1="0" x2="0" y2="85" stroke="#64748b" stroke-width="3"/>
      <rect x="-8" y="22" width="16" height="42" rx="4" fill="#fde68a" stroke="#d97706" stroke-width="1.5"/>
      <rect x="-8" y="28" width="16" height="4" fill="#78350f"/>
      <rect x="-8" y="36" width="16" height="4" fill="#000000"/>
      <rect x="-8" y="44" width="16" height="4" fill="#dc2626"/>
      <rect x="-8" y="54" width="16" height="4" fill="#eab308"/>
      <text x="18" y="46" font-size="13" font-weight="900" fill="#b45309">1 kΩ</text>
    </g>

    <!-- Resistor 2 (2kΩ) -->
    <g id="r2" transform="translate(68, 185)">
      <line x1="0" y1="0" x2="50" y2="0" stroke="#64748b" stroke-width="3"/>
      <rect x="12" y="-8" width="28" height="16" rx="4" fill="#fde68a" stroke="#d97706" stroke-width="1.5"/>
      <rect x="16" y="-8" width="4" height="16" fill="#dc2626"/>
      <rect x="23" y="-8" width="4" height="16" fill="#000000"/>
      <rect x="30" y="-8" width="4" height="16" fill="#dc2626"/>
      <rect x="36" y="-8" width="3" height="16" fill="#eab308"/>
      <text x="26" y="-14" font-size="13" font-weight="900" fill="#b45309" text-anchor="middle">2 kΩ</text>
    </g>

    <rect x="80" y="50" width="160" height="36" rx="6" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1.5"/>
    <text x="160" y="66" font-size="11" font-weight="900" fill="#1d4ed8" text-anchor="middle">DIVISOR DE TENSÃO</text>
    <text x="160" y="80" font-size="10" font-weight="bold" fill="#2563eb" text-anchor="middle">Protege o pino RXD (3.3V)</text>
  </g>

  <!-- ======================================================== -->
  <!-- 3. COMPONENTE: MÓDULO PONTE H L298N (X: 960, Y: 180)      -->
  <!-- ======================================================== -->
  <g id="l298n" transform="translate(960, 180)" filter="url(#shadow)">
    <rect x="0" y="0" width="370" height="390" rx="16" fill="#dc2626" stroke="#991b1b" stroke-width="3.5"/>
    <text x="185" y="36" font-size="20" font-weight="900" fill="#ffffff" text-anchor="middle" letter-spacing="1.5">MÓDULO PONTE H L298N</text>

    <!-- Heatsink -->
    <rect x="75" y="55" width="220" height="110" rx="6" fill="url(#heatsink-grad)" stroke="#0f172a" stroke-width="2"/>
    <line x1="100" y1="55" x2="100" y2="165" stroke="#475569" stroke-width="3.5"/>
    <line x1="130" y1="55" x2="130" y2="165" stroke="#475569" stroke-width="3.5"/>
    <line x1="160" y1="55" x2="160" y2="165" stroke="#475569" stroke-width="3.5"/>
    <line x1="185" y1="55" x2="185" y2="165" stroke="#475569" stroke-width="3.5"/>
    <line x1="210" y1="55" x2="210" y2="165" stroke="#475569" stroke-width="3.5"/>
    <line x1="240" y1="55" x2="240" y2="165" stroke="#475569" stroke-width="3.5"/>
    <line x1="270" y1="55" x2="270" y2="165" stroke="#475569" stroke-width="3.5"/>

    <!-- Left Blue Screw Terminal (OUT1 & OUT2) -->
    <rect x="-18" y="195" width="58" height="95" rx="6" fill="#1d4ed8" stroke="#1e3a8a" stroke-width="2"/>
    <circle cx="11" cy="220" r="11" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>
    <circle cx="11" cy="265" r="11" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>
    <text x="48" y="225" font-size="13" font-weight="900" fill="#ffffff">OUT1</text>
    <text x="48" y="270" font-size="13" font-weight="900" fill="#ffffff">OUT2</text>

    <!-- Right Blue Screw Terminal (OUT3 & OUT4) -->
    <rect x="330" y="195" width="58" height="95" rx="6" fill="#1d4ed8" stroke="#1e3a8a" stroke-width="2"/>
    <circle cx="359" cy="220" r="11" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>
    <circle cx="359" cy="265" r="11" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>
    <text x="322" y="225" font-size="13" font-weight="900" fill="#ffffff" text-anchor="end">OUT3</text>
    <text x="322" y="270" font-size="13" font-weight="900" fill="#ffffff" text-anchor="end">OUT4</text>

    <!-- Bottom 3-Pin Power Screw Terminal -->
    <rect x="25" y="305" width="145" height="72" rx="8" fill="#1d4ed8" stroke="#1e3a8a" stroke-width="2.5"/>
    <circle cx="50" cy="335" r="12" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>
    <text x="50" y="366" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">+12V</text>
    <circle cx="97" cy="335" r="12" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>
    <text x="97" y="366" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">GND</text>
    <circle cx="145" cy="335" r="12" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>
    <text x="145" y="366" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">+5V</text>

    <!-- Logic Pins Header -->
    <rect x="185" y="325" width="170" height="42" rx="5" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <rect x="192" y="318" width="18" height="26" rx="3" fill="#020617" stroke="#facc15" stroke-width="1.5"/>
    <text x="201" y="312" font-size="10" font-weight="900" fill="#fde047" text-anchor="middle">ENA</text>

    <circle cx="230" cy="346" r="7" fill="#10b981" stroke="#065f46" stroke-width="2"/>
    <text x="230" y="312" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">IN1</text>
    <circle cx="256" cy="346" r="7" fill="#06b6d4" stroke="#0e7490" stroke-width="2"/>
    <text x="256" y="312" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">IN2</text>
    <circle cx="282" cy="346" r="7" fill="#f97316" stroke="#c2410c" stroke-width="2"/>
    <text x="282" y="312" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">IN3</text>
    <circle cx="308" cy="346" r="7" fill="#8b5cf6" stroke="#6d28d9" stroke-width="2"/>
    <text x="308" y="312" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">IN4</text>

    <rect x="328" y="318" width="18" height="26" rx="3" fill="#020617" stroke="#facc15" stroke-width="1.5"/>
    <text x="337" y="312" font-size="10" font-weight="900" fill="#fde047" text-anchor="middle">ENB</text>
  </g>

  <!-- ======================================================== -->
  <!-- 4. MOTORES DC COM RODAS (TT MOTORS)                      -->
  <!-- ======================================================== -->
  <g id="motor-left" transform="translate(1480, 130)" filter="url(#shadow)">
    <rect x="180" y="0" width="70" height="170" rx="14" fill="#0f172a" stroke="#000" stroke-width="3"/>
    <rect x="196" y="25" width="38" height="120" rx="10" fill="#facc15"/>
    <circle cx="215" cy="85" r="14" fill="#0f172a"/>
    <rect x="40" y="35" width="150" height="100" rx="10" fill="url(#motor-grad)" stroke="#a16207" stroke-width="3"/>
    <rect x="0" y="50" width="50" height="70" rx="8" fill="#cbd5e1" stroke="#64748b" stroke-width="2"/>
    <text x="115" y="80" font-size="15" font-weight="900" fill="#713f12" text-anchor="middle">MOTOR ESQUERDO</text>
    <text x="115" y="100" font-size="12" font-weight="bold" fill="#854d0e" text-anchor="middle">(Tração A - OUT1 / OUT2)</text>
    <circle cx="8" cy="68" r="5" fill="#f59e0b" stroke="#b45309" stroke-width="1.5"/>
    <circle cx="8" cy="102" r="5" fill="#f59e0b" stroke="#b45309" stroke-width="1.5"/>
  </g>

  <g id="motor-right" transform="translate(1480, 400)" filter="url(#shadow)">
    <rect x="180" y="0" width="70" height="170" rx="14" fill="#0f172a" stroke="#000" stroke-width="3"/>
    <rect x="196" y="25" width="38" height="120" rx="10" fill="#facc15"/>
    <circle cx="215" cy="85" r="14" fill="#0f172a"/>
    <rect x="40" y="35" width="150" height="100" rx="10" fill="url(#motor-grad)" stroke="#a16207" stroke-width="3"/>
    <rect x="0" y="50" width="50" height="70" rx="8" fill="#cbd5e1" stroke="#64748b" stroke-width="2"/>
    <text x="115" y="80" font-size="15" font-weight="900" fill="#713f12" text-anchor="middle">MOTOR DIREITO</text>
    <text x="115" y="100" font-size="12" font-weight="bold" fill="#854d0e" text-anchor="middle">(Tração B - OUT3 / OUT4)</text>
    <circle cx="8" cy="68" r="5" fill="#f59e0b" stroke="#b45309" stroke-width="1.5"/>
    <circle cx="8" cy="102" r="5" fill="#f59e0b" stroke="#b45309" stroke-width="1.5"/>
  </g>

  <!-- ======================================================== -->
  <!-- 5. FIAÇÃO ELÉTRICA (WIRES) ARDUINO + HC-05 + L298N        -->
  <!-- ======================================================== -->
  <g id="wires" filter="url(#wire-shadow)">
    <!-- 1. HC-05 TXD (648, 488) -> Arduino D2 (395, 149) -->
    <path d="M 648, 488 V 530 H 450 V 149 H 395" fill="none" stroke="#3b82f6" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- 2. Arduino D3 (370, 149) -> Top of Resistor 1k (648, 190) -->
    <path d="M 370, 149 V 115 H 648 V 190" fill="none" stroke="#eab308" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- 3. Bottom of Resistor 1k (648, 275) -> HC-05 RXD (626, 488) -->
    <path d="M 648, 275 V 450 H 626 V 488" fill="none" stroke="#eab308" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- 4. Resistor 2k (598, 275) -> Breadboard GND (-) (578, 275) -->
    <path d="M 598, 275 H 578" fill="none" stroke="#0f172a" stroke-width="4.5" stroke-linecap="round"/>

    <!-- 5. Arduino 5V (315, 585) -> Breadboard (+) (558, 585) -->
    <path d="M 315, 585 H 558" fill="none" stroke="#ef4444" stroke-width="5" stroke-linecap="round"/>
    <!-- Breadboard (+) to HC-05 VCC (692, 488) -->
    <path d="M 558, 510 H 692 V 488" fill="none" stroke="#ef4444" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- 6. Arduino GND (342, 585) -> Breadboard (-) (578, 585) -->
    <path d="M 342, 585 H 578" fill="none" stroke="#0f172a" stroke-width="5" stroke-linecap="round"/>
    <!-- Breadboard (-) to HC-05 GND (670, 488) -->
    <path d="M 578, 495 H 670 V 488" fill="none" stroke="#0f172a" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- 7. Arduino D5 (320, 149) -> L298N IN1 (1190, 526) -->
    <path d="M 320, 149 V 85 H 890 V 465 H 1190 V 526" fill="none" stroke="#10b981" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- 8. Arduino D6 (295, 149) -> L298N IN2 (1216, 526) -->
    <path d="M 295, 149 V 70 H 910 V 480 H 1216 V 526" fill="none" stroke="#06b6d4" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- 9. Arduino D9 (230, 149) -> L298N IN3 (1242, 526) -->
    <path d="M 230, 149 V 55 H 930 V 495 H 1242 V 526" fill="none" stroke="#f97316" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- 10. Arduino D10 (205, 149) -> L298N IN4 (1268, 526) -->
    <path d="M 205, 149 V 40 H 950 V 510 H 1268 V 526" fill="none" stroke="#8b5cf6" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- 11. POWER: L298N 5V Out (1105, 515) -> Arduino 5V/VIN (315, 585) -->
    <path d="M 1105, 515 V 650 H 315 V 585" fill="none" stroke="#ef4444" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- 12. POWER: L298N GND (1057, 515) -> Common GND (342, 585) -->
    <path d="M 1057, 515 V 630 H 342 V 585" fill="none" stroke="#0f172a" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- Motor Esquerdo OUT1 & OUT2 -->
    <path d="M 942, 400 H 910 V 145 H 1450 V 198 H 1488" fill="none" stroke="#ef4444" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M 942, 445 H 890 V 130 H 1430 V 232 H 1488" fill="none" stroke="#0f172a" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- Motor Direito OUT3 & OUT4 -->
    <path d="M 1348, 400 H 1400 V 468 H 1488" fill="none" stroke="#ef4444" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M 1348, 445 H 1380 V 502 H 1488" fill="none" stroke="#0f172a" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <!-- Labels on wires -->
  <g font-size="11" font-weight="bold" text-anchor="middle">
    <rect x="390" y="240" width="130" height="20" rx="4" fill="#ffffff" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="455" y="254" fill="#1d4ed8">HC-05 TXD ➔ D2</text>

    <rect x="360" y="80" width="130" height="20" rx="4" fill="#ffffff" stroke="#eab308" stroke-width="1.5"/>
    <text x="425" y="94" fill="#a16207">D3 (TX) ➔ 1kΩ</text>

    <rect x="680" y="55" width="130" height="20" rx="4" fill="#ffffff" stroke="#10b981" stroke-width="1.5"/>
    <text x="745" y="69" fill="#059669">D5 ➔ L298N IN1</text>

    <rect x="820" y="38" width="130" height="20" rx="4" fill="#ffffff" stroke="#f97316" stroke-width="1.5"/>
    <text x="885" y="52" fill="#c2410c">D9 ➔ L298N IN3</text>
  </g>
</svg>

</body>
</html>
"""

def generate_screenshots():
    with open("docs/diagrama_esp32.html", "w", encoding="utf-8") as f:
        f.write(HTML_ESP32)
    with open("docs/diagrama_arduino.html", "w", encoding="utf-8") as f:
        f.write(HTML_ARDUINO)

    print("HTML files updated. Launching Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})

        # Screenshot ESP32
        page.goto("file:///" + os.path.abspath("docs/diagrama_esp32.html").replace("\\", "/"))
        page.wait_for_timeout(300)
        page.screenshot(path="docs/images/circuito_esp32_l298n.jpg", type="jpeg", quality=95)
        print("ESP32 diagram recaptured!")

        # Screenshot Arduino
        page.goto("file:///" + os.path.abspath("docs/diagrama_arduino.html").replace("\\", "/"))
        page.wait_for_timeout(300)
        page.screenshot(path="docs/images/circuito_arduino_hc05.jpg", type="jpeg", quality=95)
        print("Arduino diagram recaptured!")

        browser.close()

if __name__ == "__main__":
    generate_screenshots()
