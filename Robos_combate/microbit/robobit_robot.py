# =====================================================================================
# PROJETO: ROBÔ DE COMBATE BBC MICRO:BIT - FIRMWARE RECEPTOR ROBO:BIT SHIELD
# Plataforma: BBC micro:bit (V1 ou V2)
# Linguagem: MicroPython (compatível com python.microbit.org, Mu Editor e Thonny)
# Shield de Motores: 4tronix Robo:Bit (Mk1, Mk2 ou Mk3)
# =====================================================================================
#
# MAPEAMENTO DE HARDWARE DO ROBO:BIT SHIELD:
#   * Motor Esquerdo:
#       - P0: Velocidade / PWM (0 a 1023)
#       - P8: Sentido / Direção (0 = Frente, 1 = Ré)
#   * Motor Direito:
#       - P1: Velocidade / PWM (0 a 1023)
#       - P12: Sentido / Direção (0 = Frente, 1 = Ré)
#   * Alimentação: 4x Pilhas AA (6V) ou Bateria LiPo 2S (7.4V) no conector do shield
#   * Arma / Acessório: Pino 16 (P16 - Saída Digital para MOSFET ou Relé)
#
# PROTOCOLO DE RÁDIO 2.4GHz:
#   * Canal: Grupo 7
#   * Pacotes:
#       - "D:<velL>,<velR>" : Controle analógico contínuo (-1023 a +1023)
#       - "CMD:TURBO"       : Arrancada frontal 100% de torque
#       - "CMD:T180"        : Giro tático de 180 graus
#       - "CMD:ARMA_ON/OFF" : Ativa/desativa atuador de combate
#       - "CMD:STOP"        : Parada total de emergência
#   * Failsafe Watchdog: Para os motores se o sinal sumir por mais de 400ms!
# =====================================================================================

from microbit import *
import radio

# ==========================================
# CONFIGURAÇÕES DO RÁDIO
# ==========================================
CANAL_RADIO = 7        # Mesmo canal configurado no transmissor
POTENCIA_RADIO = 7     # Potência máxima (+4dBm)

radio.on()
radio.config(group=CANAL_RADIO, power=POTENCIA_RADIO)

# ==========================================
# CLASSE DRIVER DO 4TRONIX ROBO:BIT
# ==========================================
class RoboBitShield:
    def __init__(self):
        # Configura os períodos de PWM para 50Hz (20ms) nos pinos analógicos
        try:
            pin0.set_analog_period(20)
            pin1.set_analog_period(20)
        except Exception:
            pass
        self.stop()

    def set_left(self, speed):
        """
        speed: inteiro entre -1023 (ré máxima) e +1023 (frente máxima)
        """
        speed = max(-1023, min(1023, speed))
        if abs(speed) < 30:
            pin8.write_digital(0)
            pin0.write_analog(0)
        elif speed > 0:
            pin8.write_digital(0)
            pin0.write_analog(speed)
        else:
            pin8.write_digital(1)
            pin0.write_analog(1023 - abs(speed))

    def set_right(self, speed):
        """
        speed: inteiro entre -1023 (ré máxima) e +1023 (frente máxima)
        """
        speed = max(-1023, min(1023, speed))
        if abs(speed) < 30:
            pin12.write_digital(0)
            pin1.write_analog(0)
        elif speed > 0:
            pin12.write_digital(0)
            pin1.write_analog(speed)
        else:
            pin12.write_digital(1)
            pin1.write_analog(1023 - abs(speed))

    def drive(self, left, right):
        self.set_left(left)
        self.set_right(right)

    def spin_180(self):
        # Rotação sobre o próprio eixo
        self.set_left(1023)
        self.set_right(-1023)
        sleep(260) # Tempo calibrado para 180°
        self.stop()

    def stop(self):
        pin8.write_digital(0)
        pin0.write_analog(0)
        pin12.write_digital(0)
        pin1.write_analog(0)

# Inicializa o hardware do robô
robot = RoboBitShield()
arma_ativa = False
pin16.write_digital(0)

# ==========================================
# FAILSAFE WATCHDOG DE SEGURANÇA
# ==========================================
TIMEOUT_FAILSAFE_MS = 400
ultimo_tempo_sinal = running_time()
failsafe_acionado = True

# Feedback visual de inicialização
display.show(Image.TARGET)
sleep(300)
display.clear()

# ==========================================
# LOOP PRINCIPAL DE CONTROLE
# ==========================================
while True:
    msg = radio.receive()

    if msg is not None:
        ultimo_tempo_sinal = running_time()
        failsafe_acionado = False

        # 1. Movimentação Contínua: "D:<velL>,<velR>"
        if msg.startswith("D:"):
            try:
                partes = msg[2:].split(",")
                if len(partes) == 2:
                    vel_l = int(partes[0])
                    vel_r = int(partes[1])
                    robot.drive(vel_l, vel_r)

                    # Ícone direcional
                    if vel_l > 300 and vel_r > 300:
                        display.show(Image.ARROW_N)
                    elif vel_l < -300 and vel_r < -300:
                        display.show(Image.ARROW_S)
                    elif vel_l > 300 and vel_r < -300:
                        display.show(Image.ARROW_E)
                    elif vel_l < -300 and vel_r > 300:
                        display.show(Image.ARROW_W)
                    elif vel_l == 0 and vel_r == 0:
                        display.show(Image.DIAMOND_SMALL)
            except ValueError:
                pass

        # 2. Comandos Táticos: "CMD:<tipo>"
        elif msg.startswith("CMD:"):
            cmd = msg[4:]

            if cmd == "TURBO":
                display.show(Image.SKULL)
                robot.drive(1023, 1023)

            elif cmd == "T180":
                display.show(Image.SURPRISED)
                robot.spin_180()
                display.clear()

            elif cmd == "ARMA_ON":
                pin16.write_digital(1)
                arma_ativa = True
                display.show(Image.SWORD)

            elif cmd == "ARMA_OFF":
                pin16.write_digital(0)
                arma_ativa = False
                display.clear()

            elif cmd == "STOP":
                robot.stop()
                display.show(Image.DIAMOND_SMALL)

    # 3. Verificação do Watchdog de Sinal (Failsafe)
    agora = running_time()
    if not failsafe_acionado and (agora - ultimo_tempo_sinal > TIMEOUT_FAILSAFE_MS):
        robot.stop()
        pin16.write_digital(0) # Desliga arma por segurança
        failsafe_acionado = True
        display.show(Image.NO)

    sleep(10)
