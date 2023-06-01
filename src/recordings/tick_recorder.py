import env
import time
import MetaTrader5 as mt5
from src.config.singleton import Singleton
from src.repositories.tick_repository import TickRepository
from src.trades.trade_time import TradeTime


class TickRecorder(Singleton):
    def __init__(self):
        self.tickRepository = TickRepository()
        self.tradeTime = TradeTime()

    def record1min(self):
        while self.tradeTime.isTradingTime:
            tick = mt5.symbol_info_tick(env.symbol)

            if tick is not None:
                print(tick)
                self.tickRepository.insert(tick, "ticks_win_1min")
            else:
                raise Exception(f"Não foi possível obter a cotação do {env.symbol}")

            time.sleep(60)

    def record5min(self):
        while self.tradeTime.isTradingTime:
            tick = mt5.symbol_info_tick(env.symbol)

            if tick is not None:
                self.tickRepository.insert(tick, "ticks_win_5min")
            else:
                raise Exception(f"Não foi possível obter a cotação do {env.symbol}")

            time.sleep(60 * 5)
