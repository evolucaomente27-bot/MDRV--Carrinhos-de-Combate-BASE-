#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>

// ==========================================
// CONFIGURAÇÕES DO PONTO DE ACESSO (Wi-Fi)
// ==========================================
const char* AP_SSID     = "Robo-Combate";
const char* AP_PASSWORD = "";  // Vazio = Rede Aberta (mínimo 8 caracteres se colocar senha)
const int   WEB_PORT    = 80;

// ==========================================
// MAPEAMENTO DOS PINOS (GPIOs do ESP32)
// ==========================================
const int PIN_IN1 = 18;  // Motor Esquerdo Frente
const int PIN_IN2 = 19;  // Motor Esquerdo Ré
const int PIN_ENA = 21;  // Motor Esquerdo PWM (se USE_ENABLE_PINS = true)

const int PIN_IN3 = 22;  // Motor Direito Frente
const int PIN_IN4 = 23;  // Motor Direito Ré
const int PIN_ENB = 25;  // Motor Direito PWM (se USE_ENABLE_PINS = true)

const int PIN_WEAPON = 26; // Acionamento de Arma/Atuador (Relé/MOSFET/ESC)
const int PIN_LED    = 2;  // LED onboard

#define USE_ENABLE_PINS false

// ==========================================
// FAILSAFE (WATCHDOG DE SEGURANÇA)
// ==========================================
const unsigned long FAILSAFE_TIMEOUT_MS = 400;
unsigned long lastCommandTime = 0;
bool failsafeTriggered = true;

WebServer server(WEB_PORT);
int currentSpeed = 255;
bool weaponActive = false;

// ==========================================
// PROTÓTIPOS DE FUNÇÕES
// ==========================================
void stopMotors();
void moveForward(int speed);
void moveBackward(int speed);
void spinLeft(int speed);
void spinRight(int speed);
void setWeapon(bool active);
void configurePins();
void handleRoot();
void handleCommand();
void handleNotFound();

