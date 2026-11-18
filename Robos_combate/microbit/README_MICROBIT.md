# 🤖 Robô de Combate BBC micro:bit - Controle por Rádio 2.4GHz e Acelerômetro

Esta versão transforma o **BBC micro:bit (V1 ou V2)** em um robô de combate de alta performance, utilizando o seu **rádio nativo de 2.4GHz** para alcançar uma latência recorde de **menos de 2 milissegundos**, sem necessidade de Wi-Fi, sem roteadores e sem o atraso típico do Bluetooth!

---

## ⚡ Por que o BBC micro:bit é incrível para Robôs de Combate?

1. **Rádio Integrado de Ultra-Baixa Latência (< 2ms)**:
   - Ao contrário do Wi-Fi (que tem atrasos de 40ms a 100ms e exige conexão a uma rede IP), o protocolo `radio` nativo do micro:bit envia pacotes diretos no ar.
   - Resposta instantânea e imediata no volante: o robô responde exatamente no mesmo instante em que você mexe a mão.
2. **Pilotagem por Inclinação 3D (Acelerômetro Embutido)**:
   - Não precisa de joysticks caros nem de telas de celular: basta segurar um segundo micro:bit na mão.
   - Incline para frente para avançar, incline para trás para ré e incline para os lados para fazer curvas dinâmicas ou rodar sobre o próprio eixo!
3. **Display Matriz 5x5 Animado**:
   - Feedback visual instantâneo nos dois micro:bits: setas de direção, ícone de Turbo (caveira), mira, espada e alerta de Failsafe em caso de perda de sinal.
4. **Failsafe Watchdog de 400ms Ativo**:
   - Caso o controle remoto saia do alcance da arena ou a bateria do controle acabe, o micro:bit do robô corta imediatamente todos os canais de motor.

---

## 🔌 Tabela de Conexões (micro:bit ➔ Ponte H L298N)

Para ligar os pinos do micro:bit na Ponte H, recomenda-se usar uma **placa de expansão básica (Edge Connector Breakout ou Sensor Shield)**:

| Pino micro:bit | Pino Ponte H | Função |
| :--- | :--- | :--- |
| **P0** (Anel grande) | `IN1` | Motor Esquerdo - Frente (PWM) |
| **P1** (Anel grande) | `IN2` | Motor Esquerdo - Ré (PWM) |
| **P8** | `IN3` | Motor Direito - Frente (PWM) |
| **P12** | `IN4` | Motor Direito - Ré (PWM) |
| **P16** *(Opcional)* | `Sinal MOSFET/Relé` | Gatilho da Arma / Atuador |
| **GND** (Anel grande) | `GND` | **Terra Comum Unificado** (unido ao (-) da Bateria) |
| *Jumpers* | `ENA` e `ENB` | Mantidos conectados na Ponte H |

> [!IMPORTANT]
> **Alimentação do micro:bit**:
> - O micro:bit opera a **3.3V**. Seus pinos lógicos P0, P1, P8 e P12 entregam 3.3V, o que aciona perfeitamente as entradas TTL do L298N ou da TB6612FNG.
> - O micro:bit do robô pode ser alimentado através do **módulo fonte MB102** (fornecendo 3.3V estáveis), através de um cabo USB de 5V ou pelo conector de 2 pilhas AAA (3V).
> - **NUNCA** conecte o pino de 12V da bateria diretamente no micro:bit!

---

## 🕹️ Como Funciona o Sistema com 2 micro:bits

```
[ PILOTO NA ARENA ]                                [ ROBÔ DE COMBATE ]
┌─────────────────────────┐                        ┌─────────────────────────┐
│  micro:bit Transmissor  │                        │   micro:bit Receptor    │
│  (Controle na Mão)      │     📡 RÁDIO 2.4GHz    │   (Montado no Robô)     │
│                         │ ─────────────────────> │                         │
│ • Acelerômetro 3D       │     Latência < 2ms     │ • PWM nos Pinos P0/P1   │
│ • Botão A (Turbo 100%)  │                        │ • PWM nos Pinos P8/P12  │
│ • Botão B (Meia-volta)  │                        │ • Failsafe Watchdog     │
│ • Combo A+B (Arma)      │                        │ • Display 5x5 Direções  │
└─────────────────────────┘                        └─────────────────────────┘
                                                               │
                                                               ▼
                                                   [ Ponte H L298N / TB6612 ]
                                                               │
                                                               ▼
                                                      [ 2x Motores DC ]
```

---

## 📥 Como Gravar o Código nos micro:bits

Você pode escolher entre duas formas de gravar:

### Opção 1: Via Microsoft MakeCode (Mais Fácil / Plug-and-Play)
1. Conecte o micro:bit no computador via cabo USB (ele aparecerá como um pen drive chamado `MICROBIT`).
2. Acesse no navegador: [makecode.microbit.org](https://makecode.microbit.org)
3. Crie um projeto e mude a aba superior para **JavaScript**.
4. Copie o código correspondente:
   - Para o Robô: [`microbit/makecode_robot.js`](file:///c:/Users/user/Documents/antigravity/blissful-darwin/microbit/makecode_robot.js)
   - Para o Controle: [`microbit/makecode_controller.js`](file:///c:/Users/user/Documents/antigravity/blissful-darwin/microbit/makecode_controller.js)
5. Clique no botão inferior **"Baixar" (Download)** e salve o arquivo `.hex` direto dentro do drive do micro:bit.
6. A luz amarela do micro:bit piscará e ele reiniciará pronto para a batalha!

### Opção 2: Via MicroPython Oficial
1. Acesse [python.microbit.org](https://python.microbit.org)
2. Cole o conteúdo de:
   - [`microbit/robo_microbit_receptor.py`](file:///c:/Users/user/Documents/antigravity/blissful-darwin/microbit/robo_microbit_receptor.py) para o micro:bit do Robô.
   - [`microbit/controle_microbit_transmissor.py`](file:///c:/Users/user/Documents/antigravity/blissful-darwin/microbit/controle_microbit_transmissor.py) para o micro:bit do Controle.
3. Clique em **"Send to micro:bit"** (ou faça download do `.hex`).

---

## 🎮 Comandos do Piloto na Batalha

- **Inclinar para Frente**: Acelera o robô em linha reta com velocidade proporcional ao ângulo.
- **Inclinar para Trás**: Dá marcha ré.
- **Inclinar para as Diagonais**: Executa curvas suaves em movimento com redução proporcional de velocidade na roda interna.
- **Inclinar no Próprio Eixo (Esquerda/Direita puro)**: Giro de tanque de 360° em ponto fixo.
- **Deixar na Horizontal (Reto)**: Freia e para o robô.
- **Botão A**: **TURBO 100%** (força PWM 1023 contínuo para choque e empurrão).
- **Botão B**: **Meia-volta rápida de 180°** para contra-ataque.
- **Botão A + B**: Liga o atuador da arma (P16).
