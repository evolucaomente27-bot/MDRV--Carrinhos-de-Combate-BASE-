/**
 * =====================================================================================
 * PROJETO: ROBÔ DE COMBATE BBC MICRO:BIT - CONTROLE REMOTO TRANSMISSOR (NA MÃO)
 * Plataforma: Microsoft MakeCode (makecode.microbit.org)
 * Modo: JavaScript / Blocos / Python
 * =====================================================================================
 * 
 * Como usar:
 *  1. Acesse https://makecode.microbit.org
 *  2. Crie um "Novo Projeto" chamado "Controle-Robo".
 *  3. Alterne a visualização para "JavaScript" e cole este código.
 *  4. Clique em "Baixar" para gravar no micro:bit que ficará na sua mão como Joystick!
 */

const CANAL_RADIO = 7;
radio.setGroup(CANAL_RADIO);
radio.setTransmitPower(7);

basic.showIcon(IconNames.Target);
basic.pause(500);
basic.clearScreen();

const ZONA_MORTA = 12;      // Graus de inclinação neutra
const MAX_ANGULO = 50;      // Inclinação máxima para atingir 100% de PWM

let armaAtiva = false;

basic.forever(function () {
    let btnA = input.buttonIsPressed(Button.A);
    let btnB = input.buttonIsPressed(Button.B);

    // 1. Combo A + B: Arma de Combate
    if (btnA && btnB) {
        radio.sendString("CMD:ARMA_ON");
        basic.showIcon(IconNames.Sword);
        armaAtiva = true;
        basic.pause(40);
        return;
    } else if (armaAtiva && !btnA && !btnB) {
        radio.sendString("CMD:ARMA_OFF");
        armaAtiva = false;
    }

    // 2. Botão A: Turbo 100%
    if (btnA) {
        radio.sendString("CMD:TURBO");
        basic.showIcon(IconNames.Skull);
        basic.pause(30);
        return;
    }

    // 3. Botão B: Manobra 180°
    if (btnB) {
        radio.sendString("CMD:T180");
        basic.showIcon(IconNames.Surprised);
        basic.pause(300);
        basic.clearScreen();
        return;
    }

    // 4. Pilotagem por Acelerômetro (Inclinação)
    let pitch = input.rotation(Rotation.Pitch); // Frente / Ré (-90 a +90)
    let roll = input.rotation(Rotation.Roll);   // Esquerda / Direita (-90 a +90)

    if (Math.abs(pitch) < ZONA_MORTA) pitch = 0;
    if (Math.abs(roll) < ZONA_MORTA) roll = 0;

    if (pitch == 0 && roll == 0) {
        radio.sendString("D:0,0");
        basic.clearScreen();
        led.plot(2, 2);
    } else {
        let normV = pitch / MAX_ANGULO;
        let normW = roll / MAX_ANGULO;

        normV = Math.max(-1.0, Math.min(1.0, normV));
        normW = Math.max(-1.0, Math.min(1.0, normW));

        // Arcade Drive Mixing
        let left = normV + normW;
        let right = normV - normW;

        let maior = Math.max(Math.abs(left), Math.abs(right));
        if (maior > 1.0) {
            left /= maior;
            right /= maior;
        }

        let velL = Math.round(left * 1023);
        let velR = Math.round(right * 1023);

        radio.sendString("D:" + velL + "," + velR);

        // Feedback visual na matriz 5x5
        let px = Math.max(0, Math.min(4, Math.round(2 + (normW * 2))));
        let py = Math.max(0, Math.min(4, Math.round(2 + (normV * 2))));
        basic.clearScreen();
        led.plot(px, py);
    }

    basic.pause(25);
});
