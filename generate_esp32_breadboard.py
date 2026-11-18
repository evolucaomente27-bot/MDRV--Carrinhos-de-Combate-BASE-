import os
from playwright.sync_api import sync_playwright

HTML_ESP32_MB102 = """<!DOCTYPE html>
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
    border-bottom: 5px solid #10b981;
    box-shadow: 0 4px 16px rgba(0,0,0,0.18);
  }
  .header h1 { font-size: 29px; letter-spacing: 1px; display: flex; align-items: center; gap: 14px; font-weight: 800; }
  .header .badge {
    background: #0284c7;
    color: #ffffff;
    font-size: 14px;
    font-weight: 800;
    padding: 6px 14px;
    border-radius: 6px;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .header .subtitle { font-size: 15.5px; color: #94a3b8; margin-top: 2px; }

  svg {
    width: 1920px;
    height: 990px;
    position: absolute;
    top: 86px;
    left: 0;
  }

  .legend-box {
    position: absolute;
    bottom: 22px;
    left: 48px;
    background: rgba(255, 255, 255, 0.97);
    border: 2px solid #cbd5e1;
    border-radius: 14px;
    padding: 16px 24px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.12);
    display: flex;
    flex-direction: column;
    gap: 8px;
    font-size: 13.5px;
    max-width: 580px;
  }
  .legend-title { font-weight: 800; font-size: 15.5px; color: #0f172a; margin-bottom: 2px; border-bottom: 2px solid #e2e8f0; padding-bottom: 5px; }
  .legend-item { display: flex; align-items: center; gap: 10px; color: #334155; }
  .legend-color { width: 26px; height: 7px; border-radius: 4px; flex-shrink: 0; }

  .notes-box {
    position: absolute;
    bottom: 22px;
    right: 48px;
    background: #ecfdf5;
    border: 2px solid #a7f3d0;
    border-radius: 14px;
    padding: 16px 24px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.09);
    max-width: 580px;
    font-size: 13px;
    color: #065f46;
    line-height: 1.5;
  }
  .notes-box strong { color: #047857; }
</style>
</head>
<body>

<div class="header">
  <div>
    <h1><span>⚡</span> DIAGRAMA DE MONTAGEM: ESP32 + MÓDULO FONTE MB102 + L298N</h1>
    <div class="subtitle">Alimentação Isolada e Estabilizada para Protoboard (Zero Brownouts / Quedas de Tensão)</div>
  </div>
  <div class="badge">Versão Protoboard + MB102</div>
</div>

<div class="legend-box">
  <div class="legend-title">Identificação dos Fios e Barramentos</div>
  <div class="legend-item"><div class="legend-color" style="background:#ef4444;"></div><strong>Vermelho (+12V/7.4V):</strong> Bateria ➔ Chave Geral ➔ Borne 12V da Ponte H e Entrada Jack do MB102</div>
  <div class="legend-item"><div class="legend-color" style="background:#0f172a;"></div><strong>Preto (GND):</strong> Terra Comum Unificado (Bateria + L298N + MB102 + ESP32)</div>
  <div class="legend-item"><div class="legend-color" style="background:#dc2626;"></div><strong>Vermelho (+5V Regulado):</strong> Saída MB102 (5V) ➔ Barramento (+) da Protoboard ➔ VIN do ESP32</div>
  <div class="legend-item"><div class="legend-color" style="background:#10b981;"></div><strong>Verde:</strong> Fileira D18 da Protoboard ➔ IN1 da Ponte H (Motor Esq Frente)</div>
  <div class="legend-item"><div class="legend-color" style="background:#0284c7;"></div><strong>Azul:</strong> Fileira D19 da Protoboard ➔ IN2 da Ponte H (Motor Esq Ré)</div>
  <div class="legend-item"><div class="legend-color" style="background:#f59e0b;"></div><strong>Laranja:</strong> Fileira D22 da Protoboard ➔ IN3 da Ponte H (Motor Dir Frente)</div>
  <div class="legend-item"><div class="legend-color" style="background:#8b5cf6;"></div><strong>Roxo:</strong> Fileira D23 da Protoboard ➔ IN4 da Ponte H (Motor Dir Ré)</div>
</div>

<div class="notes-box">
  <strong>🛡️ Por que adicionar o Módulo MB102 no Robô de Batalha?</strong><br>
  - <strong>Zero Brownouts / Quedas de Tensão:</strong> O L298N tem um regulador 78M05 fraco que desarma com o tranco dos motores. O MB102 usa reguladores dedicados AMS1117 com capacitores de filtro, mantendo o ESP32 firme mesmo em choque violento.<br>
  - <strong>Isolamento Elétrico:</strong> A saída de +5V do L298N fica <strong>desconectada</strong>. O L298N cuida só da força bruta e o MB102 cuida da eletrônica sensível.<br>
  - <strong>Chave Geral da Lógica:</strong> O botão push-button do MB102 permite ligar/desligar o ESP32 instantaneamente.
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
    <linearGradient id="mb102-pcb" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
  </defs>

  <!-- ======================================================== -->
  <!-- 1. COMPONENTE: PROTOBOARD COM ESP32 (X: 80, Y: 25)       -->
  <!-- ======================================================== -->
  <g id="breadboard-esp32" transform="translate(80, 25)" filter="url(#shadow)">
    <!-- White Breadboard (830 tie-points layout) -->
    <rect x="0" y="0" width="370" height="690" rx="16" fill="#ffffff" stroke="#cbd5e1" stroke-width="3"/>
    
    <!-- Power Rails Left (+ / -) -->
    <line x1="28" y1="120" x2="28" y2="670" stroke="#ef4444" stroke-width="3.5"/>
    <line x1="48" y1="120" x2="48" y2="670" stroke="#3b82f6" stroke-width="3.5"/>
    <text x="28" y="112" font-size="14" font-weight="900" fill="#ef4444" text-anchor="middle">+</text>
    <text x="48" y="112" font-size="14" font-weight="900" fill="#3b82f6" text-anchor="middle">-</text>

    <!-- Power Rails Right (+ / -) -->
    <line x1="322" y1="120" x2="322" y2="670" stroke="#3b82f6" stroke-width="3.5"/>
    <line x1="342" y1="120" x2="342" y2="670" stroke="#ef4444" stroke-width="3.5"/>
    <text x="342" y="112" font-size="14" font-weight="900" fill="#ef4444" text-anchor="middle">+</text>
    <text x="322" y="112" font-size="14" font-weight="900" fill="#3b82f6" text-anchor="middle">-</text>

    <!-- Central Ravine -->
    <rect x="180" y="120" width="10" height="550" rx="2" fill="#e2e8f0"/>

    <!-- Tie-point holes matrix -->
    <g fill="#94a3b8">
      <!-- Left side columns (A, B, C, D, E) -->
      <circle cx="75" cy="170" r="3"/><circle cx="95" cy="170" r="3"/><circle cx="115" cy="170" r="3"/><circle cx="135" cy="170" r="3"/><circle cx="155" cy="170" r="3"/>
      <circle cx="75" cy="200" r="3"/><circle cx="95" cy="200" r="3"/><circle cx="115" cy="200" r="3"/><circle cx="135" cy="200" r="3"/><circle cx="155" cy="200" r="3"/>
      <circle cx="75" cy="230" r="3"/><circle cx="95" cy="230" r="3"/><circle cx="115" cy="230" r="3"/><circle cx="135" cy="230" r="3"/><circle cx="155" cy="230" r="3"/>
      <circle cx="75" cy="260" r="3"/><circle cx="95" cy="260" r="3"/><circle cx="115" cy="260" r="3"/><circle cx="135" cy="260" r="3"/><circle cx="155" cy="260" r="3"/>
      <circle cx="75" cy="290" r="3"/><circle cx="95" cy="290" r="3"/><circle cx="115" cy="290" r="3"/><circle cx="135" cy="290" r="3"/><circle cx="155" cy="290" r="3"/>
      <circle cx="75" cy="320" r="3"/><circle cx="95" cy="320" r="3"/><circle cx="115" cy="320" r="3"/><circle cx="135" cy="320" r="3"/><circle cx="155" cy="320" r="3"/>
      <circle cx="75" cy="350" r="3"/><circle cx="95" cy="350" r="3"/><circle cx="115" cy="350" r="3"/><circle cx="135" cy="350" r="3"/><circle cx="155" cy="350" r="3"/>
      <circle cx="75" cy="380" r="3"/><circle cx="95" cy="380" r="3"/><circle cx="115" cy="380" r="3"/><circle cx="135" cy="380" r="3"/><circle cx="155" cy="380" r="3"/>
      <circle cx="75" cy="410" r="3"/><circle cx="95" cy="410" r="3"/><circle cx="115" cy="410" r="3"/><circle cx="135" cy="410" r="3"/><circle cx="155" cy="410" r="3"/>
      <circle cx="75" cy="440" r="3"/><circle cx="95" cy="440" r="3"/><circle cx="115" cy="440" r="3"/><circle cx="135" cy="440" r="3"/><circle cx="155" cy="440" r="3"/>
      <circle cx="75" cy="470" r="3"/><circle cx="95" cy="470" r="3"/><circle cx="115" cy="470" r="3"/><circle cx="135" cy="470" r="3"/><circle cx="155" cy="470" r="3"/>
      <circle cx="75" cy="500" r="3"/><circle cx="95" cy="500" r="3"/><circle cx="115" cy="500" r="3"/><circle cx="135" cy="500" r="3"/><circle cx="155" cy="500" r="3"/>
      <circle cx="75" cy="530" r="3"/><circle cx="95" cy="530" r="3"/><circle cx="115" cy="530" r="3"/><circle cx="135" cy="530" r="3"/><circle cx="155" cy="530" r="3"/>
      <circle cx="75" cy="560" r="3"/><circle cx="95" cy="560" r="3"/><circle cx="115" cy="560" r="3"/><circle cx="135" cy="560" r="3"/><circle cx="155" cy="560" r="3"/>
      <circle cx="75" cy="590" r="3"/><circle cx="95" cy="590" r="3"/><circle cx="115" cy="590" r="3"/><circle cx="135" cy="590" r="3"/><circle cx="155" cy="590" r="3"/>

      <!-- Right side columns (F, G, H, I, J) -->
      <circle cx="215" cy="170" r="3"/><circle cx="235" cy="170" r="3"/><circle cx="255" cy="170" r="3"/><circle cx="275" cy="170" r="3"/><circle cx="295" cy="170" r="3"/>
      <circle cx="215" cy="200" r="3"/><circle cx="235" cy="200" r="3"/><circle cx="255" cy="200" r="3"/><circle cx="275" cy="200" r="3"/><circle cx="295" cy="200" r="3"/>
      <circle cx="215" cy="230" r="3"/><circle cx="235" cy="230" r="3"/><circle cx="255" cy="230" r="3"/><circle cx="275" cy="230" r="3"/><circle cx="295" cy="230" r="3"/>
      <circle cx="215" cy="260" r="3"/><circle cx="235" cy="260" r="3"/><circle cx="255" cy="260" r="3"/><circle cx="275" cy="260" r="3"/><circle cx="295" cy="260" r="3"/>
      <circle cx="215" cy="290" r="3"/><circle cx="235" cy="290" r="3"/><circle cx="255" cy="290" r="3"/><circle cx="275" cy="290" r="3"/><circle cx="295" cy="290" r="3"/>
      <circle cx="215" cy="320" r="3"/><circle cx="235" cy="320" r="3"/><circle cx="255" cy="320" r="3"/><circle cx="275" cy="320" r="3"/><circle cx="295" cy="320" r="3"/>
      <circle cx="215" cy="350" r="3"/><circle cx="235" cy="350" r="3"/><circle cx="255" cy="350" r="3"/><circle cx="275" cy="350" r="3"/><circle cx="295" cy="350" r="3"/>
      <circle cx="215" cy="380" r="3"/><circle cx="235" cy="380" r="3"/><circle cx="255" cy="380" r="3"/><circle cx="275" cy="380" r="3"/><circle cx="295" cy="380" r="3"/>
      <circle cx="215" cy="410" r="3"/><circle cx="235" cy="410" r="3"/><circle cx="255" cy="410" r="3"/><circle cx="275" cy="410" r="3"/><circle cx="295" cy="410" r="3"/>
      <circle cx="215" cy="440" r="3"/><circle cx="235" cy="440" r="3"/><circle cx="255" cy="440" r="3"/><circle cx="275" cy="440" r="3"/><circle cx="295" cy="440" r="3"/>
      <circle cx="215" cy="470" r="3"/><circle cx="235" cy="470" r="3"/><circle cx="255" cy="470" r="3"/><circle cx="275" cy="470" r="3"/><circle cx="295" cy="470" r="3"/>
      <circle cx="215" cy="500" r="3"/><circle cx="235" cy="500" r="3"/><circle cx="255" cy="500" r="3"/><circle cx="275" cy="500" r="3"/><circle cx="295" cy="500" r="3"/>
      <circle cx="215" cy="530" r="3"/><circle cx="235" cy="530" r="3"/><circle cx="255" cy="530" r="3"/><circle cx="275" cy="530" r="3"/><circle cx="295" cy="530" r="3"/>
      <circle cx="215" cy="560" r="3"/><circle cx="235" cy="560" r="3"/><circle cx="255" cy="560" r="3"/><circle cx="275" cy="560" r="3"/><circle cx="295" cy="560" r="3"/>
      <circle cx="215" cy="590" r="3"/><circle cx="235" cy="590" r="3"/><circle cx="255" cy="590" r="3"/><circle cx="275" cy="590" r="3"/><circle cx="295" cy="590" r="3"/>
    </g>

    <!-- ==================================================== -->
    <!-- MÓDULO FONTE DE ALIMENTAÇÃO MB-102 (ENCAIXADO NO TOPO)-->
    <!-- ==================================================== -->
    <g id="mb102-module" transform="translate(0, 0)">
      <!-- Main Shaped PCB -->
      <path d="M 10,12 H 360 C 365,12 368,16 368,22 V 95 C 368,100 364,104 358,104 H 305 V 82 H 65 V 104 H 12 C 6,104 2,100 2,95 V 22 C 2,16 5,12 10,12 Z" 
            fill="url(#mb102-pcb)" stroke="#475569" stroke-width="2.5"/>

      <!-- Labeling -->
      <text x="185" y="32" font-size="14" font-weight="900" fill="#f8fafc" text-anchor="middle" letter-spacing="1">MÓDULO FONTE MB-102</text>
      <text x="185" y="47" font-size="10.5" font-weight="bold" fill="#38bdf8" text-anchor="middle">REGULADOR DE TENSÃO PROTOBOARD (5V / 3.3V)</text>

      <!-- DC Barrel Jack (P4 2.1mm) Input (Left) -->
      <rect x="14" y="24" width="46" height="64" rx="5" fill="#020617" stroke="#334155" stroke-width="2"/>
      <circle cx="37" cy="56" r="14" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
      <circle cx="37" cy="56" r="5" fill="#facc15"/>
      <text x="37" y="18" font-size="10" font-weight="900" fill="#fde047" text-anchor="middle">JACK P4</text>
      <text x="37" y="98" font-size="8.5" font-weight="bold" fill="#94a3b8" text-anchor="middle">6.5V - 12V</text>

      <!-- USB Type-A Port -->
      <rect x="68" y="28" width="44" height="38" rx="4" fill="#94a3b8" stroke="#475569" stroke-width="2"/>
      <rect x="74" y="35" width="32" height="24" rx="2" fill="#0f172a"/>
      <rect x="78" y="42" width="24" height="6" fill="#ffffff"/>
      <text x="90" y="22" font-size="9" font-weight="bold" fill="#94a3b8" text-anchor="middle">USB 5V</text>

      <!-- Latching Push Switch (Chave Liga/Desliga) -->
      <rect x="120" y="48" width="28" height="28" rx="4" fill="#334155" stroke="#1e293b" stroke-width="1.5"/>
      <circle cx="134" cy="62" r="9" fill="#ef4444" stroke="#991b1b" stroke-width="2"/>
      <text x="134" y="42" font-size="9" font-weight="bold" fill="#fca5a5" text-anchor="middle">POWER</text>

      <!-- Power Indicator LED (Green) -->
      <circle cx="168" cy="62" r="5.5" fill="#22c55e" stroke="#15803d" stroke-width="1.5"/>
      <circle cx="168" cy="62" r="11" fill="none" stroke="#22c55e" stroke-width="1" opacity="0.6"/>
      <text x="168" y="78" font-size="8.5" font-weight="bold" fill="#86efac" text-anchor="middle">ON</text>

      <!-- AMS1117 Regulators (SOT-223) -->
      <rect x="195" y="52" width="22" height="22" rx="3" fill="#0f172a" stroke="#334155"/>
      <rect x="201" y="49" width="10" height="3" fill="#94a3b8"/>
      <text x="206" y="66" font-size="7.5" font-weight="bold" fill="#94a3b8" text-anchor="middle">5.0V</text>

      <rect x="225" y="52" width="22" height="22" rx="3" fill="#0f172a" stroke="#334155"/>
      <rect x="231" y="49" width="10" height="3" fill="#94a3b8"/>
      <text x="236" y="66" font-size="7.5" font-weight="bold" fill="#94a3b8" text-anchor="middle">3.3V</text>

      <!-- Left Rail Jumper Selector (Set to 5V) -->
      <g transform="translate(14, 102)">
        <rect x="0" y="0" width="36" height="24" rx="3" fill="#020617" stroke="#334155"/>
        <!-- Yellow Jumper Cap on 5V Position -->
        <rect x="2" y="2" width="15" height="20" rx="3" fill="#eab308" stroke="#ca8a04" stroke-width="1.5"/>
        <text x="9" y="15" font-size="8.5" font-weight="900" fill="#000" text-anchor="middle">5V</text>
        <text x="26" y="15" font-size="7.5" font-weight="bold" fill="#64748b" text-anchor="middle">3V3</text>
      </g>
      <!-- Plug Pins into Left Rail -->
      <circle cx="28" cy="132" r="4.5" fill="#ef4444" stroke="#991b1b" stroke-width="1.5"/>
      <circle cx="48" cy="132" r="4.5" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>

      <!-- Right Rail Jumper Selector (Set to 5V) -->
      <g transform="translate(320, 102)">
        <rect x="0" y="0" width="36" height="24" rx="3" fill="#020617" stroke="#334155"/>
        <!-- Yellow Jumper Cap on 5V Position -->
        <rect x="2" y="2" width="15" height="20" rx="3" fill="#eab308" stroke="#ca8a04" stroke-width="1.5"/>
        <text x="9" y="15" font-size="8.5" font-weight="900" fill="#000" text-anchor="middle">5V</text>
        <text x="26" y="15" font-size="7.5" font-weight="bold" fill="#64748b" text-anchor="middle">3V3</text>
      </g>
      <!-- Plug Pins into Right Rail -->
      <circle cx="322" cy="132" r="4.5" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>
      <circle cx="342" cy="132" r="4.5" fill="#ef4444" stroke="#991b1b" stroke-width="1.5"/>
    </g>

    <!-- ==================================================== -->
    <!-- ESP32 SEATED IN THE MIDDLE OF THE PROTOBOARD         -->
    <!-- ==================================================== -->
    <g id="mounted-esp32" transform="translate(100, 150)">
      <!-- Black PCB of ESP32 -->
      <rect x="0" y="0" width="170" height="490" rx="10" fill="#18181b" stroke="#3f3f46" stroke-width="2.5"/>
      
      <!-- ESP Metal Shield -->
      <rect x="25" y="25" width="120" height="130" rx="6" fill="#e2e8f0" stroke="#94a3b8" stroke-width="2"/>
      <rect x="35" y="6" width="100" height="24" rx="3" fill="#18181b"/>
      <path d="M 50,15 H 120 M 60,10 V 22 M 80,10 V 22 M 100,10 V 22" stroke="#eab308" stroke-width="2" fill="none"/>
      <text x="85" y="80" font-size="13" font-weight="900" fill="#0f172a" text-anchor="middle">ESP-WROOM-32</text>
      <text x="85" y="102" font-size="11" font-weight="bold" fill="#475569" text-anchor="middle">Wi-Fi &amp; WebSockets</text>

      <!-- USB Connector -->
      <rect x="55" y="465" width="60" height="30" rx="4" fill="#94a3b8" stroke="#475569" stroke-width="1.5"/>

      <!-- Board Name -->
      <text x="85" y="210" font-size="15" font-weight="900" fill="#ffffff" text-anchor="middle" letter-spacing="1">ESP32 DevKit</text>

      <!-- Buttons -->
      <rect x="20" y="430" width="22" height="16" rx="3" fill="#ef4444"/>
      <text x="31" y="458" font-size="9" font-weight="bold" fill="#94a3b8" text-anchor="middle">EN</text>
      <rect x="128" y="430" width="22" height="16" rx="3" fill="#3b82f6"/>
      <text x="139" y="458" font-size="9" font-weight="bold" fill="#94a3b8" text-anchor="middle">BOOT</text>

      <!-- Left Pins -->
      <g font-size="9.5" font-family="monospace" font-weight="bold" fill="#cbd5e1">
        <circle cx="8" cy="45" r="5" fill="#eab308"/><text x="18" y="48">3V3</text>
        <circle cx="8" cy="73" r="5" fill="#eab308"/><text x="18" y="76">EN</text>
        <circle cx="8" cy="101" r="5" fill="#eab308"/><text x="18" y="104">VP</text>
        <circle cx="8" cy="129" r="5" fill="#eab308"/><text x="18" y="132">VN</text>
        <circle cx="8" cy="157" r="5" fill="#eab308"/><text x="18" y="160">D34</text>
        <circle cx="8" cy="185" r="5" fill="#eab308"/><text x="18" y="188">D35</text>
        <circle cx="8" cy="213" r="5" fill="#eab308"/><text x="18" y="216">D32</text>
        <circle cx="8" cy="241" r="5" fill="#eab308"/><text x="18" y="244">D33</text>
        <circle cx="8" cy="269" r="5" fill="#eab308"/><text x="18" y="272">D25</text>
        <circle cx="8" cy="297" r="6" fill="#f97316" stroke="#c2410c" stroke-width="1.5"/><text x="18" y="300" fill="#fdba74">D26</text>
        <circle cx="8" cy="325" r="5" fill="#eab308"/><text x="18" y="328">D27</text>
        <circle cx="8" cy="353" r="5" fill="#eab308"/><text x="18" y="356">D14</text>
        <circle cx="8" cy="381" r="5" fill="#eab308"/><text x="18" y="384">D12</text>
        <circle cx="8" cy="409" r="5" fill="#eab308"/><text x="18" y="412">D13</text>
        <circle cx="8" cy="437" r="5" fill="#64748b"/><text x="18" y="440" fill="#94a3b8">GND</text>
      </g>

      <!-- Right Pins (VIN, GND, D18, D19, D22, D23...) -->
      <g font-size="10" font-family="monospace" font-weight="bold">
        <!-- VIN -->
        <circle cx="162" cy="45" r="6.5" fill="#ef4444" stroke="#991b1b" stroke-width="1.5"/>
        <text x="150" y="48" fill="#fca5a5" text-anchor="end">VIN</text>
        <!-- GND -->
        <circle cx="162" cy="73" r="6.5" fill="#0f172a" stroke="#ffffff" stroke-width="1.5"/>
        <text x="150" y="76" fill="#ffffff" text-anchor="end">GND</text>

        <circle cx="162" cy="101" r="5" fill="#eab308"/><text x="150" y="104" fill="#cbd5e1" text-anchor="end">D15</text>
        <circle cx="162" cy="129" r="5" fill="#3b82f6"/><text x="150" y="132" fill="#93c5fd" text-anchor="end">D2</text>
        <circle cx="162" cy="157" r="5" fill="#eab308"/><text x="150" y="160" fill="#cbd5e1" text-anchor="end">D4</text>
        <circle cx="162" cy="185" r="5" fill="#eab308"/><text x="150" y="188" fill="#cbd5e1" text-anchor="end">RX2</text>
        <circle cx="162" cy="213" r="5" fill="#eab308"/><text x="150" y="216" fill="#cbd5e1" text-anchor="end">TX2</text>
        <circle cx="162" cy="241" r="5" fill="#eab308"/><text x="150" y="244" fill="#cbd5e1" text-anchor="end">D5</text>

        <!-- D18 (IN1) -->
        <circle cx="162" cy="269" r="7" fill="#10b981" stroke="#065f46" stroke-width="2"/>
        <text x="150" y="272" fill="#6ee7b7" text-anchor="end">D18</text>

        <!-- D19 (IN2) -->
        <circle cx="162" cy="297" r="7" fill="#0284c7" stroke="#075985" stroke-width="2"/>
        <text x="150" y="300" fill="#7dd3fc" text-anchor="end">D19</text>

        <circle cx="162" cy="325" r="5" fill="#eab308"/><text x="150" y="328" fill="#cbd5e1" text-anchor="end">D21</text>
        <circle cx="162" cy="353" r="5" fill="#eab308"/><text x="150" y="356" fill="#cbd5e1" text-anchor="end">RX0</text>
        <circle cx="162" cy="381" r="5" fill="#eab308"/><text x="150" y="384" fill="#cbd5e1" text-anchor="end">TX0</text>

        <!-- D22 (IN3) -->
        <circle cx="162" cy="409" r="7" fill="#f59e0b" stroke="#92400e" stroke-width="2"/>
        <text x="150" y="412" fill="#fde68a" text-anchor="end">D22</text>

        <!-- D23 (IN4) -->
        <circle cx="162" cy="437" r="7" fill="#8b5cf6" stroke="#5b21b6" stroke-width="2"/>
        <text x="150" y="440" fill="#ddd6fe" text-anchor="end">D23</text>
      </g>
    </g>

    <!-- Jumpers on Breadboard: VIN to (+) Rail & GND to (-) Rail -->
    <!-- VIN pin row connects to Right (+) Rail -->
    <path d="M 275, 195 H 342" fill="none" stroke="#ef4444" stroke-width="4.5" stroke-linecap="round"/>
    <circle cx="342" cy="195" r="4.5" fill="#ef4444"/>
    <circle cx="275" cy="195" r="4.5" fill="#ef4444"/>

    <!-- GND pin row connects to Right (-) Rail -->
    <path d="M 275, 223 H 322" fill="none" stroke="#0f172a" stroke-width="4.5" stroke-linecap="round"/>
    <circle cx="322" cy="223" r="4.5" fill="#0f172a"/>
    <circle cx="275" cy="223" r="4.5" fill="#0f172a"/>
  </g>

  <!-- ======================================================== -->
  <!-- 2. COMPONENTE: PONTE H L298N (X: 840, Y: 180)            -->
  <!-- ======================================================== -->
  <g id="l298n" transform="translate(840, 180)" filter="url(#shadow)">
    <!-- Red PCB -->
    <rect x="0" y="0" width="380" height="380" rx="14" fill="#b91c1c" stroke="#7f1d1d" stroke-width="3"/>
    
    <!-- Large Black Aluminum Heatsink -->
    <rect x="80" y="45" width="220" height="155" rx="6" fill="url(#heatsink-grad)" stroke="#0f172a" stroke-width="2"/>
    <!-- Fins -->
    <line x1="110" y1="45" x2="110" y2="200" stroke="#475569" stroke-width="4"/>
    <line x1="140" y1="45" x2="140" y2="200" stroke="#475569" stroke-width="4"/>
    <line x1="170" y1="45" x2="170" y2="200" stroke="#475569" stroke-width="4"/>
    <line x1="200" y1="45" x2="200" y2="200" stroke="#475569" stroke-width="4"/>
    <line x1="230" y1="45" x2="230" y2="200" stroke="#475569" stroke-width="4"/>
    <line x1="260" y1="45" x2="260" y2="200" stroke="#475569" stroke-width="4"/>

    <!-- L298N IC with metal tab -->
    <rect x="135" y="180" width="110" height="40" rx="4" fill="#020617"/>
    <text x="190" y="206" font-size="16" font-weight="900" fill="#ffffff" text-anchor="middle" letter-spacing="2">L298N</text>

    <!-- Electrolytic Filter Capacitors -->
    <circle cx="55" cy="225" r="26" fill="#1e293b" stroke="#0f172a" stroke-width="2.5"/>
    <path d="M 45,205 H 65" stroke="#94a3b8" stroke-width="3"/>
    <circle cx="325" cy="225" r="26" fill="#1e293b" stroke="#0f172a" stroke-width="2.5"/>

    <!-- Screw Terminal Left (Motor A - OUT1 / OUT2) -->
    <rect x="-18" y="210" width="36" height="85" rx="5" fill="#1d4ed8" stroke="#172554" stroke-width="2"/>
    <circle cx="0" cy="232" r="9" fill="#93c5fd" stroke="#1e3a8a" stroke-width="1.5"/>
    <circle cx="0" cy="272" r="9" fill="#93c5fd" stroke="#1e3a8a" stroke-width="1.5"/>
    <text x="26" y="236" font-size="11" font-weight="900" fill="#ffffff">OUT1</text>
    <text x="26" y="276" font-size="11" font-weight="900" fill="#ffffff">OUT2</text>

    <!-- Screw Terminal Right (Motor B - OUT3 / OUT4) -->
    <rect x="362" y="210" width="36" height="85" rx="5" fill="#1d4ed8" stroke="#172554" stroke-width="2"/>
    <circle cx="380" cy="232" r="9" fill="#93c5fd" stroke="#1e3a8a" stroke-width="1.5"/>
    <circle cx="380" cy="272" r="9" fill="#93c5fd" stroke="#1e3a8a" stroke-width="1.5"/>
    <text x="354" y="236" font-size="11" font-weight="900" fill="#ffffff" text-anchor="end">OUT3</text>
    <text x="354" y="276" font-size="11" font-weight="900" fill="#ffffff" text-anchor="end">OUT4</text>

    <!-- Screw Terminal Power 3-pin (Bottom) -->
    <rect x="25" y="320" width="145" height="48" rx="5" fill="#1d4ed8" stroke="#172554" stroke-width="2"/>
    <circle cx="48" cy="335" r="12" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>
    <text x="48" y="366" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">+12V</text>
    <circle cx="97" cy="335" r="12" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>
    <text x="97" y="366" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">GND</text>
    <circle cx="145" cy="335" r="12" fill="#64748b" stroke="#334155" stroke-width="2"/>
    <text x="145" y="366" font-size="10" font-weight="bold" fill="#fca5a5" text-anchor="middle">+5V(Vazio)</text>

    <!-- Logic Header -->
    <rect x="185" y="325" width="170" height="42" rx="5" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <rect x="192" y="318" width="18" height="26" rx="3" fill="#020617" stroke="#facc15" stroke-width="1.5"/>
    <text x="201" y="312" font-size="10" font-weight="900" fill="#fde047" text-anchor="middle">ENA</text>

    <circle cx="230" cy="346" r="7" fill="#10b981" stroke="#065f46" stroke-width="2"/>
    <text x="230" y="312" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">IN1</text>
    <circle cx="256" cy="346" r="7" fill="#0284c7" stroke="#075985" stroke-width="2"/>
    <text x="256" y="312" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">IN2</text>
    <circle cx="282" cy="346" r="7" fill="#f59e0b" stroke="#92400e" stroke-width="2"/>
    <text x="282" y="312" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">IN3</text>
    <circle cx="308" cy="346" r="7" fill="#8b5cf6" stroke="#5b21b6" stroke-width="2"/>
    <text x="308" y="312" font-size="11" font-weight="900" fill="#ffffff" text-anchor="middle">IN4</text>

    <rect x="328" y="318" width="18" height="26" rx="3" fill="#020617" stroke="#facc15" stroke-width="1.5"/>
    <text x="337" y="312" font-size="10" font-weight="900" fill="#fde047" text-anchor="middle">ENB</text>
  </g>

  <!-- ======================================================== -->
  <!-- 3. COMPONENTE: BATERIA LiPo 7.4V E CHAVE GERAL           -->
  <!-- ======================================================== -->
  <g id="battery" transform="translate(680, 680)" filter="url(#shadow)">
    <rect x="0" y="0" width="230" height="115" rx="14" fill="url(#lipo-grad)" stroke="#1e3a8a" stroke-width="3"/>
    <text x="115" y="46" font-size="18" font-weight="900" fill="#ffffff" text-anchor="middle">BATERIA LiPo 2S</text>
    <text x="115" y="72" font-size="16" font-weight="bold" fill="#93c5fd" text-anchor="middle">7.4V - 1500mAh</text>
    <rect x="35" y="84" width="160" height="18" rx="4" fill="#1e3a8a"/>
    <text x="115" y="97" font-size="11" font-weight="bold" fill="#bfdbfe" text-anchor="middle">ALTA DESCARGA (30C)</text>

    <rect x="-12" y="32" width="14" height="16" rx="2" fill="#ef4444"/>
    <rect x="-12" y="70" width="14" height="16" rx="2" fill="#0f172a"/>
  </g>

  <g id="switch" transform="translate(520, 690)" filter="url(#shadow)">
    <rect x="0" y="0" width="90" height="65" rx="8" fill="#334155" stroke="#1e293b" stroke-width="2.5"/>
    <circle cx="45" cy="32" r="18" fill="#dc2626" stroke="#991b1b" stroke-width="2.5"/>
    <rect x="40" y="10" width="10" height="26" rx="5" fill="#f87171"/>
    <text x="45" y="58" font-size="10" font-weight="900" fill="#ffffff" text-anchor="middle">CHAVE GERAL</text>
  </g>

  <!-- ======================================================== -->
  <!-- 4. MOTORES DC COM RODAS (TT MOTORS)                      -->
  <!-- ======================================================== -->
  <g id="motor-left" transform="translate(1480, 110)" filter="url(#shadow)">
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

  <g id="motor-right" transform="translate(1480, 390)" filter="url(#shadow)">
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
  <!-- 5. FIAÇÃO (WIRES)                                        -->
  <!-- ======================================================== -->
  <g id="wires" filter="url(#wire-shadow)">
    <!-- Bateria (+) -> Chave Geral -->
    <path d="M 668, 712 H 610" fill="none" stroke="#ef4444" stroke-width="6" stroke-linecap="round"/>

    <!-- Chave Geral -> Split: 
         1) Para L298N 12V (888, 515)
         2) Para MB102 Jack P4 (+) (117, 81) -->
    <path d="M 520, 722 H 470 V 610 H 888 V 515" fill="none" stroke="#ef4444" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
    
    <!-- Linha de Alimentação MB102 Jack (+) -->
    <path d="M 470, 610 V 100 H 117" fill="none" stroke="#ef4444" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="117" cy="100" r="5" fill="#ef4444"/>

    <!-- Bateria (-) -> Split:
         1) Para L298N GND (937, 515)
         2) Para MB102 Jack P4 (-) (95, 81) -->
    <path d="M 668, 750 H 450 V 630 H 937 V 515" fill="none" stroke="#0f172a" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
    
    <!-- Linha de Terra MB102 Jack (-) -->
    <path d="M 450, 630 V 80 H 95" fill="none" stroke="#0f172a" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="95" cy="80" r="5" fill="#0f172a"/>

    <!-- D18 Row on Breadboard (355, 419) -> L298N IN1 (1070, 526) -->
    <path d="M 355, 419 H 700 V 465 H 1070 V 526" fill="none" stroke="#10b981" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="355" cy="419" r="5" fill="#10b981"/>

    <!-- D19 Row on Breadboard (355, 447) -> L298N IN2 (1096, 526) -->
    <path d="M 355, 447 H 720 V 480 H 1096 V 526" fill="none" stroke="#0284c7" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="355" cy="447" r="5" fill="#0284c7"/>

    <!-- D22 Row on Breadboard (355, 559) -> L298N IN3 (1122, 526) -->
    <path d="M 355, 559 H 740 V 495 H 1122 V 526" fill="none" stroke="#f59e0b" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="355" cy="559" r="5" fill="#f59e0b"/>

    <!-- D23 Row on Breadboard (355, 587) -> L298N IN4 (1148, 526) -->
    <path d="M 355, 587 H 760 V 510 H 1148 V 526" fill="none" stroke="#8b5cf6" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="355" cy="587" r="5" fill="#8b5cf6"/>

    <!-- Motor Esquerdo OUT1 & OUT2 -->
    <path d="M 822, 412 H 780 V 135 H 1450 V 178 H 1488" fill="none" stroke="#ef4444" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M 822, 452 H 760 V 120 H 1430 V 212 H 1488" fill="none" stroke="#0f172a" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- Motor Direito OUT3 & OUT4 -->
    <path d="M 1228, 412 H 1320 V 458 H 1488" fill="none" stroke="#ef4444" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M 1228, 452 H 1300 V 492 H 1488" fill="none" stroke="#0f172a" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <!-- Labels on wires -->
  <g font-size="11" font-weight="bold" text-anchor="middle">
    <rect x="250" y="68" width="165" height="22" rx="4" fill="#ffffff" stroke="#ef4444" stroke-width="1.5"/>
    <text x="332" y="83" fill="#b91c1c">+7.4V Bateria ➔ Jack MB102</text>

    <rect x="250" y="94" width="165" height="22" rx="4" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>
    <text x="332" y="109" fill="#0f172a">GND Bateria ➔ Jack MB102</text>

    <rect x="780" y="444" width="130" height="18" rx="4" fill="#ffffff" stroke="#10b981" stroke-width="1.5"/>
    <text x="845" y="457" fill="#059669">Fila D18 ➔ IN1</text>

    <rect x="780" y="464" width="130" height="18" rx="4" fill="#ffffff" stroke="#0284c7" stroke-width="1.5"/>
    <text x="845" y="477" fill="#0284c7">Fila D19 ➔ IN2</text>

    <rect x="780" y="484" width="130" height="18" rx="4" fill="#ffffff" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="845" y="497" fill="#d97706">Fila D22 ➔ IN3</text>

    <rect x="780" y="504" width="130" height="18" rx="4" fill="#ffffff" stroke="#8b5cf6" stroke-width="1.5"/>
    <text x="845" y="517" fill="#7c3aed">Fila D23 ➔ IN4</text>

    <!-- Callout explaining L298N 5V isolated -->
    <rect x="940" y="545" width="220" height="26" rx="5" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5"/>
    <text x="1050" y="562" font-size="11" font-weight="900" fill="#dc2626">5V do L298N: NÃO CONECTADO!</text>
  </g>
</svg>

</body>
</html>
"""

def generate():
    os.makedirs("docs/images", exist_ok=True)
    with open("docs/diagrama_esp32_protoboard.html", "w", encoding="utf-8") as f:
        f.write(HTML_ESP32_MB102)

    print("HTML written. Capturing with Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto("file:///" + os.path.abspath("docs/diagrama_esp32_protoboard.html").replace("\\", "/"))
        page.wait_for_timeout(300)
        page.screenshot(path="docs/images/circuito_esp32_protoboard.jpg", type="jpeg", quality=95)
        page.screenshot(path="circuito_esp32_protoboard.jpg", type="jpeg", quality=95)
        print("ESP32 Protoboard with MB102 captured successfully!")
        browser.close()

if __name__ == "__main__":
    generate()
