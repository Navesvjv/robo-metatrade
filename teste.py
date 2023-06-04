from datetime import datetime


def obter_letra_referencia():
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year % 100

    letras = ["F", "G", "H", "J", "K", "M", "N", "Q", "U", "V", "X", "Z"]
    indice_letra = mes_atual - 1

    return letras[indice_letra] + str(ano_atual)


# Exemplo de uso da função
letra_referencia = obter_letra_referencia()
print(letra_referencia)
