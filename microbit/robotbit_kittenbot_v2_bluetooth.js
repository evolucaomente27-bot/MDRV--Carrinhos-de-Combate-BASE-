/**
 * =====================================================================================
 * PROJETO: ROBÔ DE COMBATE BBC MICRO:BIT V2 - SHIELD KITTENBOT ROBOT:BIT
 * Controle Direto pelo Celular (Bluetooth BLE / Web Bluetooth)
 * Hardware: BBC micro:bit V2 + Shield KittenBot Robot:bit (com Bateria 18650)
 * Extensão MakeCode: robotbit (https://github.com/KittenBot/pxt-robotbit)
 * =====================================================================================
 * 
 * COMO LIGAR OS MOTORES FISICAMENTE NA SUA PLACA (Conforme sua foto):
 *   - Na barra de pinos do canto inferior (B- B+ A- A+ VM):
 *       * Motor Esquerdo: Ligue os 2 fios nos pinos A+ e A- (Canal M1A)
 *       * Motor Direito:  Ligue os 2 fios nos pinos B+ e B- (Canal M1B)
 *       * O PINO VM FICA VAZIO! (Não conecte nada no VM para motores DC)
 * 
 * COMO GRAVAR NO MICROSOFT MAKECODE:
 *   1. Acesse: https://makecode.microbit.org e crie um "Novo Projeto".
 *   2. Clique na engrenagem ⚙️ ➔ Extensões ➔ adicione "bluetooth".
 *   3. Clique na engrenagem ⚙️ ➔ Extensões ➔ pesquise e adicione "robotbit".
 *   4. Na engrenagem ⚙️ ➔ "Configurações do Projeto" (Project Settings):
 *      Ative a opção "No Pairing Required: Anyone can connect via Bluetooth".
 *   5. Alterne para a aba "JavaScript" no topo central, cole este código e Baixe (.hex).
 * =====================================================================================
 */

let conectado = false;
let ultimoSinal = input.runningTime();

// Para todos os motores no início
robotbit.MotorStopAll();

// Inicia o serviço Bluetooth UART
bluetooth.startUartService();
basic.showIcon(IconNames.Diamond);

// Evento: Celular Conectado
bluetooth.onBluetoothConnected(function () {
    conectado = true;
    ultimoSinal = input.runningTime();
    basic.showIcon(IconNames.Happy);
    basic.pause(500);
    basic.showIcon(IconNames.SmallDiamond);
});

// Evento: Celular Desconectado
bluetooth.onBluetoothDisconnected(function () {
    conectado = false;
    robotbit.MotorStopAll();
    basic.showIcon(IconNames.Sad);
});

function pararMotores() {
    robotbit.MotorStopAll();
}

/**
 * Aciona os motores M1A (Esquerdo) e M1B (Direito)
 * velL e velR variam entre -255 (ré máxima) e +255 (frente máxima)
 */
function acionarMotores(velL: number, velR: number) {
    // Limita entre -255 e +255
    velL = Math.max(-255, Math.min(255, velL));
    velR = Math.max(-255, Math.min(255, velR));

    if (Math.abs(velL) < 25) {
        robotbit.MotorRun(robotbit.Motors.M1A, 0);
    } else {
        robotbit.MotorRun(robotbit.Motors.M1A, velL);
    }

    if (Math.abs(velR) < 25) {
        robotbit.MotorRun(robotbit.Motors.M1B, 0);
    } else {
        robotbit.MotorRun(robotbit.Motors.M1B, velR);
    }
}

// Receptor de comandos do celular via BLE
bluetooth.onUartDataReceived(serial.delimiters(Delimiters.NewLine), function () {
    let cmd = bluetooth.uartReadUntil(serial.delimiters(Delimiters.NewLine)).trim();
    if (cmd.length == 0) return;

    ultimoSinal = input.runningTime();

    // 1. Pacote do Joystick Touch 360°: "D:<velL>,<velR>"
    if (cmd.indexOf("D:") == 0) {
        let partes = cmd.substr(2).split(",");
        if (partes.length == 2) {
            let vL = parseInt(partes[0]);
            let vR = parseInt(partes[1]);

            // Se vier na escala -1023..+1023 do app, converte para escala -255..+255 do Robotbit
            if (Math.abs(vL) > 100 || Math.abs(vR) > 100) {
                vL = Math.round((vL / 1023) * 255);
                vR = Math.round((vR / 1023) * 255);
            } else {
                // Escala percentual (-100 a +100)
                vL = Math.round((vL / 100) * 255);
                vR = Math.round((vR / 100) * 255);
            }

            acionarMotores(vL, vR);

            // Animação Direcional na Matriz 5x5
            if (vL > 60 && vR > 60) {
                basic.showArrow(ArrowNames.North);
            } else if (vL < -60 && vR < -60) {
                basic.showArrow(ArrowNames.South);
            } else if (vL > 60 && vR < -60) {
                basic.showArrow(ArrowNames.East);
            } else if (vL < -60 && vR > 60) {
                basic.showArrow(ArrowNames.West);
            } else if (vL == 0 && vR == 0) {
                basic.showIcon(IconNames.SmallDiamond);
            }
        }
    }
    // 2. Comandos D-Pad Rápidos (Botões)
    else if (cmd == "F") { // Frente
        acionarMotores(220, 220);
        basic.showArrow(ArrowNames.North);
    } else if (cmd == "B") { // Ré
        acionarMotores(-220, -220);
        basic.showArrow(ArrowNames.South);
    } else if (cmd == "L") { // Giro Esquerda
        acionarMotores(-200, 200);
        basic.showArrow(ArrowNames.West);
    } else if (cmd == "R") { // Giro Direita
        acionarMotores(200, -200);
        basic.showArrow(ArrowNames.East);
    } else if (cmd == "S") { // Parar
        pararMotores();
        basic.showIcon(IconNames.SmallDiamond);
    }
    // 3. Comandos Táticos de Combate
    else if (cmd == "T" || cmd == "TURBO") { // Turbo 100%
        basic.showIcon(IconNames.Skull);
        acionarMotores(255, 255);
    } else if (cmd == "G" || cmd == "T180") { // Giro 180°
        basic.showIcon(IconNames.Surprised);
        acionarMotores(255, -255);
        basic.pause(260);
        pararMotores();
        basic.showIcon(IconNames.SmallDiamond);
    } else if (cmd == "X" || cmd == "ARMA_ON") { // Ativa Servo de Combate no S1
        robotbit.Servo(robotbit.Servos.S1, 180);
        basic.showIcon(IconNames.Sword);
    } else if (cmd == "x" || cmd == "ARMA_OFF") { // Desativa Servo no S1
        robotbit.Servo(robotbit.Servos.S1, 0);
        basic.showIcon(IconNames.SmallDiamond);
    }
});

// Watchdog Failsafe de Segurança (500ms)
basic.forever(function () {
    if (conectado && (input.runningTime() - ultimoSinal > 500)) {
        pararMotores();
        basic.showIcon(IconNames.No);
    }
    basic.pause(60);
});
