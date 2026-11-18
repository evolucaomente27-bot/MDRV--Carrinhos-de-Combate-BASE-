# 🤖 Projeto Robô de Combate com ESP32 e Módulo Ponte H

Projeto completo, moderno e didático para construção de um **Robô de Batalha / Combate** controlado remotamente por smartphone via **Wi-Fi Web Controller** (sem necessidade de instalar nenhum aplicativo ou ter internet) com sistema de segurança obrigatório de **Failsafe** em tempo real.

---

## 📋 Sumário
1. [Características do Projeto](#-características-do-projeto)
2. [Lista de Materiais (BOM)](#-lista-de-materiais-bom)
3. [Esquema de Ligação Elétrica](#-esquema-de-ligação-elétrica)
   - [Opção 1: Módulo Ponte H L298N (Clássico)](#opção-1-módulo-ponte-h-l298n-clássico)
   - [Opção 2: Módulo Mini TB6612FNG (Compacto)](#opção-2-módulo-mini-tb6612fng-compacto)
4. [Alimentação, Chave Geral e Segurança](#-alimentação-chave-geral-e-segurança)
5. [Como Gravar no ESP32](#-como-gravar-no-esp32)
   - [Via Arduino IDE](#via-arduino-ide)
   - [Via PlatformIO (VS Code)](#via-platformio-vs-code)
6. [Como Pilotar pelo Celular](#-como-pilotar-pelo-celular)
7. [Sistema de Failsafe (Regras de Competição)](#-sistema-de-failsafe-regras-de-competição)
8. [Estrutura de Arquivos](#-estrutura-de-arquivos)

---

## ⚡ Características do Projeto

- **Sem aplicativos externos**: O ESP32 cria uma rede Wi-Fi própria (`Robo-Combate`). Basta conectar o celular e abrir o navegador em `192.168.4.1`.
- **Interface Touch Gamer**: D-pad responsivo com acelerador, curvas tipo tanque (giro no próprio eixo) e ajuste contínuo de velocidade (PWM).
- **Controle de Arma/Atuador**: Saída dedicada (GPIO 26) para acionar arma ativa (disco de impacto, cunha móvel, lifter ou spinner via MOSFET/Relé/ESC).
- **Failsafe Ativo (400ms)**: Se o celular sair do alcance, descarregar ou o sinal for perdido, os motores e a arma são desligados imediatamente.
- **Versão Bluetooth Opcional**: Inclui código alternativo para aplicativos Bluetooth Serial clássicos.

---

## 📦 Lista de Materiais (BOM)

| Componente | Quantidade | Observações / Recomendação |
| :--- | :---: | :--- |
| **Placa ESP32** | 1 | NodeMCU-32S ou ESP32 DevKit v1 (30 ou 38 pinos) |
| **Módulo Ponte H** | 1 | L298N (duplo 2A) ou TB6612FNG (mini 1.2A por canal) |
| **Motores DC com Caixa de Redução** | 2 | Motores TT amarelos (para testes) ou Micro Metal Gear N20 / 25GA (para combate) |
| **Bateria** | 1 | LiPo 2S (7.4V) ou 3S (11.1V), ou 2x baterias 18650 em série |
| **Chave Liga/Desliga Geral (Kill Switch)**| 1 | Chave de alavanca reforçada ou conector de segurança XT60 |
| **Módulo Step-Down / Regulador (Opcional)**| 1 | LM2596 ou regulador 5V (recomendado caso use LiPo 3S) |
| **Módulo MOSFET ou Relé (Opcional)** | 1 | Para acionar o motor da arma/disco |
| **Rodas com Alta Tração** | 2 | Rodas emborrachadas de combate ou esteiras |
| **Cabos Jumper e Conectores** | Kit | Jumpers macho-fêmea e fios de alimentação 18-20 AWG |

---

## 🔌 Esquema de Ligação Elétrica

### Opção 1: Módulo Ponte H L298N (Clássico)

O L298N possui um jumper regulador interno de 5V. Quando a bateria for de **7.4V a 12V**, mantenha o jumper de 5V inserido; assim, o pino `+5V` do L298N pode alimentar o pino `VIN` do ESP32!

![Circuito Robô de Combate ESP32 (Estilo Tinkercad)](docs/images/circuito_esp32_l298n.jpg)

```
                 +-------------------+
                 |    Bateria LiPo   |
                 | (7.4V - 11.1V)    |
                 +----+---------+----+
                 (+)  |         | (-)
                      |         |
               [Chave Geral]    |
                      |         |
                      |         +-----------------------+
                      v                                 |
              +---------------+                         |
              |     L298N     |                         |
              |               |                         |
              | 12V / VMS <---+                         |
              | GND       <-----------------------------+
              | 5V Out    +-------------+               |
              |               |         |               |
              | IN1 <----+    |         |               |
              | IN2 <----+    |         |               |
              | IN3 <----+    |         |               |
              | IN4 <----+    |         |               |
              | ENA, ENB |    |         |               |
              | (Jumpers)|    |         |               |
              +---------------+         |               |
                                        v               v
                                 +--------------+--------------+
                                 | VIN          GND            |
                                 |                             |
                                 |           ESP32             |
                                 |                             |
                                 | GPIO 18  -----> IN1 (L298N) |
                                 | GPIO 19  -----> IN2 (L298N) |
                                 | GPIO 22  -----> IN3 (L298N) |
                                 | GPIO 23  -----> IN4 (L298N) |
                                 | GPIO 26  -----> Sinal Arma  |
                                 +-----------------------------+
```

#### Tabela de Conexões L298N:
| L298N | ESP32 | Descrição |
| :--- | :--- | :--- |
| **IN1** | `GPIO 18` | Motor Esquerdo - Sentido Horário |
| **IN2** | `GPIO 19` | Motor Esquerdo - Sentido Anti-horário |
| **IN3** | `GPIO 22` | Motor Direito - Sentido Horário |
| **IN4** | `GPIO 23` | Motor Direito - Sentido Anti-horário |
| **ENA & ENB**| *Manter jumpers pretos originais colocados* | Habilita controle direto por PWM em IN1-IN4 |
| **GND** | `GND` | **OBRIGATÓRIO**: Terra comum entre bateria, ponte H e ESP32 |
| **5V (Saída)**| `VIN (5V)` | Alimenta o ESP32 (caso bateria seja até 12V com jumper ativo) |
| **OUT1 & OUT2**| Motor Esquerdo | Terminais do motor DC esquerdo |
| **OUT3 & OUT4**| Motor Direito | Terminais do motor DC direito |

---

### Opção 2: Módulo Mini TB6612FNG (Compacto)

O TB6612FNG é muito mais eficiente que o L298N (aquece menos e perde menos tensão). Ideal para categorias leves (**Antweight** 454g / **Fairyweight** 150g):

| TB6612FNG | ESP32 / Bateria | Observação |
| :--- | :--- | :--- |
| **VM** | `+ Bateria (7.4V)` | Tensão de força dos motores |
| **VCC** | `3V3 (ESP32)` | Tensão de controle lógico (3.3V) |
| **GND** | `GND (Comum)` | Unir com o GND da bateria e ESP32 |
| **STBY** | `3V3 (ESP32)` | Pino Standby (ligado em nível alto para ativar o driver) |
| **AIN1** | `GPIO 18` | Motor A |
| **AIN2** | `GPIO 19` | Motor A |
| **BIN1** | `GPIO 22` | Motor B |
| **BIN2** | `GPIO 23` | Motor B |
| **PWMA & PWMB**| `3V3` (ou pinos de PWM) | Conecte em 3.3V se controlar velocidade via AIN/BIN |

---

## ⚠️ Alimentação, Chave Geral e Segurança

> [!CAUTION]
> **Regra Número 1 do Combate de Robôs**:
> 1. **GND Unificado**: O polo negativo (-) da bateria, o pino GND da Ponte H e o pino GND do ESP32 **devem obrigatoriamente estar conectados juntos**. Se faltar esse terra comum, os motores terão comportamento instável ou travarão ligados!
> 2. **Chave Geral (Link de Segurança)**: Em competições oficiais, é obrigatório um dispositivo de corte de energia visível e acessível externamente no robô.
> 3. **Nunca alimente motores direto do ESP32**: Motores geram ruído elétrico e picos de corrente reversa (CEMF) que queimam o microcontrolador se ligados aos pinos de 3.3V/5V.

---

## 💻 Como Gravar no ESP32

### Via Arduino IDE:
1. Instale o **Arduino IDE** (versão 2.x recomendada).
2. Vá em `Arquivo` -> `Preferências` e adicione a URL das placas ESP32:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
3. Em `Ferramentas` -> `Placa` -> `Gerenciador de Placas`, pesquise por **esp32** da Espressif e instale.
4. Conecte seu ESP32 via cabo micro-USB / USB-C no computador.
5. Abra o arquivo [`robo_combate.ino`](file:///c:/Users/user/Documents/antigravity/blissful-darwin/robo_combate.ino).
6. Selecione a placa: **ESP32 Dev Module** (ou a variante específica da sua placa) e a respectiva **Porta COM**.
7. Clique em **Upload** (Carregar).
   *(Se a gravação travar em `Connecting...___...`, segure o botão `BOOT` da placa por 2 segundos e solte).*

### Via PlatformIO (VS Code):
1. Abra esta pasta no VS Code com a extensão **PlatformIO IDE** instalada.
2. O arquivo [`platformio.ini`](file:///c:/Users/user/Documents/antigravity/blissful-darwin/platformio.ini) já está configurado.
3. Conecte o ESP32 e clique no ícone de "Visto" (Build) e depois na "Seta para Direita" (Upload) na barra inferior.

---

## 📱 Como Pilotar pelo Celular

1. Ligue a chave geral do robô.
2. No seu smartphone ou notebook, abra as configurações de **Wi-Fi**.
3. Conecte-se à rede:
   - **Nome da Rede (SSID)**: `Robo-Combate`
   - **Senha**: *(Rede aberta sem senha por padrão)*
4. Abra o navegador (Chrome, Safari, Firefox) e digite na barra de endereços:
   ```
   192.168.4.1
   ```
5. Pronto! A central de combate carregará instantaneamente:
   - Toque e segure nos botões do **D-Pad** para movimentar (Frente, Ré, Giros).
   - Ao soltar o botão, o robô para de imediato.
   - Ajuste o cursor de **Potência dos Motores** para dosar a velocidade em manobras precisas.
   - Clique em **ARMA** para acionar o atuador de combate.

---

## 🛡️ Sistema de Failsafe (Regras de Competição)

Nas principais ligas de robótica de combate (como RoboCore no Brasil e eventos internacionais da RobotGames):
- Um robô sem sistema de fail-safe **é desclassificado** por motivos de segurança.
- Caso o transmissor seja desligado ou a conexão caia, o robô deve parar de se mover em menos de **1 segundo**.

### Como funciona o nosso Failsafe:
1. A interface web envia pacotes contínuos de verificação (**Heartbeat**) a cada **200 milissegundos**.
2. O ESP32 monitora esse tempo na variável `lastCommandTime`.
3. Se nenhum comando for recebido dentro de **400ms** (por exemplo: sinal fora de alcance, navegador fechado ou bateria do celular esgotada):
   - A função `stopMotors()` é acionada instantaneamente.
   - A saída da arma (`PIN_WEAPON`) é cortada.
   - O LED onboard apaga.
   - O robô entra em modo inerte seguro até que a conexão seja restabelecida.

---

## 📁 Estrutura de Arquivos

```
blissful-darwin/
├── README.md                      # Este manual completo
├── robo_combate.ino               # Código principal ESP32 (Wi-Fi Web Controller)
├── platformio.ini                 # Configuração para PlatformIO
├── src/
│   └── main.cpp                   # Código-fonte ESP32 para PlatformIO
├── lista_de_materiais.txt         # Checklist completo de peças e ferramentas
├── como_montar_esp32.txt          # Guia de montagem direta do ESP32
├── como_montar_esp32_protoboard.txt # Guia de montagem do ESP32 na Protoboard
├── como_montar_arduino_hc05.txt   # Guia de montagem do Arduino + HC-05
├── data/
│   └── index.html                 # Interface Web visual para testes
├── docs/
│   └── images/                    # Diagramas elétricos estilo Tinkercad (1920x1080)
├── bluetooth_companion/
│   └── robo_combate_bluetooth.ino # Versão ESP32 via Bluetooth Classic
└── arduino_hc05/
    ├── robo_combate_arduino_hc05.ino # Código para Arduino Uno/Nano + HC-05
    └── README_ARDUINO.md             # Manual de montagem e pinagem do Arduino + HC-05
```


