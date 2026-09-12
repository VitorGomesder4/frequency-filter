import tkinter as tk
import numpy as np
from createSinais import gerar_sinal_composto, aplicar_ruido

window = tk.Tk()

largura = window.winfo_screenwidth() / 2
altura = window.winfo_screenheight() / 2

frequency_sample = 1000
t = np.arange(0, 1, 1/frequency_sample)

sinal_composto = gerar_sinal_composto(t, 10, 10, 5, 5)

sinal_composto_ruido = aplicar_ruido(0.2, t, sinal_composto)

print(sinal_composto[0:10])
print(sinal_composto_ruido[0:10])

window.config(height=altura, width=largura)
window.state("zoomed")