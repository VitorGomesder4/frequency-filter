import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np

from createSinais import gerar_sinal_composto, aplicar_ruido

import filtrosFrequencias as filtros
import filtrosFrequenciaisComOrdem as filtrosOrdem

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# =========================================================
# VARIÁVEIS
# =========================================================

canvas = None


# =========================================================
# APLICAR FILTRO
# =========================================================

def aplicar_filtro(sinal):

    frequencia_rate = int(frequencia_amostragem.get())

    if ordem.get() == "None":
        filtro_ordem = None
    else:
        filtro_ordem = int(ordem.get())

    tipo_filtro = filtro.get()

    # ---------------- PASSA-BAIXA ----------------

    if tipo_filtro == "Passa-baixa":

        corte = float(frequencia_corte.get())

        if filtro_ordem is None:
            return filtros.filtrar_passa_baixa(
                sinal,
                corte,
                frequencia_rate
            )

        return filtrosOrdem.filtrar_passa_baixa(
            sinal,
            corte,
            frequencia_rate,
            filtro_ordem
        )

    # ---------------- PASSA-ALTA ----------------

    elif tipo_filtro == "Passa-alta":

        corte = float(frequencia_corte.get())

        if filtro_ordem is None:
            return filtros.filtrar_passa_alta(
                sinal,
                corte,
                frequencia_rate
            )

        return filtrosOrdem.filtrar_passa_alta(
            sinal,
            corte,
            frequencia_rate,
            filtro_ordem
        )

    # ---------------- PASSA-FAIXA ----------------

    elif tipo_filtro == "Passa-faixa":

        minimo = float(frequencia_min.get())
        maximo = float(frequencia_max.get())

        if minimo >= maximo:
            raise ValueError("A frequência mínima deve ser menor que a máxima.")

        if filtro_ordem is None:
            return filtros.filtrar_passa_faixa(
                sinal,
                minimo,
                maximo,
                frequencia_rate
            )

        return filtrosOrdem.filtrar_passa_faixa(
            sinal,
            minimo,
            maximo,
            frequencia_rate,
            filtro_ordem
        )

    # ---------------- REJEITA-FAIXA ----------------

    elif tipo_filtro == "Rejeita-faixa":

        minimo = float(frequencia_min.get())
        maximo = float(frequencia_max.get())

        if minimo >= maximo:
            raise ValueError("A frequência mínima deve ser menor que a máxima.")

        if filtro_ordem is None:
            return filtros.filtrar_rejeita_faixa(
                sinal,
                minimo,
                maximo,
                frequencia_rate
            )

        return filtrosOrdem.filtrar_rejeita_faixa(
            sinal,
            minimo,
            maximo,
            frequencia_rate,
            filtro_ordem
        )


# =========================================================
# GERAR
# =========================================================

