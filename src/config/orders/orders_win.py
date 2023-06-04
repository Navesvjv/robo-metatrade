import env as env
import MetaTrader5 as mt5
from src.config.singleton import Singleton


class OrdersWIN(Singleton):
    def __init__(self, symbol):
        if self._wasInstantiated is None:
            self.symbol = symbol

        self._wasInstantiated = True

    def openMarketBuy(self, magic, symbol):
        price = mt5.symbol_info_tick(self.symbol).ask
        point = mt5.symbol_info(self.symbol).point
        tp = price + 50 * point
        sl = price - 100 * point

        result = mt5.order_send(
            symbol=symbol,
            action=mt5.ORDER_ACTION_BUY,
            volume=env.volume_win,
            type=mt5.ORDER_TYPE_MARKET,
            price=0,
            tp=tp,
            sl=sl,
            magic=magic,
        )

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Error opening order: {result.comment} ❌")
        else:
            print("Order MarketBuy opened successfully! ✅")

    def openMarketSell(self, magic, symbol):
        price = mt5.symbol_info_tick(self.symbol).bid
        point = mt5.symbol_info(self.symbol).point
        tp = price - 50 * point
        sl = price + 100 * point

        result = mt5.order_send(
            symbol=symbol,
            action=mt5.ORDER_ACTION_SELL,
            volume=env.volume_win,
            type=mt5.ORDER_TYPE_MARKET,
            price=0,
            tp=tp,
            sl=sl,
            magic=magic,
        )

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Error opening order: {result.comment} ❌")
        else:
            print("Order MarketSell opened successfully! ✅")
