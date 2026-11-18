/**
 * =====================================================================================
 * PROJETO: ROBÔ DE COMBATE BBC MICRO:BIT V2 - CONTROLADO PELO CELULAR (BLUETOOTH BLE)
 * Hardware do Robô: BBC micro:bit V2 + Ponte H L298N (ou TB6612FNG)
 * Plataforma: Microsoft MakeCode (makecode.microbit.org)
 * =====================================================================================
 * 
 * VANTAGENS DESTA VERSÃO:
 *  - NÃO PRECISA DE UM SEGUNDO MICRO:BIT PARA PILOTAR!
 *  - Conecta diretamente ao seu Celular (Android, iPhone ou PC) via Bluetooth Low Energy.
 *  - Compatível com a página Web Bluetooth (controle_celular_web_bluetooth.html)
 *    ou qualquer aplicativo de terminal BLE (Serial Bluetooth Terminal, nRF Toolbox, etc).
 * 
 * MAPEAMENTO DE PINOS L298N:
 *  - P0  -----> IN1 da Ponte H (Motor Esquerdo Frente)
 *  - P1  -----> IN2 da Ponte H (Motor Esquerdo Ré)
 *  - P8  -----> IN3 da Ponte H (Motor Direito Frente)
 *  - P12 -----> IN4 da Ponte H (Motor Direito Ré)
 *  - P16 -----> Gatilho da Arma (MOSFET / Relé / Servo)
 * =====================================================================================
 */

let conectado = false;
let ultimoSinal = input.runningTime();
let armaAtiva = false;

// Inicialização dos pinos
pararMotores();

// Inicialização do Bluetooth UART
bluetooth.startUartService();
basic.showIcon(IconNames.Diamond);

bluetooth.onBluetoothConnected(function () {
    conectado = true;
    ultimoSinal = input.runningTime();
    basic.showIcon(IconNames.Happy);
    basic.pause(500);
    basic.showIcon(IconNames.SmallDiamond);
});

bluetooth.onBluetoothDisconnected(function () {
    conectado = false;
    pararMotores();
    basic.showIcon(IconNames.Sad);
});

function pararMotores() {
    pins.digitalWritePin(DigitalPin.P0, 0);
    pins.digitalWritePin(DigitalPin.P1, 0);
    pins.digitalWritePin(DigitalPin.P8, 0);
    pins.digitalWritePin(DigitalPin.P12, 0);
    pins.digitalWritePin(DigitalPin.P16, 0);
    armaAtiva = false;
}

function setMotores(esq: number, dir: number) {
    esq = Math.max(-1023, Math.min(1023, esq));
    dir = Math.max(-1023, Math.min(1023, dir));

    // Motor Esquerdo (P0 e P1)
    if (Math.abs(esq) < 40) {
        pins.digitalWritePin(DigitalPin.P0, 0);
        pins.digitalWritePin(DigitalPin.P1, 0);
    } else if (esq > 0) {
        pins.analogWritePin(AnalogPin.P0, esq);
        pins.digitalWritePin(DigitalPin.P1, 0);
    } else {
        pins.digitalWritePin(DigitalPin.P0, 0);
        pins.analogWritePin(AnalogPin.P1, Math.abs(esq));
    }

    // Motor Direito (P8 e P12)
    if (Math.abs(dir) < 40) {
        pins.digitalWritePin(DigitalPin.P8, 0);
        pins.digitalWritePin(DigitalPin.P12, 0);
    } else if (dir > 0) {
        pins.analogWritePin(AnalogPin.P8, dir);
        pins.digitalWritePin(DigitalPin.P12, 0);
    } else {
        pins.digitalWritePin(DigitalPin.P8, 0);
        pins.analogWritePin(AnalogPin.P12, Math.abs(dir));
    }
}

function processarComando(cmd: string) {
    cmd = cmd.trim();
    if (cmd.length == 0) return;

    ultimoSinal = input.runningTime();

    // 1. Comando de Joystick: "D:<velL>,<velR>"
    if (cmd.indexOf("D:") == 0) {
        let partes = cmd.substr(2).split(",");
        if (partes.length == 2) {
            let velL = parseInt(partes[0]);
            let velR = parseInt(partes[1]);

            if (Math.abs(velL) <= 100 && Math.abs(velR) <= 100 && (velL != 0 || velR != 0)) {
                velL = Math.round((velL / 100) * 1023);
                velR = Math.round((velR / 100) * 1023);
            }

            setMotores(velL, velR);

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
    // 2. Comandos D-Pad Rápidos
    else if (cmd == "F") {
        setMotores(850, 850);
        basic.showArrow(ArrowNames.North);
    } else if (cmd == "B") {
        setMotores(-850, -850);
        basic.showArrow(ArrowNames.South);
    } else if (cmd == "L") {
        setMotores(-750, 750);
        basic.showArrow(ArrowNames.West);
    } else if (cmd == "R") {
        setMotores(750, -750);
        basic.showArrow(ArrowNames.East);
    } else if (cmd == "S") {
        setMotores(0, 0);
        basic.showIcon(IconNames.SmallDiamond);
    }
    // 3. Comandos Táticos
    else if (cmd == "T" || cmd == "TURBO") {
        basic.showIcon(IconNames.Skull);
        setMotores(1023, 1023);
    } else if (cmd == "G" || cmd == "T180") {
        basic.showIcon(IconNames.Surprised);
        setMotores(1023, -1023);
        basic.pause(280);
        pararMotores();
        basic.showIcon(IconNames.SmallDiamond);
    } else if (cmd == "X" || cmd == "ARMA_ON") {
        pins.digitalWritePin(DigitalPin.P16, 1);
        armaAtiva = true;
        basic.showIcon(IconNames.Sword);
    } else if (cmd == "x" || cmd == "ARMA_OFF") {
        pins.digitalWritePin(DigitalPin.P16, 0);
        armaAtiva = false;
        basic.showIcon(IconNames.SmallDiamond);
    }
}

bluetooth.onUartDataReceived(serial.delimiters(Delimiters.NewLine), function () {
    let msg = bluetooth.uartReadUntil(serial.delimiters(Delimiters.NewLine));
    processarComando(msg);
});

// Watchdog Failsafe (500ms)
basic.forever(function () {
    if (conectado && (input.runningTime() - ultimoSinal > 500)) {
        pararMotores();
        basic.showIcon(IconNames.No);
    }
    basic.pause(60);
});
