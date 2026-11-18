/**
 * =====================================================================================
 * PROJETO: ROBÔ DE COMBATE BBC MICRO:BIT - FIRMWARE DO RECEPTOR (NO ROBÔ)
 * Plataforma: Microsoft MakeCode (makecode.microbit.org)
 * Modo: JavaScript / Blocos / Python
 * =====================================================================================
 * 
 * Como usar:
 *  1. Acesse o site oficial: https://makecode.microbit.org
 *  2. Crie um "Novo Projeto".
 *  3. Alterne a visualização de "Blocos" para "JavaScript" (no topo central).
 *  4. Cole este código inteiro e clique no botão "Blocos": os blocos visuais se formarão!
 *  5. Clique em "Baixar" (Download) e salve o arquivo .hex dentro do seu micro:bit conectado via USB.
 */

// ==========================================
// CONFIGURAÇÕES DO RÁDIO E FAILSAFE
// ==========================================
const CANAL_RADIO = 7;
radio.setGroup(CANAL_RADIO);
radio.setTransmitPower(7);

let ultimoSinal = input.runningTime();
let failsafeAtivo = true;

// Inicialização dos motores
pararMotores();
basic.showIcon(IconNames.Yes);
basic.pause(300);
basic.clearScreen();

function pararMotores() {
    pins.analogWritePin(AnalogPin.P0, 0);
    pins.digitalWritePin(DigitalPin.P1, 0);
    pins.analogWritePin(AnalogPin.P8, 0);
    pins.digitalWritePin(DigitalPin.P12, 0);
    pins.digitalWritePin(DigitalPin.P16, 0);
    failsafeAtivo = true;
}

function setMotores(esq: number, dir: number) {
    failsafeAtivo = false;
    esq = Math.max(-1023, Math.min(1023, esq));
    dir = Math.max(-1023, Math.min(1023, dir));

    // Motor Esquerdo (P0 e P1)
    if (esq > 0) {
        pins.analogWritePin(AnalogPin.P0, esq);
        pins.digitalWritePin(DigitalPin.P1, 0);
    } else if (esq < 0) {
        pins.digitalWritePin(DigitalPin.P0, 0);
        pins.analogWritePin(AnalogPin.P1, Math.abs(esq));
    } else {
        pins.digitalWritePin(DigitalPin.P0, 0);
        pins.digitalWritePin(DigitalPin.P1, 0);
    }

    // Motor Direito (P8 e P12)
    if (dir > 0) {
        pins.analogWritePin(AnalogPin.P8, dir);
        pins.digitalWritePin(DigitalPin.P12, 0);
    } else if (dir < 0) {
        pins.digitalWritePin(DigitalPin.P8, 0);
        pins.analogWritePin(AnalogPin.P12, Math.abs(dir));
    } else {
        pins.digitalWritePin(DigitalPin.P8, 0);
        pins.digitalWritePin(DigitalPin.P12, 0);
    }
}

// Receptor de Mensagens de Rádio
radio.onReceivedString(function (recebido: string) {
    ultimoSinal = input.runningTime();

    if (recebido.indexOf("D:") == 0) {
        let partes = recebido.substr(2).split(",");
        if (partes.length == 2) {
            let velL = parseInt(partes[0]);
            let velR = parseInt(partes[1]);
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
    } else if (recebido.indexOf("CMD:") == 0) {
        let cmd = recebido.substr(4);
        if (cmd == "TURBO") {
            basic.showIcon(IconNames.Skull);
            setMotores(1023, 1023);
        } else if (cmd == "T180") {
            basic.showIcon(IconNames.Surprised);
            setMotores(1023, -1023);
            basic.pause(280);
            pararMotores();
        } else if (cmd == "ARMA_ON") {
            pins.digitalWritePin(DigitalPin.P16, 1);
            basic.showIcon(IconNames.Sword);
        } else if (cmd == "ARMA_OFF") {
            pins.digitalWritePin(DigitalPin.P16, 0);
            basic.clearScreen();
        } else if (cmd == "STOP") {
            pararMotores();
            basic.showIcon(IconNames.SmallDiamond);
        }
    }
});

// Watchdog Failsafe em Loop de Fundo (a cada 50ms)
basic.forever(function () {
    if (!failsafeAtivo && (input.runningTime() - ultimoSinal > 400)) {
        pararMotores();
        basic.showIcon(IconNames.No);
    }
    basic.pause(50);
});
