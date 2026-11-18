/*
 * =====================================================================================
 * PROJETO: Robô de Combate com ESP32 - VERSÃO BLUETOOTH SERIAL (OPCIONAL)
 * 
 * Compatível com aplicativos de controle remoto Bluetooth como:
 *  - "Bluetooth RC Controller"
 *  - "Serial Bluetooth Terminal"
 *  - "Dabble - Bluetooth Controller"
 * 
 * NOTA: O Bluetooth Classic funciona no ESP32 padrão (ESP-WROOM-32 / DevKit v1).
 * Não suportado nas variantes ESP32-S2 / ESP32-C3.
 * =====================================================================================
 */

#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error "O Bluetooth não está ativado! Verifique as configurações da placa no Arduino IDE."
#endif

BluetoothSerial SerialBT;

// Mapeamento de pinos
const int PIN_IN1 = 18;
const int PIN_IN2 = 19;
const int PIN_IN3 = 22;
const int PIN_IN4 = 23;
const int PIN_WEAPON = 26;
const int PIN_LED = 2;

// Failsafe
const unsigned long FAILSAFE_TIMEOUT_MS = 500;
unsigned long lastCommandTime = 0;
bool failsafeTriggered = true;

int currentSpeed = 255;
bool weaponActive = false;

void stopMotors() {
  analogWrite(PIN_IN1, 0);
  analogWrite(PIN_IN2, 0);
  analogWrite(PIN_IN3, 0);
  analogWrite(PIN_IN4, 0);
}

void moveForward(int speed) {
  analogWrite(PIN_IN1, speed);
  analogWrite(PIN_IN2, 0);
  analogWrite(PIN_IN3, speed);
  analogWrite(PIN_IN4, 0);
}

void moveBackward(int speed) {
  analogWrite(PIN_IN1, 0);
  analogWrite(PIN_IN2, speed);
  analogWrite(PIN_IN3, 0);
  analogWrite(PIN_IN4, speed);
}

void spinLeft(int speed) {
  analogWrite(PIN_IN1, 0);
  analogWrite(PIN_IN2, speed);
  analogWrite(PIN_IN3, speed);
  analogWrite(PIN_IN4, 0);
}

void spinRight(int speed) {
  analogWrite(PIN_IN1, speed);
  analogWrite(PIN_IN2, 0);
  analogWrite(PIN_IN3, 0);
  analogWrite(PIN_IN4, speed);
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_IN1, OUTPUT);
  pinMode(PIN_IN2, OUTPUT);
  pinMode(PIN_IN3, OUTPUT);
  pinMode(PIN_IN4, OUTPUT);
  pinMode(PIN_WEAPON, OUTPUT);
  pinMode(PIN_LED, OUTPUT);
  stopMotors();

  // Nome do dispositivo que aparecerá ao buscar Bluetooth no celular
  SerialBT.begin("Robo-Combate-BT");
  Serial.println("[BT] Bluetooth pronto! Pareie com 'Robo-Combate-BT'.");
  lastCommandTime = millis();
}

void loop() {
  if (SerialBT.available()) {
    char cmd = SerialBT.read();
    lastCommandTime = millis();
    failsafeTriggered = false;
    digitalWrite(PIN_LED, HIGH);

    switch (cmd) {
      case 'F': // Frente
        moveForward(currentSpeed);
        break;
      case 'B': // Ré
        moveBackward(currentSpeed);
        break;
      case 'L': // Giro Esquerda
        spinLeft(currentSpeed);
        break;
      case 'R': // Giro Direita
        spinRight(currentSpeed);
        break;
      case 'S': // Parar
        stopMotors();
        break;
      case 'W': // Toggle Arma
        weaponActive = !weaponActive;
        digitalWrite(PIN_WEAPON, weaponActive ? HIGH : LOW);
        SerialBT.println(weaponActive ? "Arma: LIGADA" : "Arma: DESLIGADA");
        break;
      // Comandos de velocidade padrão do app Bluetooth RC (0 a 9 e q)
      case '0': currentSpeed = 0; break;
      case '5': currentSpeed = 130; break;
      case '9': currentSpeed = 230; break;
      case 'q': currentSpeed = 255; break;
    }
  }

  // Failsafe Watchdog
  if (!failsafeTriggered && (millis() - lastCommandTime > FAILSAFE_TIMEOUT_MS)) {
    failsafeTriggered = true;
    stopMotors();
    weaponActive = false;
    digitalWrite(PIN_WEAPON, LOW);
    digitalWrite(PIN_LED, LOW);
  }
}
