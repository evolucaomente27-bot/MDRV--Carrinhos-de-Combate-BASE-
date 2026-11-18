# =====================================================================================
# PROJETO: ROBÔ DE COMBATE BBC MICRO:BIT - CONTROLE REMOTO TRANSMISSOR (NA MÃO)
# Plataforma: BBC micro:bit (V1 ou V2)
# Linguagem: MicroPython (compatível com python.microbit.org e Mu Editor)
# =====================================================================================
#
# Como Funciona a Pilotagem:
#   * INCLINAÇÃO (ACELERÔMETRO 3D):
#     - Incline o micro:bit para FRENTE ➔ Robô acelera proporcionalmente
#     - Incline para TRÁS ➔ Robô dá ré
#     - Incline para ESQUERDA/DIREITA ➔ Curvas dinâmicas e giros no próprio eixo
#     - Deixe na HORIZONTAL (reto) ➔ Robô freia e para imediatamente
#
#   * BOTÕES TÁTICOS DE COMBATE:
#     - [ BOTÃO A ]: TURBO 100% (PWM 1023) para investida de choque e abalroamento!
#     - [ BOTÃO B ]: Meia-volta rápida de 180° para fuga ou contra-ataque.
#     - [ BOTÃO A + B ]: Dispara a Arma / Atuador de Combate (P16).
# =====================================================================================

from microbit import *
import radio

# ==========================================
# CONFIGURAÇÕES DO RÁDIO
# ==========================================
CANAL_RADIO = 7        # DEVE SER O MESMO CANAL CONFIGURADO NO ROBÔ!
POTENCIA_RADIO = 7     # Potência máxima (+4dBm)

radio.on()
radio.config(group=CANAL_RADIO, power=POTENCIA_RADIO)

display.show(Image.TARGET)
sleep(500)
display.clear()

# ==========================================
# CALIBRAÇÃO E PARÂMETROS DE CONTROLE
# ==========================================
ZONA_MORTA = 120       # Leitura neutra para evitar trepidação da mão (-120 a +120)
MAX_INCLINACAO = 650   # Inclinação máxima para atingir 100% de PWM
TAXA_ENVIO_MS = 25     # Intervalo de envio (25ms = 40 atualizações por segundo)

arma_disparada = False

while True:
    inicio_ciclo = running_time()

    # Leitura dos botões físicos
    btn_a = button_a.is_pressed()
    btn_b = button_b.is_pressed()

    # 1. COMBO A + B: DISPARO DA ARMA
    if btn_a and btn_b:
        radio.send("CMD:ARMA_ON")
        display.show(Image.SWORD)
        arma_disparada = True
        sleep(50)
        continue
    elif arma_disparada and not (btn_a or btn_b):
        radio.send("CMD:ARMA_OFF")
        arma_disparada = False

    # 2. BOTÃO A: MODO TURBO 100% INSTANTÂNEO
    if btn_a:
        radio.send("CMD:TURBO")
        display.show(Image.SKULL)
        sleep(TAXA_ENVIO_MS)
        continue

    # 3. BOTÃO B: MEIA-VOLTA 180° TÁTICA
    if button_b.was_pressed():
        radio.send("CMD:T180")
        display.show(Image.SURPRISED)
        sleep(300)
        display.clear()
        continue

    # 4. LEITURA DO ACELERÔMETRO (PILOTAGEM POR INCLINAÇÃO)
    # y: Pitch (frente/ré) -> inclinar para frente dá valor positivo em Y
    # x: Roll (esquerda/direita) -> inclinar para direita dá valor positivo em X
    pitch = accelerometer.get_y()
    roll = accelerometer.get_x()

    # Aplicação de Zona Morta (Deadzone)
    if abs(pitch) < ZONA_MORTA:
        pitch = 0
    if abs(roll) < ZONA_MORTA:
        roll = 0

    if pitch == 0 and roll == 0:
        # Robô em repouso
        v_esq = 0
        v_dir = 0
        radio.send("D:0,0")
        
        # Ponto central na matriz 5x5
        display.clear()
        display.set_pixel(2, 2, 9)
    else:
        # Normalização dos valores (-1.0 a +1.0)
        norm_v = pitch / MAX_INCLINACAO  # Aceleração/Ré
        norm_w = roll / MAX_INCLINACAO   # Direção/Curva

        norm_v = max(-1.0, min(1.0, norm_v))
        norm_w = max(-1.0, min(1.0, norm_w))

        # Algoritmo Arcade Drive Mixing (Tração Diferencial)
        left = norm_v + norm_w
        right = norm_v - norm_w

        # Normalização para não estourar a proporção
        maior = max(abs(left), abs(right))
        if maior > 1.0:
            left /= maior
            right /= maior

        # Escala para a resolução PWM do micro:bit (0 a 1023)
        v_esq = int(left * 1023)
        v_dir = int(right * 1023)

        # Envia pacote de rádio ultracompacto: "D:<left>,<right>"
        radio.send("D:{},{}".format(v_esq, v_dir))

        # Desenha a "bolha de nível" na matriz de LEDs (mostra onde está o joystick)
        px = max(0, min(4, int(2 + (norm_w * 2))))
        py = max(0, min(4, int(2 + (norm_v * 2))))
        display.clear()
        display.set_pixel(px, py, 9)

    # Mantém taxa fixa de 25ms para latência mínima e estável
    tempo_gasto = running_time() - inicio_ciclo
    if tempo_gasto < TAXA_ENVIO_MS:
        sleep(TAXA_ENVIO_MS - tempo_gasto)
