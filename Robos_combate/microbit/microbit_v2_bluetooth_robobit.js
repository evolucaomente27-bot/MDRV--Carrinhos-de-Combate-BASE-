/**
 * =====================================================================================
 * PROJETO: ROBÔ DE COMBATE BBC MICRO:BIT V2 - CONTROLADO PELO CELULAR (BLUETOOTH BLE)
 * Hardware do Robô: BBC micro:bit V2 + Shield 4tronix Robo:Bit (Mk1, Mk2 ou Mk3)
 * Plataforma: Microsoft MakeCode (makecode.microbit.org)
 * =====================================================================================
 * 
 * VANTAGENS DESTA VERSÃO:
 *  - NÃO PRECISA DE UM SEGUNDO MICRO:BIT PARA PILOTAR!
 *  - Conecta diretamente ao seu Celular (Android, iPhone ou PC) via Bluetooth Low Energy.
 *  - Compatível com a página Web Bluetooth (controle_celular_web_bluetooth.html)
 *    ou qualquer aplicativo de terminal BLE (Serial Bluetooth Terminal, nRF Toolbox, etc).
 * 
 * COMO CONFIGURAR NO MAKECODE:
 *  1. Acesse: https://makecode.microbit.org
 *  2. Crie um "Novo Projeto" (ex: "RoboBit-Celular-V2").
 *  3. No menu da engrenagem (canto superior direito), clique em "Extensões" (Extensions).
 *  4. Busque por "bluetooth" e adicione a extensão oficial (aceite remover o rádio).
 *  5. Clique novamente na engrenagem ➔ "Configurações do Projeto" (Project Settings).
 *  6. Ative a opção: "No Pairing Required: Anyone can connect via Bluetooth"
 *     (Isso permite conectar o celular direto sem precisar parear código de 6 dígitos!).
 *  7. Mude a visualização para "JavaScript" no topo central, cole este código e Baixe (.hex).
 * =====================================================================================
 */

// ==========================================
// PINOS DO SHIELD 4TRONIX ROBO:BIT
// ==========================================
// Motor Esquerdo: P0 (Velocidade PWM), P8 (Sentido: 0=Frente, 1=Ré)
// Motor Direito:  P1 (Velocidade PWM), P12 (Sentido: 0=Frente, 1=Ré)
// Arma / MOSFET:  P16 (0 = Desligado, 1 = Ligado)

let conectado = false;
let ultimoSinal = input.runningTime();
let armaAtiva = false;

// Inicialização dos pinos
pararMotores();

// ==========================================
// INICIALIZAÇÃO DO SERVIÇO BLUETOOTH UART
// ==========================================
bluetooth.startUartService();

// Feedback ao ligar (aguardando conexão)
basic.showIcon(IconNames.Diamond);

// Evento: Celular Conectou
bluetooth.onBluetoothConnected(function () {
    conectado = true;
    ultimoSinal = input.runningTime();
    basic.showIcon(IconNames.Happy);
    basic.pause(500);
    basic.showIcon(IconNames.SmallDiamond);
});

// Evento: Celular Desconectou
bluetooth.onBluetoothDisconnected(function () {
    conectado = false;
    pararMotores();
    basic.showIcon(IconNames.Sad);
});

// ==========================================
// FUNÇÕES DE CONTROLE DOS MOTORES
// ==========================================
function pararMotores() {
    pins.digitalWritePin(DigitalPin.P8, 0);
    pins.analogWritePin(AnalogPin.P0, 0);
    pins.digitalWritePin(DigitalPin.P12, 0);
    pins.analogWritePin(AnalogPin.P1, 0);
    pins.digitalWritePin(DigitalPin.P16, 0);
    armaAtiva = false;
}

function setMotorEsquerdo(vel: number) {
    vel = Math.max(-1023, Math.min(1023, vel));
    if (Math.abs(vel) < 40) {
        pins.digitalWritePin(DigitalPin.P8, 0);
        pins.analogWritePin(AnalogPin.P0, 0);
    } else if (vel > 0) {
        pins.digitalWritePin(DigitalPin.P8, 0);
        pins.analogWritePin(AnalogPin.P0, vel);
    } else {
        pins.digitalWritePin(DigitalPin.P8, 1);
        pins.analogWritePin(AnalogPin.P0, 1023 - Math.abs(vel));
    }
}

