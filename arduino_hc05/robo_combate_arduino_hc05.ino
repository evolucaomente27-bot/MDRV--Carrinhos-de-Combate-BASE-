/*
 * =====================================================================================
 * PROJETO: Robô de Combate com Arduino (Uno / Nano) + Módulo Bluetooth HC-05
 * 
 * Descrição:
 *  Controle remoto para robô de batalha via Bluetooth usando Arduino e módulo HC-05.
 *  Compatível com o aplicativo "Bluetooth RC Controller" e terminais seriais Bluetooth.
 * 
 * Mapeamento dos Pinos:
 *  - Pinos 2 e 3: Comunicação SoftwareSerial com o HC-05 (RX=2, TX=3)
 *  - Pinos 5 e 6: Motor Esquerdo (IN1 e IN2 - Pinos PWM)
 *  - Pinos 9 e 10: Motor Direito (IN3 e IN4 - Pinos PWM)
 *  - Pino 4: Gatilho da Arma/Atuador (Relé ou MOSFET)
 *  - Pino 13: LED onboard indicador de status
 * 
 * Segurança de Combate:
 *  - SISTEMA FAILSAFE: Se o celular sair de alcance ou perder o sinal por mais de 500ms,
 *    todos os motores e a arma são desligados imediatamente.
 * =====================================================================================
 */

#include <SoftwareSerial.h>

// ==========================================
// CONFIGURAÇÃO DO MÓDULO HC-05 (SoftwareSerial)
// ==========================================
// Pino 2 do Arduino vai no TXD do HC-05
// Pino 3 do Arduino vai no RXD do HC-05 (através de divisor resistivo 1k/2k)
const int BT_RX = 2;
const int BT_TX = 3;
SoftwareSerial bluetooth(BT_RX, BT_TX);

// ==========================================
// MAPEAMENTO DOS MOTORES E ATUADORES
// ==========================================
// Motor Esquerdo (Pinos PWM do Arduino Uno/Nano)
const int PIN_IN1 = 5;
const int PIN_IN2 = 6;

// Motor Direito (Pinos PWM do Arduino Uno/Nano)
const int PIN_IN3 = 9;
const int PIN_IN4 = 10;

// Arma / Atuador de Combate (Gatilho para Relé ou Módulo MOSFET)
const int PIN_WEAPON = 4;

// LED Onboard
const int PIN_LED = 13;

// ==========================================
// VARIÁVEIS DE CONTROLE E FAILSAFE
// ==========================================
const unsigned long FAILSAFE_TIMEOUT_MS = 500; // Tempo máximo sem comando antes do corte
unsigned long lastCommandTime = 0;
bool failsafeTriggered = true;

int currentSpeed = 255;      // Velocidade atual (0 a 255)
bool weaponActive = false;   // Estado da arma

// ==========================================
// FUNÇÕES DE MOVIMENTAÇÃO DOS MOTORES
// ==========================================

// Parar todos os motores
void stopMotors() {
  analogWrite(PIN_IN1, 0);
  analogWrite(PIN_IN2, 0);
  analogWrite(PIN_IN3, 0);
  analogWrite(PIN_IN4, 0);
}

// Avançar (Frente)
void moveForward(int speed) {
  analogWrite(PIN_IN1, speed);
  analogWrite(PIN_IN2, 0);
  analogWrite(PIN_IN3, speed);
  analogWrite(PIN_IN4, 0);
}

// Recuar (Ré)
void moveBackward(int speed) {
  analogWrite(PIN_IN1, 0);
  analogWrite(PIN_IN2, speed);
  analogWrite(PIN_IN3, 0);
  analogWrite(PIN_IN4, speed);
}

// Giro no próprio eixo à Esquerda (Tank Turn)
void spinLeft(int speed) {
  analogWrite(PIN_IN1, 0);
  analogWrite(PIN_IN2, speed);
  analogWrite(PIN_IN3, speed);
  analogWrite(PIN_IN4, 0);
}

// Giro no próprio eixo à Direita (Tank Turn)
void spinRight(int speed) {
  analogWrite(PIN_IN1, speed);
  analogWrite(PIN_IN2, 0);
  analogWrite(PIN_IN3, 0);
  analogWrite(PIN_IN4, speed);
}

