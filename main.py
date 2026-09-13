import tkinter as tk
import numpy as np
from createSinais import gerar_sinal_composto, aplicar_ruido
from filtrosFrequencias import filtrar_passa_baixa
import matplotlib.pyplot as plt 

window = tk.Tk()

largura = window.winfo_screenwidth() / 2
altura = window.winfo_screenheight() / 2

frequency_sample = 1000
t = np.arange(0, 1, 1/frequency_sample)

sinal_composto = gerar_sinal_composto(t, 10, 10, 5, 5)

sinal_composto_ruido = aplicar_ruido(0.2, t, sinal_composto)

window.config(height=altura, width=largura)
window.state("zoomed")

sinal_filtrado = filtrar_passa_baixa(sinal_composto_ruido, 7, frequency_sample)
print(sinal_composto[0:10])
print(sinal_composto_ruido[0:10])
print(sinal_filtrado[0:10])


plt.figure(figsize=(10, 8))

plt.subplot(3, 1, 1)
plt.plot(t, sinal_composto)
plt.title("Sinal original")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.grid()

plt.subplot(3, 1, 2)
plt.plot(t, sinal_composto_ruido)
plt.title("Sinal com ruído")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.grid()

plt.subplot(3, 1, 3)
plt.plot(t, sinal_filtrado)
plt.title("Sinal filtrado")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.grid()

plt.tight_layout()
plt.show()