function setMotorDireito(vel: number) {
    vel = Math.max(-1023, Math.min(1023, vel));
    if (Math.abs(vel) < 40) {
        pins.digitalWritePin(DigitalPin.P12, 0);
        pins.analogWritePin(AnalogPin.P1, 0);
    } else if (vel > 0) {
        pins.digitalWritePin(DigitalPin.P12, 0);
        pins.analogWritePin(AnalogPin.P1, vel);
    } else {
        pins.digitalWritePin(DigitalPin.P12, 1);
        pins.analogWritePin(AnalogPin.P1, 1023 - Math.abs(vel));
    }
}

function acionarMotores(velL: number, velR: number) {
    setMotorEsquerdo(velL);
    setMotorDireito(velR);
}

// ==========================================
// PROCESSAMENTO DE PACOTES VINDOS DO CELULAR
// ==========================================
function processarComando(cmd: string) {
    cmd = cmd.trim();
    if (cmd.length == 0) return;

    ultimoSinal = input.runningTime();

    // 1. Comando de Joystick Analógico Contínuo: "D:<velL>,<velR>"
    if (cmd.indexOf("D:") == 0) {
        let partes = cmd.substr(2).split(",");
        if (partes.length == 2) {
            let velL = parseInt(partes[0]);
            let velR = parseInt(partes[1]);

            // Se o app mandar normalizado (-100 a +100), escalona para 0..1023
            if (Math.abs(velL) <= 100 && Math.abs(velR) <= 100 && (velL != 0 || velR != 0)) {
                velL = Math.round((velL / 100) * 1023);
                velR = Math.round((velR / 100) * 1023);
            }

            acionarMotores(velL, velR);

            // Animação direcional na matriz 5x5
            if (velL > 300 && velR > 300) {
                basic.showArrow(ArrowNames.North);
            } else if (velL < -300 && velR < -300) {
                basic.showArrow(ArrowNames.South);
            } else if (velL > 300 && velR < -300) {
                basic.showArrow(ArrowNames.East);
            } else if (velL < -300 && velR > 300) {
                basic.showArrow(ArrowNames.West);
            } else if (velL == 0 && velR == 0) {
                basic.showIcon(IconNames.SmallDiamond);
            }
        }
    }
    // 2. Comandos Direcionais Rápidos (D-Pad de Aplicativos Móveis)
    else if (cmd == "F") { // Frente
        acionarMotores(850, 850);
        basic.showArrow(ArrowNames.North);
    } else if (cmd == "B") { // Ré
        acionarMotores(-850, -850);
        basic.showArrow(ArrowNames.South);
    } else if (cmd == "L") { // Giro Esquerda
        acionarMotores(-750, 750);
        basic.showArrow(ArrowNames.West);
    } else if (cmd == "R") { // Giro Direita
        acionarMotores(750, -750);
        basic.showArrow(ArrowNames.East);
    } else if (cmd == "S") { // Parada
        acionarMotores(0, 0);
        basic.showIcon(IconNames.SmallDiamond);
    }
    // 3. Comandos Táticos de Combate
    else if (cmd == "T" || cmd == "TURBO") { // Turbo 100%
        basic.showIcon(IconNames.Skull);
        acionarMotores(1023, 1023);
    } else if (cmd == "G" || cmd == "T180") { // Giro 180°
        basic.showIcon(IconNames.Surprised);
        acionarMotores(1023, -1023);
        basic.pause(260);
        pararMotores();
        basic.showIcon(IconNames.SmallDiamond);
    } else if (cmd == "X" || cmd == "ARMA_ON") { // Liga Arma
        pins.digitalWritePin(DigitalPin.P16, 1);
        armaAtiva = true;
        basic.showIcon(IconNames.Sword);
    } else if (cmd == "x" || cmd == "ARMA_OFF") { // Desliga Arma
        pins.digitalWritePin(DigitalPin.P16, 0);
        armaAtiva = false;
        basic.showIcon(IconNames.SmallDiamond);
    }
}

// Receptor de dados via Bluetooth UART
bluetooth.onUartDataReceived(serial.delimiters(Delimiters.NewLine), function () {
    let msg = bluetooth.uartReadUntil(serial.delimiters(Delimiters.NewLine));
    processarComando(msg);
});

// ==========================================
// WATCHDOG FAILSAFE DE SEGURANÇA (500ms)
// ==========================================
// Se o celular desconectar ou parar de enviar pacotes por mais de 500ms, o robô para!
basic.forever(function () {
    if (conectado && (input.runningTime() - ultimoSinal > 500)) {
        pararMotores();
        basic.showIcon(IconNames.No);
    }
    basic.pause(60);
});