// Curva suave para a Esquerda
void turnLeft(int speed) {
  analogWrite(PIN_IN1, speed / 3);
  analogWrite(PIN_IN2, 0);
  analogWrite(PIN_IN3, speed);
  analogWrite(PIN_IN4, 0);
}

// Curva suave para a Direita
void turnRight(int speed) {
  analogWrite(PIN_IN1, speed);
  analogWrite(PIN_IN2, 0);
  analogWrite(PIN_IN3, speed / 3);
  analogWrite(PIN_IN4, 0);
}

// Controle da Arma
void setWeapon(bool active) {
  weaponActive = active;
  digitalWrite(PIN_WEAPON, active ? HIGH : LOW);
}

// ==========================================
// SETUP INICIAL
// ==========================================
void setup() {
  // Inicializa comunicação serial com o computador (para depuração)
  Serial.begin(9600);
  
  // Inicializa comunicação com o módulo HC-05 (o padrão de fábrica é 9600 baud)
  bluetooth.begin(9600);

  // Configuração dos pinos como saída
  pinMode(PIN_IN1, OUTPUT);
  pinMode(PIN_IN2, OUTPUT);
  pinMode(PIN_IN3, OUTPUT);
  pinMode(PIN_IN4, OUTPUT);
  pinMode(PIN_WEAPON, OUTPUT);
  pinMode(PIN_LED, OUTPUT);

  // Inicia com tudo desligado
  stopMotors();
  setWeapon(false);
  digitalWrite(PIN_LED, LOW);

  Serial.println(F("=== ROBO DE COMBATE ARDUINO + HC-05 PRONTO ==="));
  Serial.println(F("Aguardando conexao Bluetooth..."));

  lastCommandTime = millis();
}

// ==========================================
// LOOP PRINCIPAL
// ==========================================
void loop() {
  // Verifica se recebeu dados do módulo Bluetooth HC-05
  if (bluetooth.available()) {
    char cmd = bluetooth.read();
    
    // Reinicia o relógio do Failsafe
    lastCommandTime = millis();
    failsafeTriggered = false;
    digitalWrite(PIN_LED, HIGH);

    // Processa o comando recebido do app Bluetooth RC Controller
    switch (cmd) {
      // Movimentação principal
      case 'F': // Frente
        moveForward(currentSpeed);
        break;
      case 'B': // Ré
        moveBackward(currentSpeed);
        break;
      case 'L': // Giro sobre o eixo à esquerda
        spinLeft(currentSpeed);
        break;
      case 'R': // Giro sobre o eixo à direita
        spinRight(currentSpeed);
        break;
      case 'G': // Curva frente-esquerda
        turnLeft(currentSpeed);
        break;
      case 'I': // Curva frente-direita
        turnRight(currentSpeed);
        break;
      case 'S': // Parar
      case 'D': // Parada geral do app
        stopMotors();
        break;

      // Controle de Arma / Atuador
      case 'W': // Liga Arma (ou toggle)
      case 'X': // Triângulo / Botão de ação
        setWeapon(!weaponActive);
        bluetooth.println(weaponActive ? F("ARMA: ON") : F("ARMA: OFF"));
        break;
      case 'w': // Desliga Arma
        setWeapon(false);
        break;

      // Ajustes de Velocidade (0 a 9 e 'q' para 100%)
      case '0': currentSpeed = 0; break;
      case '1': currentSpeed = 40; break;
      case '2': currentSpeed = 65; break;
      case '3': currentSpeed = 90; break;
      case '4': currentSpeed = 115; break;
      case '5': currentSpeed = 140; break;
      case '6': currentSpeed = 165; break;
      case '7': currentSpeed = 190; break;
      case '8': currentSpeed = 215; break;
      case '9': currentSpeed = 240; break;
      case 'q': currentSpeed = 255; break;
    }
  }

  // =======================================================
  // SISTEMA DE SEGURANÇA (FAILSAFE WATCHDOG)
  // Se passar mais de 500ms sem receber dados do celular:
  // corta imediatamente tração e arma.
  // =======================================================
  if (!failsafeTriggered && (millis() - lastCommandTime > FAILSAFE_TIMEOUT_MS)) {
    failsafeTriggered = true;
    stopMotors();
    setWeapon(false);
    digitalWrite(PIN_LED, LOW);
    Serial.println(F("[FAILSAFE] Perda de conexao Bluetooth! Motores cortados."));
  }
}
