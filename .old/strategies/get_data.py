import MetaTrader5 as mt5
from datetime import datetime
from src.config.symbols import SymbolEnum, getSymbol


def getDataWIN():
    timeframe = mt5.TIMEFRAME_D1
    num_bars = 100
    bars = mt5.copy_rates_from_pos(getSymbol(SymbolEnum.WIN), timeframe, 0, num_bars)

    # Converter os timestamps para objetos datetime
    timestamps = [datetime.fromtimestamp(bar[0]) for bar in bars]
