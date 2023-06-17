import MetaTrader5 as mt5
from src.symbol import getSymbol
from src.db import DbConnection


class CopyRates:
    def __init__(self):
        self.dbConnection = DbConnection()

    def get(self):
        num_bars = 5000
        timeframe = mt5.TIMEFRAME_H1
        symbol = getSymbol()

        if not mt5.symbol_select(symbol):
            print(f"Failed to select {symbol}, error code = {mt5.last_error()}")

        return mt5.copy_rates_from_pos(symbol, timeframe, 0, num_bars)

        # for i in dataset:
        #     self.dbConnection.execQuery(
        #         f"""
        #             insert into win_h1 (time, open, high, low, close, tick_volume, spread, real_volume)
        #             values ({i[0]}, {i[1]}, {i[2]}, {i[3]}, {i[4]}, {i[5]}, {i[6]}, {i[7]})
        #         """
        #     )
