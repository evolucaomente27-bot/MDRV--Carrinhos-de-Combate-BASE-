# =====================================================================================
# PROJETO: ROBÔ DE COMBATE BBC MICRO:BIT - FIRMWARE DO RECEPTOR (NO ROBÔ)
# Plataforma: BBC micro:bit (V1 ou V2)
# Linguagem: MicroPython (compatível com python.microbit.org e Mu Editor)
# =====================================================================================
#
# Ligações Físicas (micro:bit ➔ Ponte H L298N ou TB6612FNG):
#   - P0  -----> IN1 da Ponte H (Motor Esquerdo Frente)
#   - P1  -----> IN2 da Ponte H (Motor Esquerdo Ré)
#   - P8  -----> IN3 da Ponte H (Motor Direito Frente)
#   - P12 -----> IN4 da Ponte H (Motor Direito Ré)
#   - P16 -----> Entrada do MOSFET/Relé da Arma (Opcional)
#   - GND -----> GND Comum unificado com a Bateria e a Ponte H
#
# Recursos do Robô:
#   * Rádio 2.4GHz nativo de ultra-baixa latência (< 2ms) sem delay de rede
#   * Failsafe de Segurança Watchdog (400ms): desliga motores se perder o sinal do rádio
#   * Controle de velocidade analógico PWM suave (0 a 1023)
#   * Animação na matriz de LEDs 5x5 indicando sentido e alertas de combate
# =====================================================================================

from microbit import *
import radio

# ==========================================
# CONFIGURAÇÕES DO RÁDIO
# ==========================================
CANAL_RADIO = 7        # Mude o canal (0 a 83) para batalhar sem interferência de outros robôs
POTENCIA_RADIO = 7     # Potência máxima de transmissão (0 a 7 -> 7 = +4dBm)

radio.on()
radio.config(group=CANAL_RADIO, power=POTENCIA_RADIO)

# ==========================================
# SEGURANÇA E FAILSAFE (WATCHDOG)
# ==========================================
TIMEOUT_FAILSAFE_MS = 400
ultimo_tempo_sinal = running_time()
failsafe_acionado = True

# Estado da arma
arma_ativa = False

# ==========================================
# FUNÇÕES DE CONTROLE DOS MOTORES (PWM 0-1023)
# ==========================================
def parar_motores():
    global failsafe_acionado
    pin0.write_analog(0)
    pin1.write_analog(0)
    pin8.write_analog(0)
    pin12.write_analog(0)
    pin0.write_digital(0)
    pin1.write_digital(0)
    pin8.write_digital(0)
    pin12.write_digital(0)
    pin16.write_digital(0)
    failsafe_acionado = True

def acionar_motores(vel_esq, vel_dir):
    """
    vel_esq e vel_dir: inteiros entre -1023 (ré máxima) e +1023 (frente máxima)
    """
    global failsafe_acionado
    failsafe_acionado = False

    # Limita valores entre -1023 e +1023
    vel_esq = max(-1023, min(1023, vel_esq))
    vel_dir = max(-1023, min(1023, vel_dir))

    # --- MOTOR ESQUERDO (P0 e P1) ---
    if vel_esq > 0:
        pin0.write_analog(vel_esq)
        pin1.write_digital(0)
    elif vel_esq < 0:
        pin0.write_digital(0)
        pin1.write_analog(abs(vel_esq))
    else:
        pin0.write_digital(0)
        pin1.write_digital(0)

    # --- MOTOR DIREITO (P8 e P12) ---
    if vel_dir > 0:
        pin8.write_analog(vel_dir)
        pin12.write_digital(0)
    elif vel_dir < 0:
        pin8.write_digital(0)
        pin12.write_analog(abs(vel_dir))
    else:
        pin8.write_digital(0)
        pin12.write_digital(0)

# ==========================================
# INICIALIZAÇÃO E ANIMAÇÃO DE BOOT
# ==========================================
parar_motores()
display.show(Image.SWORD)
sleep(500)
display.show(Image.YES)
sleep(300)
display.clear()

# ==========================================
# LOOP PRINCIPAL DO RECEPTOR
# ==========================================
while True:
    agora = running_time()
    mensagem = radio.receive()

    if mensagem:
        ultimo_tempo_sinal = agora

        # 1. Comando Analógico Contínuo: "D:<left>,<right>"
        #    Exemplo: "D:800,-400"
        if mensagem.startswith("D:"):
            try:
                dados = mensagem[2:].split(",")
                v_esq = int(dados[0])
                v_dir = int(dados[1])
                acionar_motores(v_esq, v_dir)

                # Feedback visual na matriz de LEDs
                if v_esq > 300 and v_dir > 300:
                    display.show(Image.ARROW_N)
                elif v_esq < -300 and v_dir < -300:
                    display.show(Image.ARROW_S)
                elif v_esq > 300 and v_dir < -300:
                    display.show(Image.ARROW_E)
                elif v_esq < -300 and v_dir > 300:
                    display.show(Image.ARROW_W)
                elif v_esq == 0 and v_dir == 0:
                    display.show(Image.DIAMOND_SMALL)
                else:
                    display.show(Image.HEART_SMALL)
            except:
                pass

        # 2. Comando Especial de Combate: "CMD:<tipo>"
        elif mensagem.startswith("CMD:"):
            cmd = mensagem[4:]
            if cmd == "TURBO":
                display.show(Image.SKULL)
                acionar_motores(1023, 1023)
            elif cmd == "T180":
                # Meia-volta 180° rápida
                display.show(Image.SURPRISED)
                acionar_motores(1023, -1023)
                sleep(280)
                parar_motores()
            elif cmd == "ARMA_ON":
                arma_ativa = True
                pin16.write_digital(1)
                display.show(Image.SWORD)
            elif cmd == "ARMA_OFF":
                arma_ativa = False
                pin16.write_digital(0)
                display.clear()
            elif cmd == "STOP":
                parar_motores()
                display.show(Image.DIAMOND_SMALL)

        # 3. Heartbeat / Ping de conexão
        elif mensagem == "P":
            if failsafe_acionado:
                display.show(Image.DIAMOND_SMALL)

    # ==========================================
    # MONITOR DE FAILSAFE WATCHDOG
    # ==========================================
    if not failsafe_acionado and (agora - ultimo_tempo_sinal > TIMEOUT_FAILSAFE_MS):
        parar_motores()
        display.show(Image.NO)  # Exibe 'X' alertando perda de sinal
