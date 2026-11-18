# 🕹️ Robô de Combate: Versão Arduino (Uno / Nano) + Módulo Bluetooth HC-05

Guia completo de ligação elétrica, configuração e pilotagem do robô de combate utilizando **Arduino Uno** ou **Arduino Nano**, módulo **Bluetooth HC-05** e **módulo Ponte H (L298N / TB6612FNG)**.

---

## 📋 Lista de Materiais Adicionais

- **1x Placa Arduino Uno ou Arduino Nano** (ATmega328P)
- **1x Módulo Bluetooth HC-05** (ou HC-06)
- **1x Módulo Ponte H L298N** (ou mini TB6612FNG)
- **2x Motores DC com redução**
- **1x Resistor de 1kΩ e 1x Resistor de 2kΩ** (para o divisor de tensão no pino RX do HC-05)
- **1x Bateria LiPo 2S (7.4V) ou Pack 2x 18650**
- **1x Chave Geral (Kill Switch)**
- **Módulo Relé ou MOSFET** (opcional, para arma ativa)

---

## 🔌 Esquema Elétrico de Conexão

![Circuito Robô de Combate Arduino + HC-05 (Estilo Tinkercad)](../docs/images/circuito_arduino_hc05.jpg)

```
                     +-------------------+
                     |   Bateria LiPo    |
                     |  (7.4V a 11.1V)   |
                     +----+---------+----+
                     (+)  |         | (-)
                          |         |
                   [Chave Geral]    |
                          |         |
                          |         +-------------------------+
                          v                                   |
                  +---------------+                           |
                  |     L298N     |                           |
                  |               |                           |
                  | 12V / VMS <---+                           |
                  | GND       <-------------------------------+
                  | 5V Out    +---------------+               |
                  |               |           |               |
                  | IN1 <----+    |           |               |
                  | IN2 <----+    |           |               |
                  | IN3 <----+    |           |               |
                  | IN4 <----+    |           |               |
                  +---------------+           |               |
                                              |               |
            +---------------------------------+               |
            |                                                 v
            v                                           +-----------+
      +-----------+                                     |    GND    |
      | 5V / VIN  |                                     |  Arduino  |
      |           |                                     +-----------+
      |  ARDUINO  |
      | UNO / NANO|
      |           |
      |   D2 (RX) <============= TXD do HC-05
      |           |
      |   D3 (TX) +---[ 1kΩ ]---+======> RXD do HC-05 (3.3V Seguro)
      |           |             |
      |           |          [ 2kΩ ]
      |           |             |
      |           |            GND
      |           |
      |   D5 (PWM) ------------> IN1 (Motor Esquerdo Frente)
      |   D6 (PWM) ------------> IN2 (Motor Esquerdo Ré)
      |   D9 (PWM) ------------> IN3 (Motor Direito Frente)
      |  D10 (PWM) ------------> IN4 (Motor Direito Ré)
      |   D4 (DIG) ------------> Sinal da Arma (Relé/MOSFET)
      +-----------+
```

---

## 📌 Tabela de Ligações dos Pinos

### 1. Módulo Bluetooth HC-05 para Arduino:
| Pino HC-05 | Pino Arduino | Observações |
| :--- | :--- | :--- |
| **VCC** | `5V` | Alimentação do módulo |
| **GND** | `GND` | Terra comum |
| **TXD** | `D2` | O sinal de 3.3V do HC-05 é reconhecido perfeitamente pelo pino digital do Arduino |
| **RXD** | `D3` *(via divisor)* | **ATENÇÃO**: O pino RXD do HC-05 opera em 3.3V. Use o divisor de 1kΩ + 2kΩ para não danificar o módulo! |

> [!IMPORTANT]
> **Por que usar os pinos D2 e D3 (SoftwareSerial)?**
> Usamos a biblioteca `SoftwareSerial` nos pinos 2 e 3 para deixar os pinos **D0 (RX) e D1 (TX)** do Arduino livres. Dessa forma, você pode gravar novos códigos no Arduino pela USB sem precisar desconectar o módulo Bluetooth toda vez!

---

### 2. Arduino para Módulo Ponte H (L298N):
| Pino Arduino | Pino L298N | Função |
| :--- | :--- | :--- |
| `D5` (PWM) | **IN1** | Motor Esquerdo - Frente |
| `D6` (PWM) | **IN2** | Motor Esquerdo - Ré |
| `D9` (PWM) | **IN3** | Motor Direito - Frente |
| `D10` (PWM)| **IN4** | Motor Direito - Ré |
| *Deixar jumpers* | **ENA e ENB** | Mantenha os jumpers pretos colocados na ponte H |
| `GND` | **GND** | **Obrigatório**: Unir o GND do Arduino ao GND do L298N e da bateria |
| `5V` (ou VIN) | **5V Out** | Alimenta o Arduino a partir do regulador do L298N |

---

## 📱 Pareamento e Conexão no Celular

1. Ligue a alimentação do robô. O LED do HC-05 começará a **piscar rapidamente** (indicando que está aguardando conexão).
2. No celular (Android), abra **Configurações** > **Bluetooth** e toque em **Procurar dispositivos**.
3. Selecione o dispositivo:
   - Nome: **`HC-05`** (ou `HC-06`)
   - Senha / PIN de pareamento: **`1234`** ou **`0000`**
4. Abra o aplicativo **"Bluetooth RC Controller"** (disponível gratuitamente na Google Play Store).
5. Toque no ícone de engrenagem / conectar e selecione o **`HC-05`**.
6. O LED do HC-05 mudará o ritmo de piscar (piscará pausado a cada 2 segundos), indicando que está **conectado**!

---

## 🎮 Comandos do Aplicativo

- **Setas**: Avanço (`F`), Ré (`B`), Giro no próprio eixo para esquerda (`L`) e direita (`R`).
- **Soltar o controle**: Envia `S` (parada imediata dos motores).
- **Botão de Ação / Triângulo**: Envia `W`, que alterna o estado da arma (`PIN_WEAPON` no pino D4).
- **Controle de Potência (Slider)**: O app envia velocidades de `0` a `9` e `q` (100%), permitindo dosar a aceleração dos motores.

---

## 🛡️ Failsafe de Segurança (Watchdog)

O código possui um temporizador de segurança em tempo real:
- Se a conexão Bluetooth cair por qualquer motivo ou o celular sair do raio de alcance por mais de **500 milissegundos**, o Arduino entra em modo de segurança:
  1. Todos os motores são desenergizados (`stopMotors()`).
  2. A arma é desarmada imediatamente.
  3. O LED onboard (D13) apaga.
