import env as env
from enum import Enum
from datetime import datetime


def getSymbol():
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year % 100

    letras = ["F", "G", "H", "J", "K", "M", "N", "Q", "U", "V", "X", "Z"]
    indice_letra = mes_atual - 1

    sufix = letras[indice_letra] + str(ano_atual)

    return "WIN" + "Q" + "23"
