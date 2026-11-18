# 🤖 Robô de Combate BBC micro:bit com Shield Robo:Bit

Este diretório contém o firmware completo e documentação para montar e programar o robô de combate usando a placa de expansão profissional **4tronix Robo:Bit** (compatível com Mk1, Mk2 e Mk3).

---

## ⚡ Por que usar o Shield Robo:Bit?

Em comparação com a montagem tradicional usando fios jumper e Ponte H L298N externa:
* **Conexão Direta (Zero Fios de Sinal):** O micro:bit encaixa diretamente no conector de borda de 40 pinos.
* **Bornes de Parafuso Industriais:** Os fios dos motores DC são parafusados com firmeza, evitando que se soltem durante colisões e impactos na arena.
* **Driver H-Bridge Integrado:** Circuito de alta eficiência térmica com controle PWM suave de velocidade e inversão de sentido.
* **Alimentação Unificada e Chave Liga/Desliga:** Interruptor ON/OFF geral na própria placa, com regulador de 3.3V integrado para proteger o micro:bit.
* **Barramento de Expansão:** Pinos dedicados (P16, P14, P15, P2, 3V, GND) para acionar armas ativas (MOSFET/disco de giro), servo motor para cunhas ou sensores ultrassônicos.

---

## 📁 Arquivos Inclusos

| Arquivo | Descrição | Plataforma |
| :--- | :--- | :--- |
| [robobit_robot.js](file:///c:/Users/user/Documents/antigravity/blissful-darwin/microbit/robobit_robot.js) | Firmware receptor usando a extensão oficial `4tronix/Robobit` | Microsoft MakeCode |
| [robobit_robot.py](file:///c:/Users/user/Documents/antigravity/blissful-darwin/microbit/robobit_robot.py) | Firmware receptor nativo com driver PWM direto dos pinos P0/P8 e P1/P12 | MicroPython (Mu / Thonny) |
| [como_montar_robobit.txt](file:///c:/Users/user/Documents/antigravity/blissful-darwin/microbit/como_montar_robobit.txt) | Guia detalhado de montagem mecânica, elétrica e testes em bancada | Guia Técnico |
| [makecode_controller.js](file:///c:/Users/user/Documents/antigravity/blissful-darwin/microbit/makecode_controller.js) | Firmware transmissor na mão (Joystick por acelerômetro, Turbo e Giro 180°) | MakeCode Transmissor |
| [controle_microbit_transmissor.py](file:///c:/Users/user/Documents/antigravity/blissful-darwin/microbit/controle_microbit_transmissor.py) | Firmware transmissor em MicroPython para quem prefere Python | MicroPython Transmissor |

---

## 🚀 Opção 1: Programando com Microsoft MakeCode (Recomendado)

1. Acesse o editor oficial: **[https://makecode.microbit.org](https://makecode.microbit.org)**.
2. Crie um **Novo Projeto** (ex: *Robo-Combate-RoboBit*).
3. **Instale a Extensão Robo:Bit**:
   * Clique no ícone de engrenagem no canto superior direito e selecione **Extensões** (Extensions).
   * No campo de busca, digite `Robobit` ou cole a URL: `https://github.com/4tronix/Robobit`.
   * Clique no card da extensão oficial da **4tronix** para adicioná-la. Uma aba laranja chamada **Robobit** aparecerá no menu lateral.
4. Mude a visualização do editor de **Blocos** para **JavaScript** (no topo).
5. Abra o arquivo [robobit_robot.js](file:///c:/Users/user/Documents/antigravity/blissful-darwin/microbit/robobit_robot.js), copie todo o seu conteúdo e cole no editor.
6. Se quiser ver os blocos visuais coloridos montados, basta clicar novamente em **Blocos**!
7. Conecte o micro:bit no computador via cabo USB e clique em **Baixar** (Download) para gravar o arquivo `.hex`.

---

## 🐍 Opção 2: Programando com MicroPython

Se você prefere programar em Python ou usa o Mu Editor / Thonny:
1. Abra o arquivo [robobit_robot.py](file:///c:/Users/user/Documents/antigravity/blissful-darwin/microbit/robobit_robot.py).
2. Abra o [Python Editor Oficial da micro:bit](https://python.microbit.org) ou o **Mu Editor**.
3. Conecte o micro:bit via USB e clique em **Flash** (Gravar).
4. O código inclui um driver integrado que gerencia o sinal PWM e sentido nos pinos `P0/P8` e `P1/P12` automaticamente.

---

## 🎮 Comandos de Combate pelo Controle Remoto

| Movimento / Ação | Controle Remoto (Transmissor) | Efeito no Robô Robo:Bit | Feedback na Tela 5x5 |
| :--- | :--- | :--- | :---: |
| **Frente / Ré / Curvas** | Inclinar a placa como manche analógico | Movimentação proporcional com controle contínuo | Seta direcional (↑, ↓, ←, →) |
| **Parado (Neutro)** | Controle na horizontal | Motores param em modo livre (Coast) | Pequeno Diamante (◆) |
| **Ataque TURBO** | Pressionar e segurar o **Botão A** | 100% de PWM nos dois motores (empurrão total) | Caveira (💀) |
| **Giro 180° Tático** | Pressionar o **Botão B** | Meia volta instantânea sobre o próprio eixo | Ícone de Espanto (😲) |
| **Arma de Combate** | Pressionar **A + B** simultaneamente | Ativa saída digital no pino P16 (MOSFET/Relé) | Espada (⚔) |
| **Failsafe (Sem Sinal)** | Desligar transmissor ou sair do alcance | Motores desligados após 400ms sem pacotes | Ícone X (❌) |

---

## 🔧 Mapeamento de Pinos Físicos

| Linha | Pino Micro:bit | Descrição na Placa Robo:Bit |
| :--- | :--- | :--- |
| **Motor Esquerdo** | `P0` (PWM) + `P8` (Sentido) | Terminal de Parafuso `LEFT` |
| **Motor Direito** | `P1` (PWM) + `P12` (Sentido) | Terminal de Parafuso `RIGHT` |
| **Arma / Acessório** | `P16` (Sinal Digital) | Barra de pinos livres |
| **Alimentação** | Suporte 4x AA (6V) ou LiPo 2S (7.4V) | Chave ON/OFF integrada |