// ==========================================
// PÁGINA WEB DO CONTROLE
// ==========================================
const char INDEX_HTML[] PROGMEM = R"rawhtml(
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Robô de Combate ESP32</title>
  <style>
    * { box-sizing: border-box; -webkit-touch-callout: none; -webkit-user-select: none; user-select: none; touch-action: manipulation; }
    body {
      margin: 0; padding: 12px; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background: radial-gradient(circle at center, #1a1a24 0%, #0d0d12 100%);
      color: #fff; display: flex; flex-direction: column; align-items: center; min-height: 100vh;
    }
    header {
      width: 100%; max-width: 440px; display: flex; justify-content: space-between; align-items: center;
      padding: 10px 14px; background: rgba(255, 255, 255, 0.05); border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 14px;
    }
    .title-box h1 { margin: 0; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 1.5px; color: #ff9800; }
    .title-box span { font-size: 0.75rem; color: #888; }
    .status-badge {
      padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: bold;
      background: #4caf50; color: #fff; box-shadow: 0 0 8px rgba(76, 175, 80, 0.6);
    }
    .status-badge.offline { background: #f44336; box-shadow: 0 0 8px rgba(244, 67, 54, 0.6); }
    .container { width: 100%; max-width: 440px; display: flex; flex-direction: column; gap: 16px; align-items: center; }
    .dpad-container { position: relative; width: 260px; height: 260px; margin: 8px auto; }
    .btn-ctrl {
      position: absolute; background: linear-gradient(145deg, #2b2b3b, #1d1d28);
      border: 2px solid #3d3d52; border-radius: 16px; color: #eee; font-size: 1.7rem;
      display: flex; align-items: center; justify-content: center; cursor: pointer;
      box-shadow: 0 6px 12px rgba(0, 0, 0, 0.5);
    }
    .btn-ctrl:active, .btn-ctrl.active { transform: scale(0.92); border-color: #ff9800; background: #ff9800; color: #111; }
    .btn-fwd  { top: 0; left: 85px; width: 90px; height: 80px; border-radius: 20px 20px 10px 10px; }
    .btn-rev  { bottom: 0; left: 85px; width: 90px; height: 80px; border-radius: 10px 10px 20px 20px; }
    .btn-left { top: 85px; left: 0; width: 80px; height: 90px; border-radius: 20px 10px 10px 20px; }
    .btn-right{ top: 85px; right: 0; width: 80px; height: 90px; border-radius: 10px 20px 20px 10px; }
    .btn-stop {
      top: 85px; left: 85px; width: 90px; height: 90px; border-radius: 50%;
      background: #dc3545; border: 3px solid #ff5252; color: #fff; font-size: 0.95rem; font-weight: 900;
    }
    .btn-stop:active { background: #ff1744; }
    .controls-panel {
      width: 100%; background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 16px; padding: 16px; display: flex; flex-direction: column; gap: 14px;
    }
    .slider-box { display: flex; flex-direction: column; gap: 6px; }
    .slider-header { display: flex; justify-content: space-between; font-size: 0.85rem; color: #bbb; }
    input[type=range] { width: 100%; height: 8px; border-radius: 4px; background: #333; accent-color: #ff9800; }
    .weapon-btn {
      width: 100%; padding: 14px; font-size: 1.1rem; font-weight: bold; letter-spacing: 1px;
      text-transform: uppercase; border-radius: 12px; border: 2px solid #ff3d00;
      background: linear-gradient(180deg, #d50000, #8e0000); color: #fff; cursor: pointer;
    }
    .weapon-btn.on { background: linear-gradient(180deg, #00e676, #009624); border-color: #00c853; }
    .footer-note { font-size: 0.75rem; color: #666; text-align: center; }
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
    <div class="dpad-container">
      <button class="btn-ctrl btn-fwd"  data-cmd="F">&#9650;</button>
      <button class="btn-ctrl btn-left" data-cmd="L">&#9664;</button>
      <button class="btn-ctrl btn-stop" data-cmd="S">STOP</button>
      <button class="btn-ctrl btn-right" data-cmd="R">&#9654;</button>
      <button class="btn-ctrl btn-rev"  data-cmd="B">&#9660;</button>
    </div>
    <div class="controls-panel">
      <div class="slider-box">
        <div class="slider-header">
          <span>Potência dos Motores</span>
          <span id="speedVal">100%</span>
        </div>
        <input type="range" id="speedSlider" min="100" max="255" value="255" step="5">
      </div>
      <button id="weaponBtn" class="weapon-btn">
        <span>&#9889; ARMA: DESLIGADA</span>
      </button>
    </div>
    <div class="footer-note">Failsafe Ativo (400ms): motores param ao perder conexão.</div>
  </div>
  <script>
    let activeCmd = 'S', currentSpeed = 255, weaponState = 0;
    const statusBadge = document.getElementById('status');
    const speedSlider = document.getElementById('speedSlider');
    const speedVal = document.getElementById('speedVal');
    const weaponBtn = document.getElementById('weaponBtn');

    speedSlider.addEventListener('input', (e) => {
      currentSpeed = e.target.value;
      speedVal.innerText = Math.round((currentSpeed / 255) * 100) + '%';
      sendCommand(activeCmd);
    });

    weaponBtn.addEventListener('click', () => {
      weaponState = weaponState ? 0 : 1;
      weaponBtn.classList.toggle('on', weaponState);
      weaponBtn.innerHTML = weaponState ? '<span>&#9889; ARMA: LIGADA</span>' : '<span>&#9889; ARMA: DESLIGADA</span>';
      sendCommand(activeCmd);
    });

    function sendCommand(cmd) {
      activeCmd = cmd;
      fetch(`/cmd?dir=${cmd}&speed=${currentSpeed}&weapon=${weaponState}`, { cache: 'no-store' })
        .then(res => { if(res.ok) { statusBadge.innerText = 'CONECTADO'; statusBadge.classList.remove('offline'); } })
        .catch(() => { statusBadge.innerText = 'SEM SINAL'; statusBadge.classList.add('offline'); });
    }

    document.querySelectorAll('.btn-ctrl').forEach(btn => {
      const cmd = btn.getAttribute('data-cmd');
      const start = (e) => { e.preventDefault(); btn.classList.add('active'); sendCommand(cmd); };
      const end   = (e) => { e.preventDefault(); btn.classList.remove('active'); sendCommand('S'); };
      btn.addEventListener('touchstart', start, { passive: false });
      btn.addEventListener('touchend', end, { passive: false });
      btn.addEventListener('mousedown', start);
      btn.addEventListener('mouseup', end);
      btn.addEventListener('mouseleave', () => { if(btn.classList.contains('active')) { btn.classList.remove('active'); sendCommand('S'); } });
    });

    setInterval(() => {
      fetch(`/cmd?dir=${activeCmd}&speed=${currentSpeed}&weapon=${weaponState}`, { cache: 'no-store' })
        .then(() => { statusBadge.innerText = 'CONECTADO'; statusBadge.classList.remove('offline'); })
        .catch(() => { statusBadge.innerText = 'SEM SINAL'; statusBadge.classList.add('offline'); });
    }, 200);
  </script>
</body>
</html>
)rawhtml";

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

void setWeapon(bool active) {
  weaponActive = active;
  digitalWrite(PIN_WEAPON, active ? HIGH : LOW);
}

void handleRoot() {
  server.send_P(200, "text/html", INDEX_HTML);
}

void handleCommand() {
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

  switch (dir[0]) {
    case 'F': moveForward(currentSpeed); break;
    case 'B': moveBackward(currentSpeed); break;
    case 'L': spinLeft(currentSpeed); break;
    case 'R': spinRight(currentSpeed); break;
    case 'S':
    default:
      stopMotors();
      break;
  }

  server.send(200, "text/plain", "OK");
}

void handleNotFound() {
  server.send(404, "text/plain", "Não encontrado");
}

void setup() {
  Serial.begin(115200);
  delay(400);
  Serial.println("\n[ROBO COMBATE] Iniciando...");

  configurePins();

  WiFi.mode(WIFI_AP);
  if (strlen(AP_PASSWORD) >= 8) {
    WiFi.softAP(AP_SSID, AP_PASSWORD);
  } else {
    WiFi.softAP(AP_SSID);
  }

  Serial.print("[Wi-Fi] AP: ");
  Serial.println(AP_SSID);
  Serial.print("[Wi-Fi] IP: ");
  Serial.println(WiFi.softAPIP());

  server.on("/", HTTP_GET, handleRoot);
  server.on("/cmd", HTTP_GET, handleCommand);
  server.onNotFound(handleNotFound);
  server.begin();

  Serial.println("[Failsafe] Sistema de segurança pronto.");
  lastCommandTime = millis();
}

void loop() {
  server.handleClient();

  if (!failsafeTriggered && (millis() - lastCommandTime > FAILSAFE_TIMEOUT_MS)) {
    failsafeTriggered = true;
    stopMotors();
    setWeapon(false);
    digitalWrite(PIN_LED, LOW);
    Serial.println("[FAILSAFE] Sinal interrompido! Parada forçada dos motores.");
  }
}
