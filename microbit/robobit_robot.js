/**
 * =====================================================================================
 * PROJETO: ROBÔ DE COMBATE BBC MICRO:BIT - FIRMWARE RECEPTOR ROBO:BIT SHIELD
 * Plataforma: Microsoft MakeCode (makecode.microbit.org)
 * Extensão Necessária: 4tronix/Robobit
 * =====================================================================================
 * 
 * COMO USAR NO MAKECODE:
 *  1. Acesse: https://makecode.microbit.org
 *  2. Crie um "Novo Projeto" (ex: "Robo-RoboBit").
 *  3. No menu superior direito (engrenagem), clique em "Extensões" (Extensions).
 *  4. Digite "Robobit" ou a URL "https://github.com/4tronix/Robobit" e selecione a extensão da 4tronix.
 *  5. Alterne a visualização de "Blocos" para "JavaScript" no topo central.
 *  6. Cole este código completo e clique novamente em "Blocos" (se quiser editar visualmente).
 *  7. Baixe o arquivo .hex e copie para o seu BBC micro:bit conectado no shield Robo:Bit!
 * =====================================================================================
 */

// ==========================================
// INICIALIZAÇÃO DO RÁDIO E HARDWARE ROBO:BIT
// ==========================================
const CANAL_RADIO = 7;
radio.setGroup(CANAL_RADIO);
radio.setTransmitPower(7); // Potência máxima de 2.4GHz (+4dBm)

// Inicializa o shield 4tronix Robo:Bit (compatível com Mk1, Mk2 e Mk3)
robobit.select_model(RBModel.Mk3);
robobit.stop(RBStopMode.Coast);

let ultimoSinal = input.runningTime();
let failsafeAtivo = true;

// Feedback inicial na matriz 5x5
basic.showIcon(IconNames.Target);
basic.pause(300);
basic.clearScreen();

/**
 * Converte velocidade de -1023..+1023 (do controle remoto) para 0..100% no Robo:Bit
 */
function aplicarMotor(motor: RBMotor, vel: number) {
    vel = Math.max(-1023, Math.min(1023, vel));

    if (Math.abs(vel) < 30) {
        robobit.move(motor, RBDirection.Forward, 0);
    } else if (vel > 0) {
        let spd = Math.round((vel / 1023) * 100);
        robobit.move(motor, RBDirection.Forward, spd);
    } else {
        let spd = Math.round((Math.abs(vel) / 1023) * 100);
        robobit.move(motor, RBDirection.Reverse, spd);
    }
}

function pararTudo() {
    robobit.stop(RBStopMode.Coast);
    pins.digitalWritePin(DigitalPin.P16, 0); // Desliga arma
    failsafeAtivo = true;
}

// ==========================================
// RECEPTOR DE PACOTES DE RÁDIO 2.4GHz
// ==========================================
radio.onReceivedString(function (recebido: string) {
    ultimoSinal = input.runningTime();
    failsafeAtivo = false;

    // 1. Comando de Movimentação Contínua: "D:<velL>,<velR>"
    if (recebido.indexOf("D:") == 0) {
        let dados = recebido.substr(2).split(",");
        if (dados.length == 2) {
            let velL = parseInt(dados[0]);
            let velR = parseInt(dados[1]);

            // Aplica motores esquerdo e direito individualmente
            aplicarMotor(RBMotor.Left, velL);
            aplicarMotor(RBMotor.Right, velR);

            // Animação Direcional na Matriz de LEDs 5x5
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
    // 2. Comandos Especiais e Táticos: "CMD:<tipo>"
    else if (recebido.indexOf("CMD:") == 0) {
        let cmd = recebido.substr(4);

        if (cmd == "TURBO") {
            // Empurrão de Força Total 100%
            basic.showIcon(IconNames.Skull);
            robobit.move(RBMotor.Both, RBDirection.Forward, 100);
        }
        else if (cmd == "T180") {
            // Giro Tático Rápido de 180 Graus
            basic.showIcon(IconNames.Surprised);
            robobit.rotate(RBRobotDirection.Right, 100);
            basic.pause(260); // Tempo calibrado para meia volta com pneus Robo:Bit
            robobit.stop(RBStopMode.Brake);
            basic.clearScreen();
        }
        else if (cmd == "ARMA_ON") {
            // Ativa MOSFET / Saída de Combate no Pino 16
            pins.digitalWritePin(DigitalPin.P16, 1);
            basic.showIcon(IconNames.Sword);
        }
        else if (cmd == "ARMA_OFF") {
            // Desativa Saída de Combate
            pins.digitalWritePin(DigitalPin.P16, 0);
            basic.clearScreen();
        }
        else if (cmd == "STOP") {
            pararTudo();
            basic.showIcon(IconNames.SmallDiamond);
        }
    }
});

// ==========================================
// WATCHDOG FAILSAFE DE SEGURANÇA (400ms)
// ==========================================
// Se o controle perder sinal por mais de 400ms, o robô para imediatamente!
basic.forever(function () {
    if (!failsafeAtivo && (input.runningTime() - ultimoSinal > 400)) {
        pararTudo();
        basic.showIcon(IconNames.No);
    }
    basic.pause(50);
});
