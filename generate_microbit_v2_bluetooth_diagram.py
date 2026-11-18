import os
import shutil
from playwright.sync_api import sync_playwright

HTML_V2_BLE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; }
  body {
    width: 1920px;
    height: 1080px;
    background-color: #0b1120;
    background-image: radial-gradient(#1e293b 1.5px, transparent 1.5px);
    background-size: 28px 28px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
    color: #f8fafc;
  }
  
  .header {
    background: #020617;
    color: white;
    padding: 18px 48px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 4px solid #38bdf8;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
  }
  .header h1 { font-size: 28px; letter-spacing: 1px; display: flex; align-items: center; gap: 14px; font-weight: 800; }
  .header .badge {
    background: #38bdf8;
    color: #020617;
    font-size: 14px;
    font-weight: 900;
    padding: 7px 18px;
    border-radius: 8px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
  }
  .header .subtitle { font-size: 15px; color: #94a3b8; margin-top: 3px; }

  svg {
    width: 1920px;
    height: 990px;
    position: absolute;
    top: 86px;
    left: 0;
  }

  .legend-box {
    position: absolute;
    bottom: 24px;
    left: 48px;
    background: rgba(15, 23, 42, 0.95);
    border: 2px solid #334155;
    border-radius: 14px;
    padding: 18px 24px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.5);
    display: flex;
    flex-direction: column;
    gap: 8px;
    font-size: 13.5px;
    max-width: 600px;
  }
  .legend-title { font-weight: 800; font-size: 16px; color: #38bdf8; margin-bottom: 2px; border-bottom: 2px solid #334155; padding-bottom: 5px; }
  .legend-item { display: flex; align-items: center; gap: 10px; color: #cbd5e1; }
  .legend-color { width: 24px; height: 8px; border-radius: 4px; flex-shrink: 0; }

  .notes-box {
    position: absolute;
    bottom: 24px;
    right: 48px;
    background: rgba(12, 74, 110, 0.85);
    border: 2px solid #0284c7;
    border-radius: 14px;
    padding: 18px 24px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.4);
    max-width: 640px;
    font-size: 13px;
    color: #f0f9ff;
    line-height: 1.5;
  }
  .notes-box strong { color: #38bdf8; }
</style>
</head>
<body>

<div class="header">
  <div>
    <h1><span>📱</span> SISTEMA BBC MICRO:BIT V2: PILOTAGEM DIRETA PELO CELULAR (BLUETOOTH BLE)</h1>
    <div class="subtitle">Sem necessidade de segundo micro:bit | Web Bluetooth no Chrome | Joystick Touch 360° | Shield Robo:Bit ou L298N</div>
  </div>
  <div class="badge">MICRO:BIT V2 + SMARTPHONE</div>
</div>

<div class="legend-box">
  <div class="legend-title">Vantagens & Arquitetura Bluetooth Low Energy</div>
  <div class="legend-item"><div class="legend-color" style="background:#38bdf8;"></div><strong>Zero Hardware Adicional:</strong> Apenas 1 placa micro:bit V2 instalada no chassi do robô.</div>
  <div class="legend-item"><div class="legend-color" style="background:#10b981;"></div><strong>Web Bluetooth Nativo:</strong> Abre no Chrome/Samsung Internet (Android/PC) sem instalar nada.</div>
  <div class="legend-item"><div class="legend-color" style="background:#f59e0b;"></div><strong>Nordic UART Service (NUS):</strong> Canal serial sem fio de alta velocidade e baixa latência.</div>
  <div class="legend-item"><div class="legend-color" style="background:#ef4444;"></div><strong>Failsafe Watchdog (500ms):</strong> Se o celular desconectar, os motores cortam a tração na hora.</div>
</div>

<div class="notes-box">
  <strong>💡 Como Funciona a Conexão:</strong><br>
  - <strong>Configuração MakeCode:</strong> Ative a opção <code>No Pairing Required</code> nas configurações do projeto para conectar o celular sem código PIN.<br>
  - <strong>Controle Completo na Tela:</strong> O celular transmite pacotes <code>D:&lt;velL&gt;,&lt;velR&gt;</code> para o joystick e comandos <code>TURBO</code>, <code>T180</code> e <code>ARMA_ON</code>.<br>
  - <strong>Compatibilidade Total:</strong> Suporta tanto o <strong>Shield 4tronix Robo:Bit</strong> quanto a ponte H clássica <strong>L298N / TB6612FNG</strong>.
</div>

<svg viewBox="0 0 1920 990">
  <defs>
    <filter id="shadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="4" dy="8" stdDeviation="8" flood-color="#000000" flood-opacity="0.6"/>
    </filter>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
    <linearGradient id="phone-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#090d16"/>
    </linearGradient>
    <linearGradient id="ble-wave" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.1"/>
    </linearGradient>
  </defs>

  <!-- ======================================================== -->
  <!-- 1. ONDAS DE BLUETOOTH BLE (ENTRE CELULAR E MICRO:BIT)    -->
  <!-- ======================================================== -->
  <g transform="translate(560, 290)">
    <!-- Linhas de ondas de rádio BLE -->
    <path d="M 0,20 C 80,-20 180,-20 260,20" fill="none" stroke="#38bdf8" stroke-width="4" stroke-dasharray="8 6" opacity="0.8" filter="url(#glow)"/>
    <path d="M 20,45 C 90,15 170,15 240,45" fill="none" stroke="#06b6d4" stroke-width="5" stroke-linecap="round" opacity="0.9"/>
    <path d="M 40,70 C 100,50 160,50 220,70" fill="none" stroke="#38bdf8" stroke-width="6" stroke-linecap="round"/>
    
    <!-- Ícone Bluetooth Central -->
    <rect x="95" y="80" width="70" height="70" rx="35" fill="#0284c7" filter="url(#shadow)"/>
    <path d="M 125,95 V 135 L 140,123 L 118,107 L 140,92 Z" fill="none" stroke="#ffffff" stroke-width="3.5" stroke-linejoin="round"/>
    <line x1="125" y1="107" x2="140" y2="123" stroke="#ffffff" stroke-width="3.5"/>
    <line x1="125" y1="123" x2="140" y2="107" stroke="#ffffff" stroke-width="3.5"/>

    <text x="130" y="175" font-size="13" font-weight="900" fill="#38bdf8" text-anchor="middle" letter-spacing="1">BLUETOOTH 5.0 BLE</text>
    <text x="130" y="195" font-size="11" font-weight="bold" fill="#94a3b8" text-anchor="middle">Nordic UART Service (NUS)</text>
    <text x="130" y="215" font-size="10" font-weight="bold" fill="#4ade80" text-anchor="middle">Latência Ultra-Baixa &lt;15ms</text>
  </g>

  <!-- ======================================================== -->
  <!-- 2. CELULAR / SMARTPHONE (À ESQUERDA)                     -->
  <!-- ======================================================== -->
  <g id="smartphone" transform="translate(140, 100)" filter="url(#shadow)">
    <!-- Corpo do Celular -->
    <rect x="0" y="0" width="380" height="660" rx="42" fill="url(#phone-grad)" stroke="#475569" stroke-width="5"/>
    
    <!-- Borda Interna / Bezel -->
    <rect x="14" y="20" width="352" height="620" rx="28" fill="#090d16" stroke="#1e293b" stroke-width="2"/>

    <!-- Ilha Dinâmica / Câmera Superior -->
    <rect x="130" y="32" width="120" height="24" rx="12" fill="#020617"/>
    <circle cx="225" cy="44" r="5" fill="#1e293b"/>

    <!-- TELA DO WEB CONTROLLER (controle_celular_web_bluetooth.html) -->
    <!-- Top Bar da Tela -->
    <rect x="14" y="65" width="352" height="50" fill="#0f172a"/>
    <text x="32" y="96" font-size="14" font-weight="900" fill="#f8fafc">🤖 micro:bit V2</text>
    <rect x="150" y="78" width="90" height="24" rx="12" fill="rgba(16, 185, 129, 0.2)" stroke="#10b981" stroke-width="1.5"/>
    <circle cx="162" cy="90" r="4" fill="#10b981"/>
    <text x="202" y="95" font-size="11" font-weight="bold" fill="#10b981" text-anchor="middle">Conectado</text>
    <rect x="255" y="78" width="95" height="24" rx="6" fill="#06b6d4"/>
    <text x="302" y="94" font-size="10" font-weight="900" fill="#042f2e" text-anchor="middle">DESCONECTAR</text>

    <!-- Barra de Telemetria -->
    <rect x="14" y="115" width="352" height="28" fill="#0b1120"/>
    <text x="32" y="133" font-size="11" font-weight="bold" fill="#64748b">MOTOR L: <tspan fill="#38bdf8">85%</tspan> | R: <tspan fill="#38bdf8">85%</tspan></text>
    <text x="345" y="133" font-size="11" font-weight="bold" fill="#38bdf8" text-anchor="end">TX: 25 pkt/s</text>

    <!-- JOYSTICK ANALÓGICO NA TELA -->
    <g transform="translate(190, 260)">
      <circle cx="0" cy="0" r="95" fill="radial-gradient(circle, #1e293b 0%, #0f172a 100%)" stroke="#334155" stroke-width="2"/>
      <circle cx="0" cy="0" r="30" fill="none" stroke="#334155" stroke-width="1" stroke-dasharray="4 4"/>
      <!-- Manípulo Inclinado para Frente -->
      <circle cx="0" cy="-45" r="38" fill="radial-gradient(circle, #38bdf8 0%, #0284c7 100%)" stroke="#e0f2fe" stroke-width="3" filter="url(#glow)"/>
      <text x="0" y="125" font-size="11" font-weight="bold" fill="#94a3b8" text-anchor="middle">JOYSTICK TOUCH 360°</text>
    </g>

    <!-- BOTÕES TÁTICOS NA TELA -->
    <g transform="translate(40, 420)">
      <!-- Botão Turbo -->
      <rect x="0" y="0" width="300" height="42" rx="10" fill="#f59e0b"/>
      <text x="150" y="26" font-size="13" font-weight="900" fill="#0f172a" text-anchor="middle">⚡ ATAQUE TURBO (100%)</text>

      <!-- Botão Giro 180° -->
      <rect x="0" y="52" width="300" height="42" rx="10" fill="#8b5cf6"/>
      <text x="150" y="78" font-size="13" font-weight="900" fill="#ffffff" text-anchor="middle">🔄 GIRO TÁTICO 180°</text>

      <!-- Botão Arma de Combate -->
      <rect x="0" y="104" width="300" height="42" rx="10" fill="#1e293b" stroke="#ef4444" stroke-width="2"/>
      <text x="150" y="130" font-size="13" font-weight="900" fill="#f87171" text-anchor="middle">⚔️ ARMA ATIVA (P16): ON</text>

      <!-- Botão E-STOP -->
      <rect x="0" y="156" width="300" height="34" rx="8" fill="#0f172a" stroke="#ef4444" stroke-width="1.5"/>
      <text x="150" y="178" font-size="11" font-weight="bold" fill="#ef4444" text-anchor="middle">PARADA DE EMERGÊNCIA (STOP)</text>
    </g>

    <!-- Legenda Smartphone -->
    <text x="190" y="695" font-size="17" font-weight="900" fill="#f8fafc" text-anchor="middle">SEU SMARTPHONE (PILOTO)</text>
    <text x="190" y="718" font-size="12" font-weight="bold" fill="#38bdf8" text-anchor="middle">Zero Aplicativos Extras: Roda no Navegador Web</text>
  </g>

  <!-- ======================================================== -->
  <!-- 3. BBC MICRO:BIT V2 NO ROBÔ (À DIREITA)                  -->
  <!-- ======================================================== -->
  <g id="microbit-v2-board" transform="translate(1000, 150)" filter="url(#shadow)">
    <!-- Base PCB Preta do micro:bit V2 com cantos arredondados -->
    <rect x="0" y="0" width="460" height="380" rx="34" fill="#18181b" stroke="#27272a" stroke-width="4"/>
    
    <!-- Faixa Superior micro:bit V2 (Amarelo / Dourado) -->
    <path d="M 0,34 Q 0,0 34,0 H 426 Q 460,0 460,34 V 60 H 0 Z" fill="#eab308"/>
    <circle cx="50" cy="30" r="9" fill="#ffffff" opacity="0.3"/>
    <circle cx="410" cy="30" r="9" fill="#ffffff" opacity="0.3"/>
    
    <text x="230" y="38" font-size="22" font-weight="900" fill="#0f172a" text-anchor="middle" letter-spacing="3">micro:bit</text>
    <rect x="330" y="18" width="42" height="24" rx="6" fill="#0f172a"/>
    <text x="351" y="35" font-size="13" font-weight="900" fill="#eab308" text-anchor="middle">V2</text>

    <!-- LOGO TOUCH CAPACITIVO DO V2 (Dourado) -->
    <circle cx="230" cy="90" r="18" fill="#ca8a04" stroke="#fef08a" stroke-width="2"/>
    <path d="M 222,90 C 222,86 228,86 228,90 C 228,94 234,94 234,90" fill="none" stroke="#0f172a" stroke-width="3"/>
    <text x="230" y="122" font-size="9" font-weight="bold" fill="#ca8a04" text-anchor="middle">LOGO TOUCH</text>

    <!-- MICROFONE & LED INDICADOR DO V2 -->
    <circle cx="280" cy="85" r="4" fill="#ef4444"/>
    <circle cx="280" cy="95" r="3" fill="#ca8a04"/>

    <!-- MATRIZ 5x5 DE LEDS (MOSTRANDO ÍCONE HAPPY 😊) -->
    <g transform="translate(155, 145)">
      <!-- Linha 1 -->
      <circle cx="0" cy="0" r="8" fill="#27272a"/>
      <circle cx="34" cy="0" r="9" fill="#ef4444"/>
      <circle cx="68" cy="0" r="8" fill="#27272a"/>
      <circle cx="102" cy="0" r="9" fill="#ef4444"/>
      <circle cx="136" cy="0" r="8" fill="#27272a"/>
      <!-- Linha 2 -->
      <circle cx="0" cy="34" r="8" fill="#27272a"/>
      <circle cx="34" cy="34" r="9" fill="#ef4444"/>
      <circle cx="68" cy="34" r="8" fill="#27272a"/>
      <circle cx="102" cy="34" r="9" fill="#ef4444"/>
      <circle cx="136" cy="34" r="8" fill="#27272a"/>
      <!-- Linha 3 -->
      <circle cx="0" cy="68" r="8" fill="#27272a"/>
      <circle cx="34" cy="68" r="8" fill="#27272a"/>
      <circle cx="68" cy="68" r="8" fill="#27272a"/>
      <circle cx="102" cy="68" r="8" fill="#27272a"/>
      <circle cx="136" cy="68" r="8" fill="#27272a"/>
      <!-- Linha 4 -->
      <circle cx="0" cy="102" r="9" fill="#ef4444"/>
      <circle cx="34" cy="102" r="8" fill="#27272a"/>
      <circle cx="68" cy="102" r="8" fill="#27272a"/>
      <circle cx="102" cy="102" r="8" fill="#27272a"/>
      <circle cx="136" cy="102" r="9" fill="#ef4444"/>
      <!-- Linha 5 (Sorriso) -->
      <circle cx="0" cy="136" r="8" fill="#27272a"/>
      <circle cx="34" cy="136" r="9" fill="#ef4444"/>
      <circle cx="68" cy="136" r="9" fill="#ef4444"/>
      <circle cx="102" cy="136" r="9" fill="#ef4444"/>
      <circle cx="136" cy="136" r="8" fill="#27272a"/>
    </g>

    <!-- Botões A e B -->
    <circle cx="55" cy="210" r="22" fill="#27272a" stroke="#52525b" stroke-width="2"/>
    <circle cx="55" cy="210" r="15" fill="#09090b"/>
    <text x="55" y="255" font-size="14" font-weight="900" fill="#a1a1aa" text-anchor="middle">A</text>

    <circle cx="405" cy="210" r="22" fill="#27272a" stroke="#52525b" stroke-width="2"/>
    <circle cx="405" cy="210" r="15" fill="#09090b"/>
    <text x="405" y="255" font-size="14" font-weight="900" fill="#a1a1aa" text-anchor="middle">B</text>

    <!-- CONECTOR DE BORDA COM RECORTE NOTCH DO V2 (Dourado) -->
    <g transform="translate(10, 315)">
      <rect x="0" y="0" width="440" height="60" rx="6" fill="#0f172a" stroke="#ca8a04" stroke-width="2"/>
      
      <!-- Anéis Grandes P0, P1, P2, 3V, GND com Furos Centrais -->
      <circle cx="35" cy="30" r="18" fill="#ca8a04"/>
      <circle cx="35" cy="30" r="7" fill="#09090b"/>
      <text x="35" y="58" font-size="10" font-weight="900" fill="#fef08a" text-anchor="middle">P0 (MOT L)</text>

      <circle cx="120" cy="30" r="18" fill="#ca8a04"/>
      <circle cx="120" cy="30" r="7" fill="#09090b"/>
      <text x="120" y="58" font-size="10" font-weight="900" fill="#fef08a" text-anchor="middle">P1 (MOT R)</text>

      <circle cx="220" cy="30" r="18" fill="#ca8a04"/>
      <circle cx="220" cy="30" r="7" fill="#09090b"/>
      <text x="220" y="58" font-size="10" font-weight="900" fill="#fef08a" text-anchor="middle">P2</text>

      <circle cx="320" cy="30" r="18" fill="#ca8a04"/>
      <circle cx="320" cy="30" r="7" fill="#09090b"/>
      <text x="320" y="58" font-size="10" font-weight="900" fill="#fef08a" text-anchor="middle">3.3V</text>

      <circle cx="405" cy="30" r="18" fill="#ca8a04"/>
      <circle cx="405" cy="30" r="7" fill="#09090b"/>
      <text x="405" y="58" font-size="10" font-weight="900" fill="#fef08a" text-anchor="middle">GND</text>
    </g>

    <!-- Legenda microbit -->
    <text x="230" y="420" font-size="17" font-weight="900" fill="#f8fafc" text-anchor="middle">BBC MICRO:BIT V2 (NO ROBÔ)</text>
    <text x="230" y="442" font-size="12" font-weight="bold" fill="#4ade80" text-anchor="middle">Encaixado no Shield Robo:Bit ou Conectado na Ponte H L298N</text>
  </g>

  <!-- ======================================================== -->
  <!-- 4. ATUADORES E MOTORES DO ROBÔ (EXTREMA DIREITA)         -->
  <!-- ======================================================== -->
  <g transform="translate(1550, 180)" filter="url(#shadow)">
    <!-- Shield Robo:Bit / Caixa do Robô -->
    <rect x="0" y="0" width="300" height="320" rx="18" fill="#14532d" stroke="#22c55e" stroke-width="3"/>
    <text x="150" y="36" font-size="16" font-weight="900" fill="#f8fafc" text-anchor="middle">SHIELD ROBO:BIT / DRIVER</text>
    <text x="150" y="58" font-size="11" font-weight="bold" fill="#86efac" text-anchor="middle">Ponte H Integrada + Bornes</text>

    <!-- Motor Esquerdo -->
    <g transform="translate(20, 80)">
      <rect x="0" y="0" width="115" height="70" rx="8" fill="#eab308" stroke="#ca8a04" stroke-width="2"/>
      <text x="57" y="32" font-size="11" font-weight="900" fill="#713f12" text-anchor="middle">MOTOR ESQ</text>
      <text x="57" y="50" font-size="10" font-weight="bold" fill="#713f12" text-anchor="middle">P0 / P8</text>
    </g>

    <!-- Motor Direito -->
    <g transform="translate(165, 80)">
      <rect x="0" y="0" width="115" height="70" rx="8" fill="#eab308" stroke="#ca8a04" stroke-width="2"/>
      <text x="57" y="32" font-size="11" font-weight="900" fill="#713f12" text-anchor="middle">MOTOR DIR</text>
      <text x="57" y="50" font-size="10" font-weight="bold" fill="#713f12" text-anchor="middle">P1 / P12</text>
    </g>

    <!-- Arma Ativa -->
    <g transform="translate(20, 175)">
      <rect x="0" y="0" width="260" height="55" rx="8" fill="#991b1b" stroke="#ef4444" stroke-width="2"/>
      <text x="130" y="28" font-size="12" font-weight="900" fill="#fef2f2" text-anchor="middle">ARMA ATIVA / MOSFET</text>
      <text x="130" y="44" font-size="10" font-weight="bold" fill="#fca5a5" text-anchor="middle">Acionamento Digital no Pino P16</text>
    </g>

    <!-- Bateria -->
    <g transform="translate(20, 245)">
      <rect x="0" y="0" width="260" height="55" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
      <text x="130" y="28" font-size="12" font-weight="900" fill="#f8fafc" text-anchor="middle">BATERIA DO ROBÔ (6V - 7.4V)</text>
      <text x="130" y="44" font-size="10" font-weight="bold" fill="#38bdf8" text-anchor="middle">4x AA ou LiPo 2S com Chave Geral</text>
    </g>
  </g>

  <!-- Fios ligando micro:bit ao driver -->
  <path d="M 1470,300 C 1510,300 1520,290 1550,290" fill="none" stroke="#22c55e" stroke-width="5" stroke-linecap="round"/>
  <path d="M 1470,360 C 1510,360 1520,380 1550,380" fill="none" stroke="#ef4444" stroke-width="5" stroke-linecap="round"/>

</svg>

</body>
</html>
"""

def generate():
    os.makedirs("docs/images", exist_ok=True)
    html_path = os.path.abspath("docs/diagrama_microbit_v2_bluetooth.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML_V2_BLE)

    print("HTML written. Capturing with Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto("file:///" + html_path.replace("\\", "/"))
        page.wait_for_timeout(350)
        
        target_img_1 = "docs/images/circuito_microbit_v2_bluetooth.jpg"
        target_img_2 = "circuito_microbit_v2_bluetooth.jpg"
        target_img_3 = "microbit/circuito_microbit_v2_bluetooth.jpg"

        page.screenshot(path=target_img_1, type="jpeg", quality=95)
        page.screenshot(path=target_img_2, type="jpeg", quality=95)
        page.screenshot(path=target_img_3, type="jpeg", quality=95)
        print("micro:bit V2 BLE diagram captured successfully!")
        browser.close()

    artifact_dir = r"C:\Users\user\.gemini\antigravity\brain\2791b75b-6916-48f5-90a8-6eae4569d8e5"
    if os.path.exists(artifact_dir):
        dest = os.path.join(artifact_dir, "circuito_microbit_v2_bluetooth.jpg")
        shutil.copyfile("circuito_microbit_v2_bluetooth.jpg", dest)
        print(f"Copied to artifact directory: {dest}")

if __name__ == "__main__":
    generate()
