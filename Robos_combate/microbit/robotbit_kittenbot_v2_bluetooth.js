/**
 * =====================================================================================
 * PROJETO: ROBÔ DE COMBATE BBC MICRO:BIT V2 - SHIELD KITTENBOT ROBOT:BIT (M1 + M2 FIX)
 * Controle Direto pelo Celular (Bluetooth BLE / Web Bluetooth)
 * Hardware: BBC micro:bit V2 + Shield KittenBot Robot:bit
 * 
 * LIGAÇÃO FÍSICA:
 *   - Motor Esquerdo: Conectado no LADO M1 (Bloco inferior)
 *   - Motor Direito:  Conectado no LADO M2 (Bloco superior)
 * =====================================================================================
 */

let conectado = false
let ultimoSinal = input.runningTime()
let ultimoEstadoExibido = -1

// Para todos os motores no início
robotbit.MotorStopAll()

// Inicia o serviço Bluetooth UART
bluetooth.startUartService()
basic.showIcon(IconNames.Diamond)

// Evento: Celular Conectado
bluetooth.onBluetoothConnected(function () {
    conectado = true
    ultimoSinal = input.runningTime()
    basic.showIcon(IconNames.Happy)
    ultimoEstadoExibido = 100
})

// Evento: Celular Desconectado
bluetooth.onBluetoothDisconnected(function () {
    conectado = false
    robotbit.MotorStopAll()
    basic.showIcon(IconNames.Sad)
    ultimoEstadoExibido = 101
})

function pararMotores() {
    robotbit.MotorStopAll()
}

/**
 * ACIONA OS MOTORES DOS DOIS LADOS (M1 E M2):
 * - velL vai para o lado M1 (Motor Esquerdo)
 * - velR vai para o lado M2 (Motor Direito)
 * Aciona tanto canal A quanto canal B para garantir que funcione em qualquer par de pinos!
 */
function acionarMotores(velL: number, velR: number) {
    velL = Math.max(-255, Math.min(255, velL))
    velR = Math.max(-255, Math.min(255, velR))

    // === LADO M1: MOTOR ESQUERDO ===
    if (Math.abs(velL) < 25) {
        robotbit.MotorRun(robotbit.Motors.M1A, 0)
        robotbit.MotorRun(robotbit.Motors.M1B, 0)
    } else {
        robotbit.MotorRun(robotbit.Motors.M1A, velL)
        robotbit.MotorRun(robotbit.Motors.M1B, velL)
    }

    // === LADO M2: MOTOR DIREITO ===
    if (Math.abs(velR) < 25) {
        robotbit.MotorRun(robotbit.Motors.M2A, 0)
        robotbit.MotorRun(robotbit.Motors.M2B, 0)
    } else {
        robotbit.MotorRun(robotbit.Motors.M2A, velR)
        robotbit.MotorRun(robotbit.Motors.M2B, velR)
    }
}

/**
 * FILTRO ANTI-TRAVAMENTO:
 * Só atualiza a tela quando o sentido mudar para não travar os motores.
 */
function atualizarDisplay(novoEstado: number) {
    if (novoEstado == ultimoEstadoExibido) return
    ultimoEstadoExibido = novoEstado

    if (novoEstado == 1) basic.showArrow(ArrowNames.North)
    else if (novoEstado == 2) basic.showArrow(ArrowNames.South)
    else if (novoEstado == 3) basic.showArrow(ArrowNames.East)
    else if (novoEstado == 4) basic.showArrow(ArrowNames.West)
    else if (novoEstado == 0) basic.showIcon(IconNames.SmallDiamond)
    else if (novoEstado == 5) basic.showIcon(IconNames.Skull)
    else if (novoEstado == 6) basic.showIcon(IconNames.Surprised)
    else if (novoEstado == 7) basic.showIcon(IconNames.No)
}

// Receptor de comandos do celular via BLE
bluetooth.onUartDataReceived(serial.delimiters(Delimiters.NewLine), function () {
    let cmd = bluetooth.uartReadUntil(serial.delimiters(Delimiters.NewLine)).trim()
    if (cmd.length == 0) return

    ultimoSinal = input.runningTime()

    // 1. Pacote do Joystick Touch 360°: "D:<velL>,<velR>"
    if (cmd.indexOf("D:") == 0) {
        let partes = cmd.substr(2).split(",")
        if (partes.length == 2) {
            let vL = parseInt(partes[0])
            let vR = parseInt(partes[1])

            if (Math.abs(vL) > 100 || Math.abs(vR) > 100) {
                vL = Math.round((vL / 1023) * 255)
                vR = Math.round((vR / 1023) * 255)
            } else {
                vL = Math.round((vL / 100) * 255)
                vR = Math.round((vR / 100) * 255)
            }

            acionarMotores(vL, vR)

            if (vL > 60 && vR > 60) {
                atualizarDisplay(1) // Frente
            } else if (vL < -60 && vR < -60) {
                atualizarDisplay(2) // Ré
            } else if (vL > 60 && vR < -60) {
                atualizarDisplay(3) // Giro Horário
            } else if (vL < -60 && vR > 60) {
                atualizarDisplay(4) // Giro Anti-horário
            } else if (vL == 0 && vR == 0) {
                atualizarDisplay(0) // Parado
            }
        }
    }
    // 2. Comandos D-Pad Rápidos
    else if (cmd == "F") {
        acionarMotores(220, 220)
        atualizarDisplay(1)
    } else if (cmd == "B") {
        acionarMotores(-220, -220)
        atualizarDisplay(2)
    } else if (cmd == "L") {
        acionarMotores(-200, 200)
        atualizarDisplay(4)
    } else if (cmd == "R") {
        acionarMotores(200, -200)
        atualizarDisplay(3)
    } else if (cmd == "S") {
        pararMotores()
        atualizarDisplay(0)
    }
    // 3. Comandos Táticos
    else if (cmd == "T" || cmd == "TURBO") {
        acionarMotores(255, 255)
        atualizarDisplay(5)
    } else if (cmd == "G" || cmd == "T180") {
        atualizarDisplay(6)
        acionarMotores(255, -255)
        basic.pause(260)
        pararMotores()
        atualizarDisplay(0)
    } else if (cmd == "X" || cmd == "ARMA_ON") {
        robotbit.Servo(robotbit.Servos.S1, 180)
    } else if (cmd == "x" || cmd == "ARMA_OFF") {
        robotbit.Servo(robotbit.Servos.S1, 0)
    }
})

// Watchdog Failsafe Calibrado (1200ms)
basic.forever(function () {
    if (conectado && (input.runningTime() - ultimoSinal > 1200)) {
        pararMotores()
        atualizarDisplay(7)
    }
    basic.pause(80)
})
