import env as env
from enum import Enum
from datetime import datetime


class SymbolEnum(Enum):
    WIN = "WIN"
    WDO = "WDO"


def getSymbol(symbolEnum: SymbolEnum):
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year % 100

    letras = ["F", "G", "H", "J", "K", "M", "N", "Q", "U", "V", "X", "Z"]
    indice_letra = mes_atual - 1

    sufix = letras[indice_letra] + str(ano_atual)

    if symbolEnum == SymbolEnum.WIN:
        return SymbolEnum.WIN + sufix
    elif symbolEnum == SymbolEnum.WDO:
        return SymbolEnum.WDO + sufix
