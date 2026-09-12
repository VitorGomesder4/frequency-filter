import tkinter as tk
import numpy as np
from gerarSenoide import gerar_senoide

window = tk.Tk()

largura = window.winfo_screenwidth() / 2
altura = window.winfo_screenheight() / 2

window.config(height=altura, width=largura)
window.state("zoomed")


#window.mainloop()

frequency_sample = 5000

t = np.arange(0, 1, 1/frequency_sample)

senoide1 = gerar_senoide(amplitude=1, frequencia=10, tempo=t)

senoide2 = gerar_senoide(amplitude=0.5, frequencia=5, tempo=t)

onda_composta = senoide1 + senoide2

ruido = 0.2 * np.random.normal(0, 1, len(t))

sinal_composto_ruido = onda_composta + ruido

print(sinal_composto_ruido)