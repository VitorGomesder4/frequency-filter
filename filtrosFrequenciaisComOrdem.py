from scipy.signal import butter, filtfilt


def filtrar_passa_baixa(sinal, frequencia_corte, frequency_rate, ordem):
    b, a = butter(
        ordem,
        frequencia_corte,
        btype="lowpass",
        fs=frequency_rate
    )

    sinal_filtrado = filtfilt(b, a, sinal)

    return sinal_filtrado


def filtrar_passa_alta(sinal, frequencia_corte, frequency_rate, ordem):
    b, a = butter(
        ordem,
        frequencia_corte,
        btype="highpass",
        fs=frequency_rate
    )

    sinal_filtrado = filtfilt(b, a, sinal)

    return sinal_filtrado


def filtrar_passa_faixa(sinal, frequencia_min, frequencia_max, frequency_rate, ordem):
    b, a = butter(
        ordem,
        [frequencia_min, frequencia_max],
        btype="bandpass",
        fs=frequency_rate
    )

    sinal_filtrado = filtfilt(b, a, sinal)

    return sinal_filtrado


def filtrar_rejeita_faixa(sinal, frequencia_min, frequencia_max, frequency_rate, ordem):
    b, a = butter(
        ordem,
        [frequencia_min, frequencia_max],
        btype="bandstop",
        fs=frequency_rate
    )

    sinal_filtrado = filtfilt(b, a, sinal)

    return sinal_filtrado