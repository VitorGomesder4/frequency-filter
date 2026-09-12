import numpy as np

def gerar_senoide(amplitude, frequencia, tempo):
    return amplitude * np.sin(2 * np.pi * frequencia * tempo)

def gerar_sinal_composto(tempo, amplitude1, frequencia1, amplitude2 = 0, frequencia2 = 0):

    senoide1 = gerar_senoide(amplitude=amplitude1, frequencia=frequencia1, tempo=tempo)

    if amplitude2 != 0 and frequencia2 != 0:
        senoide2 = gerar_senoide(amplitude=amplitude2, frequencia=frequencia2, tempo=tempo)
        return senoide1 + senoide2

    return senoide1

def aplicar_ruido(intensidade, tempo, sinal):
    ruido = intensidade * np.random.normal(0, 1, len(tempo))

    return sinal + ruido