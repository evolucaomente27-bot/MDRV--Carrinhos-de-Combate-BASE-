# 🤖 MDRV - Carrinhos e Robôs de Combate (Base Completa)

Projeto completo, moderno e didático para construção de **Robôs de Batalha / Combate** controlados remotamente por smartphone ou controle dedicado, com sistema de segurança obrigatório de **Failsafe** em tempo real.

O projeto é modular e suporta **4 plataformas completas de hardware**:

1. **BBC micro:bit V2 (Bluetooth BLE Direto no Celular)**: Não precisa de um segundo micro:bit! Conecta diretamente ao celular via Web Bluetooth (Google Chrome / Bluefy) com Joystick Analógico Touch 360°, Turbo 100%, Giro 180° e gatilho de arma.
2. **BBC micro:bit (Rádio Integrado 2.4GHz <2ms)**: Opção de controle dedicado segurado na mão (joystick 3D por acelerômetro) compatível com o **Shield 4tronix Robo:Bit** e Ponte H L298N.
3. **ESP32 (Wi-Fi Web Controller + SoftAP)**: Cria rede Wi-Fi própria, acessível via navegador em `192.168.4.1`, com suporte à montagem em protoboard com módulo fonte MB102.
4. **Arduino Uno / Nano + Módulo HC-05**: Comunicação Bluetooth serial clássica com divisor de tensão resistivo protetor e failsafe.
5. **App Mobile & Desktop em Flutter**: Aplicativo multiplataforma (Android, iOS, Web e Windows) nativo com Joystick CustomPainter, D-Pad, telemetria bidirecional, trim e personalização de temas.

---

