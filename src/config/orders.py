import env as env
import MetaTrader5 as mt5
from src.config.singleton import Singleton


class Orders(Singleton):
    def __init__(self):
        if self._wasInstantiated is None:
            pass

        self._wasInstantiated = True

    def openMarketBuy(self, magic):
        price = mt5.symbol_info_tick(env.symbol).ask
        point = mt5.symbol_info(env.symbol).point
        tp = price + 50 * point
        sl = price - 100 * point

        result = mt5.order_send(
            symbol=env.symbol,
            action=mt5.ORDER_ACTION_BUY,
            volume=env.volume,
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

    def openMarketSell(self, magic):
        price = mt5.symbol_info_tick(env.symbol).bid
        point = mt5.symbol_info(env.symbol).point
        tp = price - 50 * point
        sl = price + 100 * point

        result = mt5.order_send(
            symbol=env.symbol,
            action=mt5.ORDER_ACTION_SELL,
            volume=env.volume,
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

    def closeAllOrders(self):
        positions = mt5.positions_get()

        for position in positions:
            result = mt5.position_close(position)

            if result.retcode == mt5.TRADE_RETCODE_DONE:
                print(f"Posição {position.ticket} fechada com sucesso.")
            else:
                print(f"Erro ao fechar a posição {position.ticket}: {result.comment}")
