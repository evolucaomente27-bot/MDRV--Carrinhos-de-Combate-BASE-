# 📱 Robô BBC micro:bit V2 - Controle Direto pelo Celular (Bluetooth BLE)

Este módulo traz a solução definitiva para quem deseja usar o **BBC micro:bit V2** no robô de combate **sem precisar de uma segunda placa micro:bit como controle remoto**!

Você pilota o robô diretamente pelo seu **Smartphone (Android, iPhone ou PC)** usando **Bluetooth Low Energy (BLE)** de alta velocidade.

---

## ⚡ Principais Vantagens

1. **Economia de Hardware (1 única placa)**: Você só precisa do micro:bit instalado no chassi do robô.
2. **Web Bluetooth sem Instalação**: Basta abrir o arquivo `controle_celular_web_bluetooth.html` no Google Chrome ou Samsung Internet no celular e pilotar via tela de toque!
3. **Compatível com Aplicativos Gratuitos de Loja**: Funciona também com apps de terminal BLE (como *Serial Bluetooth Terminal*, *Dabble* ou *Bluefruit Connect*).
4. **Suporte a Dois Drivers de Motor**:
   - Versão para o shield integrado **4tronix Robo:Bit** (bornes parafusáveis).
   - Versão para a clássica **Ponte H L298N ou TB6612FNG**.
5. **Failsafe Ativo (500ms)**: Se a conexão Bluetooth cair, o robô para os motores na hora para evitar acidentes na arena.

---

## 📁 Arquivos Deste Módulo

| Arquivo | Descrição | Plataforma |
| :--- | :--- | :--- |
| [microbit_v2_bluetooth_robobit.js](file:///c:/Users/user/Documents/antigravity/blissful-darwin/microbit/microbit_v2_bluetooth_robobit.js) | Firmware MakeCode para micro:bit V2 com **Shield 4tronix Robo:Bit** via BLE | Microsoft MakeCode |
| [microbit_v2_bluetooth_l298n.js](file:///c:/Users/user/Documents/antigravity/blissful-darwin/microbit/microbit_v2_bluetooth_l298n.js) | Firmware MakeCode para micro:bit V2 com **Ponte H L298N** via BLE | Microsoft MakeCode |
| [controle_celular_web_bluetooth.html](file:///c:/Users/user/Documents/antigravity/blissful-darwin/microbit/controle_celular_web_bluetooth.html) | Aplicativo Web de Joystick Touch 360° para navegador do celular (Chrome / Bluefy) | Web Bluetooth API |
| [como_controlar_pelo_celular.txt](file:///c:/Users/user/Documents/antigravity/blissful-darwin/microbit/como_controlar_pelo_celular.txt) | Guia prático de bancada para pareamento sem PIN, testes e apps | Guia Técnico |

---

## 🚀 Como Gravar no micro:bit V2

1. Abra o [Microsoft MakeCode](https://makecode.microbit.org).
2. Crie um **Novo Projeto**.
3. Adicione a extensão oficial:
   - Clique na engrenagem ➔ **Extensões** ➔ Procure por `bluetooth` ➔ Adicione.
4. **Configuração Crucial (Sem Código PIN)**:
   - Clique na engrenagem ➔ **Configurações do Projeto** (*Project Settings*).
   - Ative a opção: **"No Pairing Required: Anyone can connect via Bluetooth"**.
5. Alterne para a aba **JavaScript** no topo, copie o código do arquivo correspondente ([Robo:Bit](file:///c:/Users/user/Documents/antigravity/blissful-darwin/microbit/microbit_v2_bluetooth_robobit.js) ou [L298N](file:///c:/Users/user/Documents/antigravity/blissful-darwin/microbit/microbit_v2_bluetooth_l298n.js)) e cole.
6. Clique em **Baixar** e grave o arquivo `.hex` no micro:bit V2 conectado via USB.

---

## 🎮 Pilotando pelo Celular via Web Bluetooth

1. Transfira ou abra o arquivo [controle_celular_web_bluetooth.html](file:///c:/Users/user/Documents/antigravity/blissful-darwin/microbit/controle_celular_web_bluetooth.html) no celular.
2. Certifique-se de que o **Bluetooth** e a **Localização** estão ativados no smartphone.
3. Clique em **CONECTAR** no topo da página.
4. Selecione o dispositivo que começa com `BBC micro:bit [xxxxx]`.
5. O micro:bit mostrará um rosto sorridente (😊) e o controle estará ativo!

---

## 📡 Protocolo e Comandos Aceitos

| Comando | Descrição | Ação no Robô |
| :--- | :--- | :--- |
| `D:<velL>,<velR>\n` | Pacote do Joystick Analógico | Controle contínuo proporcional com mixagem arcade |
| `F\n` / `B\n` | Frente / Ré direta | Aceleração contínua (85% de potência) |
| `L\n` / `R\n` | Giro Esquerda / Direita | Manobra tipo tanque (rodas em sentidos opostos) |
| `S\n` | Parar (Neutro) | Corta potência de ambos os motores |
| `TURBO\n` / `T\n` | Modo Ataque Turbo | 100% de torque em avanço |
| `T180\n` / `G\n` | Giro Tático de 180° | Meia-volta rápida para contra-ataque |
| `ARMA_ON\n` / `X\n` | Gatilho de Combate | Liga saída digital do pino P16 |
| `ARMA_OFF\n` / `x\n` | Desliga Combate | Desliga saída digital do pino P16 |