## 📋 Sumário
1. [Plataformas de Robôs](#-plataformas-de-robôs)
   - [Opção 1: BBC micro:bit V2 (Bluetooth BLE pelo Celular)](#opção-1-bbc-microbit-v2-bluetooth-ble-pelo-celular)
   - [Opção 2: BBC micro:bit + Shield 4tronix Robo:Bit](#opção-2-bbc-microbit--shield-4tronix-robobit)
   - [Opção 3: ESP32 (Wi-Fi Web Controller)](#opção-3-esp32-wi-fi-web-controller)
   - [Opção 4: Arduino Uno / Nano + HC-05](#opção-4-arduino-uno--nano--hc-05)
2. [Aplicativo de Controle em Flutter](#-aplicativo-de-controle-em-flutter)
3. [Lista de Materiais (BOM)](#-lista-de-materiais-bom)
4. [Esquemas Visuais de Ligação Elétrica](#-esquemas-visuais-de-ligação-elétrica)
5. [Sistema de Failsafe (Regras de Competição)](#-sistema-de-failsafe-regras-de-competição)
6. [Estrutura Completa do Repositório](#-estrutura-completa-do-repositório)

---

## ⚡ Plataformas de Robôs

### Opção 1: BBC micro:bit V2 (Bluetooth BLE pelo Celular)
* **Vantagem Principal**: **Não precisa de um segundo micro:bit para pilotar!** Você utiliza apenas 1 placa micro:bit V2 no chassi do robô e controla diretamente pelo celular.
* **Web Bluetooth**: Basta abrir a página [microbit/controle_celular_web_bluetooth.html](microbit/controle_celular_web_bluetooth.html) no Google Chrome ou Samsung Internet (Android) ou Bluefy (iOS) para pilotar via tela de toque.
* **Firmwares MakeCode**:
  - Para Shield 4tronix Robo:Bit: [`microbit/microbit_v2_bluetooth_robobit.js`](microbit/microbit_v2_bluetooth_robobit.js)
  - Para Shield KittenBot Robot:bit (com Bateria 18650, M1 e M2): [`microbit/robotbit_kittenbot_v2_bluetooth.js`](microbit/robotbit_kittenbot_v2_bluetooth.js)
  - Para Ponte H L298N: [`microbit/microbit_v2_bluetooth_l298n.js`](microbit/microbit_v2_bluetooth_l298n.js)
* **Guia Completo**: [`microbit/como_controlar_pelo_celular.txt`](microbit/como_controlar_pelo_celular.txt) e [`microbit/README_BLUETOOTH_V2.md`](microbit/README_BLUETOOTH_V2.md)

---

### Opção 2: BBC micro:bit + Shield 4tronix Robo:Bit
* **Conexão Direta (Zero Fios de Placa)**: O micro:bit é inserido no slot vertical de 40 pinos do shield. Os motores são parafusados com firmeza nos bornes industriais.
* **Rádio 2.4GHz Nativo**: Latência ultrabaixa (<2ms) sem necessidade de roteador Wi-Fi.
* **Controle Transmissor (Na Mão)**: Incline o micro:bit transmissor como um manche de avião para acelerar e fazer curvas fluidas.
* **Firmwares**:
  - MakeCode Shield Robo:Bit: [`microbit/robobit_robot.js`](microbit/robobit_robot.js)
  - MicroPython Shield Robo:Bit: [`microbit/robobit_robot.py`](microbit/robobit_robot.py)
  - Transmissor MakeCode: [`microbit/makecode_controller.js`](microbit/makecode_controller.js)
* **Guia e Manual**: [`microbit/como_montar_robobit.txt`](microbit/como_montar_robobit.txt) e [`microbit/README_ROBOBIT.md`](microbit/README_ROBOBIT.md)

---

### Opção 3: ESP32 (Wi-Fi Web Controller)
* **Sem necessidade de apps**: O ESP32 cria um ponto de acesso Wi-Fi próprio (`Robo-Combate`). Ao conectar o smartphone, a interface web touch abre no navegador em `192.168.4.1`.
* **Módulo Fonte MB102**: Suporta montagem limpa em protoboard alimentada por fonte MB102 para evitar resets por queda de tensão (*brownout*).
* **Firmware**: [`ESP32/robo_combate/robo_combate.ino`](ESP32/robo_combate/robo_combate.ino)
* **Guias**: [`como_montar_esp32.txt`](como_montar_esp32.txt) e [`como_montar_esp32_protoboard.txt`](como_montar_esp32_protoboard.txt)

---

### Opção 4: Arduino Uno / Nano + HC-05
* **Bluetooth Serial Clássico**: Comunicação direta com aplicativos móveis (Serial Bluetooth Terminal, Arduino Bluetooth RC, etc).
* **Divisor de Tensão Resistivo**: Resistores de 1kΩ e 2kΩ protegem a entrada RXD de 3.3V do módulo HC-05 contra os 5V do Arduino.
* **Firmware**: [`arduino_hc05/robo_combate_arduino_hc05.ino`](arduino_hc05/robo_combate_arduino_hc05.ino)
* **Guia e Manual**: [`arduino_hc05/como_montar_arduino_hc05.txt`](arduino_hc05/como_montar_arduino_hc05.txt) e [`arduino_hc05/README_ARDUINO.md`](arduino_hc05/README_ARDUINO.md)

---

## 🎮 Aplicativo de Controle em Flutter (`flutter_controller/`)

Aplicativo nativo desenvolvido em Flutter para Android, iOS, Web e Desktop:
* **Rendering a 60/120 FPS**: Construído com `CustomPainter` para mínima latência de toque.
* **Ergonomia e Personalização**:
  - Modo Canhoto e Destro (inversão da posição do analógico e botões).
  - 5 Temas Industriais (*Obsidian Blue, Cyber Emerald, Crimson Fury, Amber Stealth, Titanium Minimal*).
  - Trim de calibração de direção (-25% a +25%) para robôs que puxam para o lado.
  - Teto de potência, curva de sensibilidade e remapeamento de botões táticos.
* **Código Fonte**: Pasta [`flutter_controller/`](flutter_controller/)
* **Guia de Uso**: [`como_usar_controle_flutter.txt`](como_usar_controle_flutter.txt)

---

## 📦 Lista de Materiais (BOM)

| Componente | Quantidade | Observações / Recomendação |
| :--- | :---: | :--- |
| **Placa de Controle** | 1 | BBC micro:bit V2, ESP32 DevKit ou Arduino Uno/Nano |
| **Módulo Driver de Motores** | 1 | Shield 4tronix Robo:Bit, Ponte H L298N ou TB6612FNG |
| **Motores DC com Caixa de Redução** | 2 | Motores TT amarelos (iniciante) ou Micro Metal Gear N20 / 25GA |
| **Bateria Principal** | 1 | 4x Pilhas AA (6V) ou Bateria LiPo 2S (7.4V) |
| **Chave Geral (Kill Switch)** | 1 | Chave de alavanca reforçada ou integrada no shield |
| **Módulo de Arma (Opcional)** | 1 | Módulo MOSFET ou mini servo para disco/cunha |
| **Rodas de Borracha** | 2 | Rodas de alto coeficiente de atrito para combate |
| **Roda Boba (Caster Ball)** | 1 | Apoio de 3 pontos para giro suave |

---

## 🔌 Esquemas Visuais de Ligação Elétrica

O projeto conta com diagramas de alta definição (1920x1080) com renderização estilo Tinkercad:

| Diagrama | Imagem | Descrição |
| :--- | :---: | :--- |
| **micro:bit V2 + Celular (BLE)** | [`circuito_microbit_v2_bluetooth.jpg`](circuito_microbit_v2_bluetooth.jpg) | Celular conectado via Web Bluetooth BLE diretamente ao micro:bit V2 |
| **micro:bit + Shield Robo:Bit** | [`circuito_microbit_robobit.jpg`](circuito_microbit_robobit.jpg) | Encaixe direto no slot de 40 pinos com bornes de parafuso |
| **micro:bit + Ponte H L298N** | [`circuito_microbit_l298n.jpg`](circuito_microbit_l298n.jpg) | micro:bit conectado à ponte H externa via pinos P0, P1, P8, P12 |
| **ESP32 + Protoboard MB102** | [`circuito_esp32_protoboard.jpg`](circuito_esp32_protoboard.jpg) | ESP32 alimentado de forma estável pelo módulo MB102 |
| **ESP32 + Ponte H L298N** | [`circuito_esp32_l298n.jpg`](circuito_esp32_l298n.jpg) | Montagem direta do ESP32 com L298N |
| **Arduino Uno + HC-05** | [`circuito_arduino_hc05.jpg`](circuito_arduino_hc05.jpg) | Arduino com módulo Bluetooth HC-05 e divisor resistivo |

---

## 🛡️ Sistema de Failsafe (Regras de Competição)

Nas principais competições de robótica de combate, o sistema de **Failsafe** é item obrigatório de segurança:
1. Caso a conexão Bluetooth ou sinal de rádio caia, os motores devem cortar a tração em **menos de 1 segundo**.
2. **Implementação no micro:bit V2**: Watchdog interno de **500ms** desativa imediatamente os pinos de tração e a arma caso pare de receber pacotes.
3. **Implementação no ESP32**: Heartbeat a cada 200ms; desliga motores após 400ms sem comando.
4. **Implementação no Arduino**: Timeout serial de 500ms na leitura do buffer Bluetooth.

---

## 📁 Estrutura Completa do Repositório

```
MDRV--Carrinhos-de-Combate-BASE-/
├── README.md                                  # Este manual consolidado
├── .gitignore                                 # Regras de exclusão
├── lista_de_materiais.txt                     # Checklist de bancada
├── platformio.ini / src/main.cpp              # Build PlatformIO C++
│
├── microbit/                                  # Plataforma BBC micro:bit
│   ├── robotbit_kittenbot_v2_bluetooth.js     # V2 BLE: Celular + KittenBot Robot:bit (M1 e M2)
│   ├── microbit_v2_bluetooth_robobit.js       # V2 BLE: Celular + Shield Robo:Bit
│   ├── microbit_v2_bluetooth_l298n.js         # V2 BLE: Celular + Ponte H L298N
│   ├── controle_celular_web_bluetooth.html    # App Web Bluetooth Touch 360°
│   ├── como_controlar_pelo_celular.txt        # Guia de conexão sem PIN no celular
│   ├── README_BLUETOOTH_V2.md                 # Manual detalhado V2 BLE
│   ├── robobit_robot.js                       # Rádio 2.4GHz: Shield Robo:Bit MakeCode
│   ├── robobit_robot.py                       # Rádio 2.4GHz: Shield Robo:Bit MicroPython
│   ├── makecode_robot.js                      # Rádio 2.4GHz: L298N MakeCode
│   ├── makecode_controller.js                 # Rádio 2.4GHz: Manche Transmissor
│   ├── robo_microbit_receptor.py              # Rádio 2.4GHz: L298N MicroPython
│   ├── controle_microbit_transmissor.py       # Rádio 2.4GHz: Transmissor MicroPython
│   ├── como_montar_robobit.txt                # Montagem do shield Robo:Bit
│   ├── README_ROBOBIT.md                      # Manual do shield Robo:Bit
│   └── README_MICROBIT.md                     # Manual da versão micro:bit clássica
│
├── ESP32/                                     # Plataforma ESP32 Wi-Fi
│   ├── robo_combate/robo_combate.ino          # Firmware principal SoftAP + Web
│   ├── como_montar_esp32.txt                  # Guia de montagem direta
│   └── README.md
│
├── arduino_hc05/                              # Plataforma Arduino + Bluetooth
│   ├── robo_combate_arduino_hc05.ino          # Firmware Arduino Uno / Nano
│   ├── como_montar_arduino_hc05.txt           # Montagem e divisor resistivo
│   └── README_ARDUINO.md
│
├── flutter_controller/                        # App Gamer Multiplataforma (Flutter)
│   ├── lib/ (Joystick, D-Pad, Temas, Trim)
│   └── pubspec.yaml
│
└── Diagramas Visuais em Alta Resolução:
    ├── circuito_microbit_v2_bluetooth.jpg
    ├── circuito_microbit_robobit.jpg
    ├── circuito_microbit_l298n.jpg
    ├── circuito_esp32_protoboard.jpg
    ├── circuito_esp32_l298n.jpg
    └── circuito_arduino_hc05.jpg
```
