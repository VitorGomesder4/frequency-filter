import numpy as np

def filtrar_passa_baixa(sinal, frequencia_corte_superior, frequency_rate):
    fft_signal = np.fft.fft(sinal)
    frequencias = np.fft.fftfreq(len(sinal), 1 / frequency_rate)
    sinal_filtrado = np.fft.ifft(fft_signal * (np.abs(frequencias) <= frequencia_corte_superior)).real

    return sinal_filtrado

def filtrar_passa_alta(sinal, frequencia_corte_inferior):
    pass

def filtrar_passa_faixa(sinal, frequencia_min, frequencia_max):
    pass

def filtrar_rejeita_faixa(sinal, frequencia_min, frequencia_max):
    pass