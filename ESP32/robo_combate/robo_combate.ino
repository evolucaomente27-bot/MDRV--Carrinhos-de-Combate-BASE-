/*
 * =====================================================================================
 * PROJETO: Robô de Combate / Batalha de Robôs com ESP32 e Módulo Ponte H
 * Autoria: Assistente Antigravity
 * 
 * Funcionalidades:
 *  - Cria um Ponto de Acesso Wi-Fi (SoftAP: "Robo-Combate")
 *  - Servidor Web com Interface Touch (Joystick / D-Pad) para Smartphone (Android/iOS)
 *  - Sem necessidade de instalar nenhum aplicativo ou ter acesso à Internet
 *  - Tração diferencial (2 motores DC com controle de velocidade via PWM)
 *  - Acionamento de Atuador/Arma (Spinners, Lifters, Flippers via Relé/MOSFET/ESC)
 *  - SISTEMA FAILSAFE: Desliga todos os motores se perder o sinal por mais de 400ms
 * =====================================================================================
 */

#include <WiFi.h>
#include <WebServer.h>

// ==========================================
// CONFIGURAÇÕES DO PONTO DE ACESSO (Wi-Fi)
// ==========================================
const char* AP_SSID     = "Robo-Combate-MDV2";
const char* AP_PASSWORD = "";  // Deixe vazio ("") para rede aberta ou defina senha (mínimo 8 caracteres)
const int   WEB_PORT    = 80;

// ==========================================
// MAPEAMENTO DOS PINOS (GPIOs do ESP32)
// ==========================================
// Motor Esquerdo
const int PIN_IN1 = 18;  // Direção Frente Esquerda
const int PIN_IN2 = 19;  // Direção Ré Esquerda
const int PIN_ENA = 21;  // Velocidade Esquerda (opcional, deixe como 0 se usar jumpers na ponte H)

// Motor Direito
const int PIN_IN3 = 22;  // Direção Frente Direita
const int PIN_IN4 = 23;  // Direção Ré Direita
const int PIN_ENB = 25;  // Velocidade Direita (opcional, deixe como 0 se usar jumpers na ponte H)

// Canal da Arma / Atuador (MOSFET, Relé ou sinal de disparo)
const int PIN_WEAPON = 26;

// LED indicador de status (GPIO 2 é o LED onboard da maioria das placas ESP32)
const int PIN_LED = 2;

// Ativar ou desativar pinos ENA/ENB dedicados
// Se TRUE: controla velocidade por ENA e ENB (jumpers removidos da ponte H)
// Se FALSE: jumpers de ENA/ENB mantidos na ponte H, PWM aplicado diretamente em IN1-IN4
#define USE_ENABLE_PINS false

// ==========================================
// SEGURANÇA E FAILSAFE
// ==========================================
// Tempo máximo (em milissegundos) sem receber pacotes antes de cortar os motores
const unsigned long FAILSAFE_TIMEOUT_MS = 400;
unsigned long lastCommandTime = 0;
bool failsafeTriggered = true;

// Instância do servidor Web
WebServer server(WEB_PORT);

// Estado atual dos atuadores
int currentSpeed = 255;
bool weaponActive = false;

