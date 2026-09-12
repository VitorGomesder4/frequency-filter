import numpy as np

def gerar_senoide(amplitude, frequencia, tempo):
    return amplitude * np.sin(2 * np.pi * frequencia * tempo)