def gerar():

    global canvas

    try:

        # ---------------------------------------------
        # Pega os valores das senoides
        # ---------------------------------------------

        frequencia1 = float(frequencia_senoide1.get())
        amplitude1 = float(amplitude_senoide1.get())

        frequencia2 = float(frequencia_senoide2.get())
        amplitude2 = float(amplitude_senoide2.get())

        # ---------------------------------------------
        # Outros parâmetros
        # ---------------------------------------------

        frequency_rate = int(frequencia_amostragem.get())
        nivel_ruido = float(ruido.get())

        # ---------------------------------------------
        # Verifica Nyquist
        # ---------------------------------------------

        maior_frequencia = max(
            frequencia1,
            frequencia2
        )

        if frequency_rate <= maior_frequencia * 2:

            messagebox.showerror(
                "Erro",
                "A frequência de amostragem deve ser maior que "
                "2 vezes a maior frequência das senoides."
            )

            return

        # ---------------------------------------------
        # Cria o tempo
        # ---------------------------------------------

        t = np.arange(
            0,
            1,
            1 / frequency_rate
        )

        # ---------------------------------------------
        # Gera sinal composto
        # (argumentos nomeados: a função espera
        #  amplitude ANTES da frequência)
        # ---------------------------------------------

        sinal_composto = gerar_sinal_composto(
            tempo=t,
            amplitude1=amplitude1,
            frequencia1=frequencia1,
            amplitude2=amplitude2,
            frequencia2=frequencia2
        )

        # ---------------------------------------------
        # Adiciona ruído
        # ---------------------------------------------

        sinal_ruido = aplicar_ruido(
            nivel_ruido,
            t,
            sinal_composto
        )

        # ---------------------------------------------
        # Aplica filtro
        # ---------------------------------------------

        sinal_filtrado = aplicar_filtro(
            sinal_ruido
        )

        # ---------------------------------------------
        # Remove gráfico anterior
        # ---------------------------------------------

        if canvas is not None:

            canvas.get_tk_widget().destroy()

        # ---------------------------------------------
        # Cria gráfico: 3 painéis empilhados,
        # com o mesmo eixo X e o mesmo eixo Y,
        # para comparar as ondas com facilidade
        # ---------------------------------------------

        figura = Figure(
            dpi=100,
            constrained_layout=True
        )

        eixo_composto, eixo_ruido, eixo_filtrado = figura.subplots(
            3,
            1,
            sharex=True,
            sharey=True
        )

        # ---- 1) Sinal composto (original) ----

        eixo_composto.plot(
            t,
            sinal_composto,
            color="black",
            label="Sinal composto"
        )

        # ---- 2) Sinal com ruído ----

        eixo_ruido.plot(
            t,
            sinal_ruido,
            color="red",
            linewidth=0.8,
            label="Sinal com ruído"
        )

        # ---- 3) Sinal filtrado (com o composto como referência) ----

        eixo_filtrado.plot(
            t,
            sinal_composto,
            color="black",
            linestyle="--",
            linewidth=1,
            label="Sinal composto (referência)"
        )

        eixo_filtrado.plot(
            t,
            sinal_filtrado,
            color="green",
            linewidth=1.8,
            label="Sinal filtrado"
        )

        for eixo in (eixo_composto, eixo_ruido, eixo_filtrado):

            eixo.set_ylabel("Amplitude")
            eixo.margins(y=0.3)  # folga para a legenda não cobrir as ondas
            eixo.legend(loc="upper right")
            eixo.grid(True)

        eixo_filtrado.set_xlabel("Tempo (s)")

        figura.suptitle(
            "Simulação de filtro de frequência"
        )

        # ---------------------------------------------
        # Coloca gráfico dentro do Tkinter
        # ---------------------------------------------

        canvas = FigureCanvasTkAgg(
            figura,
            master=area_grafico
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    except ValueError as erro:

        # Mensagens específicas (ex.: faixa inválida) são mostradas;
        # erros de conversão de número usam a mensagem padrão.
        texto = str(erro)

        if "could not convert" in texto or "invalid literal" in texto:
            texto = "Verifique se todos os valores informados são válidos."

        messagebox.showerror(
            "Erro",
            texto
        )

    except Exception as erro:

        messagebox.showerror(
            "Erro",
            str(erro)
        )


# =========================================================
# JANELA
# =========================================================

window = tk.Tk()

window.title("Simulador de Filtros")


# Linha 0: painéis de configuração | Linha 1: botão | Linha 2: gráfico
window.columnconfigure(0, weight=1)
window.rowconfigure(2, weight=1)


# =========================================================
# PAINEL DE CONFIGURAÇÕES (fica no topo)
# =========================================================

painel = tk.Frame(window)
painel.grid(row=0, column=0, pady=(10, 0))


# =========================================================
# GRUPO: SINAL
# =========================================================

grupo_sinal = ttk.LabelFrame(painel, text="Sinal", padding=10)
grupo_sinal.grid(row=0, column=0, padx=10, sticky="n")

# ---------------- SENOIDE 1 ----------------

tk.Label(grupo_sinal, text="Senoide 1").grid(
    row=0, column=0, padx=5, pady=4, sticky="w"
)

tk.Label(grupo_sinal, text="Frequência (Hz):").grid(
    row=0, column=1, padx=5, pady=4, sticky="e"
)

frequencia_senoide1 = ttk.Spinbox(
    grupo_sinal,
    from_=1,
    to=100,
    increment=1,
    width=8
)

frequencia_senoide1.grid(row=0, column=2, padx=5, pady=4)
frequencia_senoide1.set(10)

tk.Label(grupo_sinal, text="Amplitude:").grid(
    row=0, column=3, padx=5, pady=4, sticky="e"
)

amplitude_senoide1 = ttk.Spinbox(
    grupo_sinal,
    from_=0.1,
    to=100,
    increment=0.5,
    width=8
)

amplitude_senoide1.grid(row=0, column=4, padx=5, pady=4)
amplitude_senoide1.set(10)

# ---------------- SENOIDE 2 ----------------

tk.Label(grupo_sinal, text="Senoide 2").grid(
    row=1, column=0, padx=5, pady=4, sticky="w"
)

tk.Label(grupo_sinal, text="Frequência (Hz):").grid(
    row=1, column=1, padx=5, pady=4, sticky="e"
)

frequencia_senoide2 = ttk.Spinbox(
    grupo_sinal,
    from_=1,
    to=100,
    increment=1,
    width=8
)

frequencia_senoide2.grid(row=1, column=2, padx=5, pady=4)
frequencia_senoide2.set(5)

tk.Label(grupo_sinal, text="Amplitude:").grid(
    row=1, column=3, padx=5, pady=4, sticky="e"
)

amplitude_senoide2 = ttk.Spinbox(
    grupo_sinal,
    from_=0.1,
    to=100,
    increment=0.5,
    width=8
)

amplitude_senoide2.grid(row=1, column=4, padx=5, pady=4)
amplitude_senoide2.set(5)

# ---------------- AMOSTRAGEM E RUÍDO ----------------

tk.Label(grupo_sinal, text="Geral").grid(
    row=2, column=0, padx=5, pady=4, sticky="w"
)

tk.Label(grupo_sinal, text="Amostragem (Hz):").grid(
    row=2, column=1, padx=5, pady=4, sticky="e"
)

frequencia_amostragem = ttk.Spinbox(
    grupo_sinal,
    from_=100,
    to=100000,
    increment=100,
    width=8
)

frequencia_amostragem.grid(row=2, column=2, padx=5, pady=4)
frequencia_amostragem.set(1000)

tk.Label(grupo_sinal, text="Ruído:").grid(
    row=2, column=3, padx=5, pady=4, sticky="e"
)

ruido = ttk.Spinbox(
    grupo_sinal,
    from_=0,
    to=2,
    increment=0.1,
    width=8
)

ruido.grid(row=2, column=4, padx=5, pady=4)
ruido.set(0.2)


# =========================================================
# GRUPO: FILTRO
# =========================================================

grupo_filtro = ttk.LabelFrame(painel, text="Filtro", padding=10)
grupo_filtro.grid(row=0, column=1, padx=10, sticky="n")

# ---------------- TIPO ----------------

tk.Label(grupo_filtro, text="Filtro:").grid(
    row=0, column=0, padx=5, pady=4, sticky="e"
)

filtro = ttk.Combobox(
    grupo_filtro,
    values=[
        "Passa-baixa",
        "Passa-alta",
        "Passa-faixa",
        "Rejeita-faixa"
    ],
    state="readonly",
    width=15
)

filtro.grid(row=0, column=1, padx=5, pady=4, sticky="w")
filtro.set("Passa-baixa")

# ---------------- ORDEM ----------------

tk.Label(grupo_filtro, text="Ordem:").grid(
    row=1, column=0, padx=5, pady=4, sticky="e"
)

ordem = ttk.Combobox(
    grupo_filtro,
    values=[
        "None",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10"
    ],
    state="readonly",
    width=8
)

ordem.grid(row=1, column=1, padx=5, pady=4, sticky="w")
ordem.set("4")

# ---------------- CORTE (passa-baixa / passa-alta) ----------------
# Os dois blocos abaixo ocupam a MESMA posição na grade (linha 2).
# Só um aparece por vez, então a ordem do layout nunca muda.

row_corte = tk.Frame(grupo_filtro)

tk.Label(row_corte, text="Frequência de corte (Hz):").grid(
    row=0, column=0, padx=5
)

frequencia_corte = ttk.Spinbox(
    row_corte,
    from_=1,
    to=500,
    increment=1,
    width=8
)

frequencia_corte.grid(row=0, column=1, padx=5)
frequencia_corte.set(7)

# ---------------- MIN / MAX (passa-faixa / rejeita-faixa) ----------------

row_faixa = tk.Frame(grupo_filtro)

tk.Label(row_faixa, text="Frequência mínima (Hz):").grid(
    row=0, column=0, padx=5, pady=2, sticky="e"
)

frequencia_min = ttk.Spinbox(
    row_faixa,
    from_=1,
    to=500,
    increment=1,
    width=8
)

frequencia_min.grid(row=0, column=1, padx=5, pady=2)
frequencia_min.set(4)

tk.Label(row_faixa, text="Frequência máxima (Hz):").grid(
    row=1, column=0, padx=5, pady=2, sticky="e"
)

frequencia_max = ttk.Spinbox(
    row_faixa,
    from_=1,
    to=500,
    increment=1,
    width=8
)

frequencia_max.grid(row=1, column=1, padx=5, pady=2)
frequencia_max.set(7)


# =========================================================
# MUDAR CAMPOS DO FILTRO
# =========================================================

def mudar_filtro(event=None):

    row_corte.grid_remove()
    row_faixa.grid_remove()

    if filtro.get() in [
        "Passa-baixa",
        "Passa-alta"
    ]:

        row_corte.grid(row=2, column=0, columnspan=2, pady=4)

    elif filtro.get() in [
        "Passa-faixa",
        "Rejeita-faixa"
    ]:

        row_faixa.grid(row=2, column=0, columnspan=2, pady=4)


filtro.bind(
    "<<ComboboxSelected>>",
    mudar_filtro
)

mudar_filtro()


# =========================================================
# BOTÃO GERAR
# =========================================================

row_gerar = tk.Frame(window)
row_gerar.grid(row=1, column=0, pady=10)

botao_gerar = ttk.Button(
    row_gerar,
    text="Gerar",
    command=gerar
)

botao_gerar.pack()


# =========================================================
# ÁREA DO GRÁFICO (sempre no final da interface)
# =========================================================

area_grafico = tk.Frame(window)

area_grafico.grid(
    row=2,
    column=0,
    sticky="nsew",
    padx=20,
    pady=(0, 10)
)


# =========================================================
# LOOP
# =========================================================

window.mainloop()