// ==========================================
// PÁGINA WEB DO CONTROLE (HTML + CSS + JS)
// Embutida na memória Flash (PROGMEM)
// ==========================================
const char INDEX_HTML[] PROGMEM = R"rawhtml(
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Robô de Combate ESP32</title>
  <style>
    * {
      box-sizing: border-box;
      -webkit-touch-callout: none;
      -webkit-user-select: none;
      user-select: none;
      touch-action: manipulation;
    }
    body {
      margin: 0;
      padding: 10px;
      font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background: radial-gradient(circle at center, #1a1a24 0%, #0d0d12 100%);
      color: #fff;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
      overflow-x: hidden;
    }
    header {
      width: 100%;
      max-width: 480px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 12px;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.1);
      margin-bottom: 12px;
    }
    .title-box h1 {
      margin: 0;
      font-size: 1.1rem;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      color: #ff9800;
    }
    .title-box span {
      font-size: 0.75rem;
      color: #888;
    }
    .status-badge {
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: bold;
      background: #4caf50;
      color: #fff;
      box-shadow: 0 0 8px rgba(76, 175, 80, 0.6);
      transition: all 0.3s;
    }
    .status-badge.offline {
      background: #f44336;
      box-shadow: 0 0 8px rgba(244, 67, 54, 0.6);
    }
    .container {
      width: 100%;
      max-width: 480px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      align-items: center;
    }
    /* D-PAD GRID */
    .dpad-container {
      position: relative;
      width: 260px;
      height: 260px;
      margin: 10px auto;
    }
    .btn-ctrl {
      position: absolute;
      background: linear-gradient(145deg, #2b2b3b, #1d1d28);
      border: 2px solid #3d3d52;
      border-radius: 16px;
      color: #eee;
      font-size: 1.6rem;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: 0 6px 12px rgba(0, 0, 0, 0.5);
      transition: transform 0.05s, border-color 0.1s;
    }
    .btn-ctrl:active, .btn-ctrl.active {
      transform: scale(0.92);
      border-color: #ff9800;
      background: #ff9800;
      color: #111;
      box-shadow: 0 0 15px rgba(255, 152, 0, 0.8);
    }
    .btn-fwd  { top: 0; left: 85px; width: 90px; height: 80px; border-radius: 20px 20px 10px 10px; }
    .btn-rev  { bottom: 0; left: 85px; width: 90px; height: 80px; border-radius: 10px 10px 20px 20px; }
    .btn-left { top: 85px; left: 0; width: 80px; height: 90px; border-radius: 20px 10px 10px 20px; }
    .btn-right{ top: 85px; right: 0; width: 80px; height: 90px; border-radius: 10px 20px 20px 10px; }
    .btn-stop {
      top: 85px; left: 85px; width: 90px; height: 90px;
      border-radius: 50%;
      background: #dc3545;
      border: 3px solid #ff5252;
      color: #fff;
      font-size: 0.95rem;
      font-weight: 900;
      box-shadow: 0 0 10px rgba(220, 53, 69, 0.6);
    }
    .btn-stop:active, .btn-stop.active {
      background: #ff1744;
      transform: scale(0.9);
      box-shadow: 0 0 20px rgba(255, 23, 68, 1);
    }

    /* WEAPON & SPEED BAR */
    .controls-panel {
      width: 100%;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 16px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .slider-box {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .slider-header {
      display: flex;
      justify-content: space-between;
      font-size: 0.85rem;
      color: #bbb;
    }
    input[type=range] {
      width: 100%;
      height: 8px;
      border-radius: 4px;
      background: #333;
      accent-color: #ff9800;
      cursor: pointer;
    }
    .weapon-btn {
      width: 100%;
      padding: 14px;
      font-size: 1.1rem;
      font-weight: bold;
      letter-spacing: 1px;
      text-transform: uppercase;
      border-radius: 12px;
      border: 2px solid #ff3d00;
      background: linear-gradient(180deg, #d50000, #8e0000);
      color: #fff;
      box-shadow: 0 4px 15px rgba(213, 0, 0, 0.4);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
    }
    .weapon-btn.on {
      background: linear-gradient(180deg, #00e676, #009624);
      border-color: #00c853;
      box-shadow: 0 0 20px rgba(0, 230, 118, 0.6);
    }
    .footer-note {
      font-size: 0.75rem;
      color: #666;
      text-align: center;
      margin-top: 8px;
    }
  </style>
</head>
<body>

  <header>
    <div class="title-box">
      <h1>COMBAT BOT</h1>
      <span>ESP32 + PONTE H</span>
    </div>
    <div id="status" class="status-badge">CONECTADO</div>
  </header>

  <div class="container">
    <!-- D-PAD CONTROLLER -->
    <div class="dpad-container">
      <button class="btn-ctrl btn-fwd"   data-cmd="F">&#9650;</button>
      <button class="btn-ctrl btn-left"  data-cmd="L">&#9664;</button>
      <button class="btn-ctrl btn-stop"  data-cmd="S">STOP</button>
      <button class="btn-ctrl btn-right" data-cmd="R">&#9654;</button>
      <button class="btn-ctrl btn-rev"   data-cmd="B">&#9660;</button>
    </div>

    <!-- PAINEL DE CONTROLES ADICIONAIS -->
    <div class="controls-panel">
      <!-- CONTROLE DE VELOCIDADE -->
      <div class="slider-box">
        <div class="slider-header">
          <span>Potência dos Motores</span>
          <span id="speedVal">100%</span>
        </div>
        <input type="range" id="speedSlider" min="100" max="255" value="255" step="5">
      </div>

      <!-- BOTÃO DA ARMA / ATUADOR -->
      <button id="weaponBtn" class="weapon-btn">
        <span>&#9889; ARMA: DESLIGADA</span>
      </button>
    </div>

    <div class="footer-note">
      Failsafe Ativo: Os motores param automaticamente se a conexão for perdida.
    </div>
  </div>

  <script>
    let activeCmd = 'S';
    let currentSpeed = 255;
    let weaponState = 0;
    const statusBadge = document.getElementById('status');
    const speedSlider = document.getElementById('speedSlider');
    const speedVal = document.getElementById('speedVal');
    const weaponBtn = document.getElementById('weaponBtn');

    // Atualiza mostrador de velocidade
    speedSlider.addEventListener('input', (e) => {
      currentSpeed = e.target.value;
      let pct = Math.round((currentSpeed / 255) * 100);
      speedVal.innerText = pct + '%';
      sendCommand(activeCmd);
    });

    // Alterna estado da arma
    weaponBtn.addEventListener('click', () => {
      weaponState = weaponState ? 0 : 1;
      if (weaponState) {
        weaponBtn.classList.add('on');
        weaponBtn.innerHTML = '<span>&#9889; ARMA: LIGADA</span>';
      } else {
        weaponBtn.classList.remove('on');
        weaponBtn.innerHTML = '<span>&#9889; ARMA: DESLIGADA</span>';
      }
      sendCommand(activeCmd);
    });

    // Envio HTTP com Keep-Alive / Heartbeat
    function sendCommand(cmd) {
      activeCmd = cmd;
      const url = `/cmd?dir=${cmd}&speed=${currentSpeed}&weapon=${weaponState}`;
      fetch(url, { method: 'GET', cache: 'no-store' })
        .then(response => {
          if (response.ok) {
            statusBadge.innerText = 'CONECTADO';
            statusBadge.classList.remove('offline');
          }
        })
        .catch(err => {
          statusBadge.innerText = 'SEM SINAL';
          statusBadge.classList.add('offline');
        });
    }

    // Gerenciador de eventos de toque e mouse para botões
    const buttons = document.querySelectorAll('.btn-ctrl');
    buttons.forEach(btn => {
      const cmd = btn.getAttribute('data-cmd');

      const startAction = (e) => {
        e.preventDefault();
        btn.classList.add('active');
        sendCommand(cmd);
      };

      const endAction = (e) => {
        e.preventDefault();
        btn.classList.remove('active');
        sendCommand('S'); // Soltou = STOP imediato
      };

      btn.addEventListener('touchstart', startAction, { passive: false });
      btn.addEventListener('touchend', endAction, { passive: false });
      btn.addEventListener('mousedown', startAction);
      btn.addEventListener('mouseup', endAction);
      btn.addEventListener('mouseleave', () => {
        if (btn.classList.contains('active')) {
          btn.classList.remove('active');
          sendCommand('S');
        }
      });
    });

    // Envia sinal periódico para manter o Failsafe satisfeito enquanto a página estiver aberta
    setInterval(() => {
      if (activeCmd !== 'S') {
        sendCommand(activeCmd);
      } else {
        // Envia ping de heartbeat
        fetch(`/cmd?dir=S&speed=${currentSpeed}&weapon=${weaponState}`, { cache: 'no-store' })
          .then(() => {
            statusBadge.innerText = 'CONECTADO';
            statusBadge.classList.remove('offline');
          })
          .catch(() => {
            statusBadge.innerText = 'SEM SINAL';
            statusBadge.classList.add('offline');
          });
      }
    }, 200); // Pacote a cada 200ms (bem abaixo do timeout de 400ms)
  </script>
</body>
</html>
)rawhtml";

// ==========================================
// FUNÇÕES DE CONTROLE DOS MOTORES
// ==========================================

void configurePins() {
  pinMode(PIN_IN1, OUTPUT);
  pinMode(PIN_IN2, OUTPUT);
  pinMode(PIN_IN3, OUTPUT);
  pinMode(PIN_IN4, OUTPUT);
  pinMode(PIN_WEAPON, OUTPUT);
  pinMode(PIN_LED, OUTPUT);

#if USE_ENABLE_PINS
  pinMode(PIN_ENA, OUTPUT);
  pinMode(PIN_ENB, OUTPUT);
#endif

  stopMotors();
  digitalWrite(PIN_WEAPON, LOW);
  digitalWrite(PIN_LED, LOW);
}

// Parada imediata de todos os motores
void stopMotors() {
#if USE_ENABLE_PINS
  analogWrite(PIN_ENA, 0);
  analogWrite(PIN_ENB, 0);
  digitalWrite(PIN_IN1, LOW);
  digitalWrite(PIN_IN2, LOW);
  digitalWrite(PIN_IN3, LOW);
  digitalWrite(PIN_IN4, LOW);
#else
  analogWrite(PIN_IN1, 0);
  analogWrite(PIN_IN2, 0);
  analogWrite(PIN_IN3, 0);
  analogWrite(PIN_IN4, 0);
#endif
}

// Movimento para Frente
void moveForward(int speed) {
#if USE_ENABLE_PINS
  digitalWrite(PIN_IN1, HIGH);
  digitalWrite(PIN_IN2, LOW);
  digitalWrite(PIN_IN3, HIGH);
  digitalWrite(PIN_IN4, LOW);
  analogWrite(PIN_ENA, speed);
  analogWrite(PIN_ENB, speed);
#else
  analogWrite(PIN_IN1, speed);
  analogWrite(PIN_IN2, 0);
  analogWrite(PIN_IN3, speed);
  analogWrite(PIN_IN4, 0);
#endif
}

// Movimento para Ré
void moveBackward(int speed) {
#if USE_ENABLE_PINS
  digitalWrite(PIN_IN1, LOW);
  digitalWrite(PIN_IN2, HIGH);
  digitalWrite(PIN_IN3, LOW);
  digitalWrite(PIN_IN4, HIGH);
  analogWrite(PIN_ENA, speed);
  analogWrite(PIN_ENB, speed);
#else
  analogWrite(PIN_IN1, 0);
  analogWrite(PIN_IN2, speed);
  analogWrite(PIN_IN3, 0);
  analogWrite(PIN_IN4, speed);
#endif
}

// Giro sobre o próprio eixo à Esquerda (Tank Turn)
void spinLeft(int speed) {
#if USE_ENABLE_PINS
  digitalWrite(PIN_IN1, LOW);
  digitalWrite(PIN_IN2, HIGH);
  digitalWrite(PIN_IN3, HIGH);
  digitalWrite(PIN_IN4, LOW);
  analogWrite(PIN_ENA, speed);
  analogWrite(PIN_ENB, speed);
#else
  analogWrite(PIN_IN1, 0);
  analogWrite(PIN_IN2, speed);
  analogWrite(PIN_IN3, speed);
  analogWrite(PIN_IN4, 0);
#endif
}

// Giro sobre o próprio eixo à Direita (Tank Turn)
void spinRight(int speed) {
#if USE_ENABLE_PINS
  digitalWrite(PIN_IN1, HIGH);
  digitalWrite(PIN_IN2, LOW);
  digitalWrite(PIN_IN3, LOW);
  digitalWrite(PIN_IN4, HIGH);
  analogWrite(PIN_ENA, speed);
  analogWrite(PIN_ENB, speed);
#else
  analogWrite(PIN_IN1, speed);
  analogWrite(PIN_IN2, 0);
  analogWrite(PIN_IN3, 0);
  analogWrite(PIN_IN4, speed);
#endif
}

// Controle da Arma
void setWeapon(bool active) {
  weaponActive = active;
  digitalWrite(PIN_WEAPON, active ? HIGH : LOW);
}

// ==========================================
// ROTAS DO SERVIDOR WEB
// ==========================================

void handleRoot() {
  server.send_P(200, "text/html", INDEX_HTML);
}

void handleCommand() {
  // Atualiza timestamp para reiniciar o watchdog do Failsafe
  lastCommandTime = millis();
  failsafeTriggered = false;
  digitalWrite(PIN_LED, HIGH);

  String dir = "S";
  int speed = 255;
  int weapon = 0;

  if (server.hasArg("dir")) {
    dir = server.arg("dir");
  }
  if (server.hasArg("speed")) {
    speed = server.arg("speed").toInt();
    speed = constrain(speed, 0, 255);
    currentSpeed = speed;
  }
  if (server.hasArg("weapon")) {
    weapon = server.arg("weapon").toInt();
    setWeapon(weapon == 1);
  }

  // Executa o comando de movimentação
  switch (dir[0]) {
    case 'F': // Frente
      moveForward(currentSpeed);
      break;
    case 'B': // Ré
      moveBackward(currentSpeed);
      break;
    case 'L': // Girar à Esquerda
      spinLeft(currentSpeed);
      break;
    case 'R': // Girar à Direita
      spinRight(currentSpeed);
      break;
    case 'S': // Parar
    default:
      stopMotors();
      break;
  }

  server.send(200, "text/plain", "OK");
}

void handleNotFound() {
  server.send(404, "text/plain", "Não encontrado");
}

// ==========================================
// SETUP & LOOP PRINCIPAL
// ==========================================

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\n--- INICIALIZANDO ROBÔ DE COMBATE ESP32 ---");

  // Configura pinagem dos motores e arma
  configurePins();

  // Configura o Ponto de Acesso (Access Point)
  WiFi.mode(WIFI_AP);
  bool apSuccess;
  if (strlen(AP_PASSWORD) >= 8) {
    apSuccess = WiFi.softAP(AP_SSID, AP_PASSWORD);
  } else {
    apSuccess = WiFi.softAP(AP_SSID); // Rede aberta
  }

  if (apSuccess) {
    Serial.print("[Wi-Fi] Ponto de Acesso criado com sucesso: ");
    Serial.println(AP_SSID);
    Serial.print("[Wi-Fi] Endereço IP do Robô: ");
    Serial.println(WiFi.softAPIP());
  } else {
    Serial.println("[ERRO] Falha ao criar Ponto de Acesso Wi-Fi!");
  }

  // Configura endpoints HTTP
  server.on("/", HTTP_GET, handleRoot);
  server.on("/cmd", HTTP_GET, handleCommand);
  server.onNotFound(handleNotFound);

  // Inicia o servidor Web
  server.begin();
  Serial.println("[Web] Servidor Web iniciado na porta 80.");
  Serial.println("[Failsafe] Sistema de segurança de corte ativo (400ms).");

  lastCommandTime = millis();
}

void loop() {
  // Processa as requisições Web recebidas
  server.handleClient();

  // =======================================================
  // ROTINA DE SEGURANÇA DE COMBATE (FAILSAFE WATCHDOG)
  // Se o piloto perder a conexão Wi-Fi ou fechar o app,
  // corta instantaneamente motores e arma em menos de 400ms.
  // =======================================================
  if (!failsafeTriggered && (millis() - lastCommandTime > FAILSAFE_TIMEOUT_MS)) {
    failsafeTriggered = true;
    stopMotors();
    setWeapon(false);
    digitalWrite(PIN_LED, LOW);
    Serial.println("[ALERTA] FAILSAFE DISPARADO: Conexão perdida. Robô desarmado!");
  }
}
