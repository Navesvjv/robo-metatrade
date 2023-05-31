import env as env
import MetaTrader5 as mt5
from config.singleton import Singleton


class Orders(Singleton):
    def openMarketBuy(self):
        result = mt5.order_send(
            symbol=env.symbol,
            action=mt5.ORDER_ACTION_BUY,
            volume=env.volume,
            type=mt5.ORDER_TYPE_MARKET,
            price=0,
        )

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Error opening order: {result.comment} ❌")
        else:
            print("Order MarketBuy opened successfully! ✅")

    def openMarketSell(self):
        result = mt5.order_send(
            symbol=env.symbol,
            action=mt5.ORDER_ACTION_SELL,
            volume=env.volume,
            type=mt5.ORDER_TYPE_MARKET,
            price=0,
        )

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Error opening order: {result.comment} ❌")
        else:
            print("Order MarketSell opened successfully! ✅")
