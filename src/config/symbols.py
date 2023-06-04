import env as env
from datetime import datetime
from .singleton import Singleton


class Symbols(Singleton):
    def __init__(self):
        if self._wasInstantiated is None:
            pass
        self._wasInstantiated = True

    def getReferenceLetterAndYear():
        mes_atual = datetime.now().month
        ano_atual = datetime.now().year % 100

        letras = ["F", "G", "H", "J", "K", "M", "N", "Q", "U", "V", "X", "Z"]
        indice_letra = mes_atual - 1

        return letras[indice_letra] + str(ano_atual)
