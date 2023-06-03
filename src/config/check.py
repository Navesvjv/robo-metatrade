import env
from datetime import datetime
import MetaTrader5 as mt5
from src.config.singleton import Singleton
from src.config.orders import Orders


class Checks(Singleton):
    def __init__(self):
        self.orders = Orders()

    def canOperate(self):
        if self.isCloseOrdersTime:
            if self.existsOpenOrder():
                self.orders.closeAllOrders()
            return False

        elif self.isTradingTime():
            return True
        else:
            return False

    def isTradingTime(self) -> bool:
        current_time = datetime.now().time()
        start_time = datetime.strptime(env.start_trading_time, "%H:%M").time()
        end_time = datetime.strptime(env.stop_trading_time, "%H:%M").time()

        if start_time <= current_time <= end_time:
            print("Hora de operar!")
            return True
        else:
            print("Não é hora de operar! ❌")
            return False

    def isCloseOrdersTime(self) -> bool:
        current_time = datetime.now().time()
        start_time = datetime.strptime(env.stop_trading_time, "%H:%M").time()
        end_time = datetime.strptime(env.close_orders_time, "%H:%M").time()

        if start_time <= current_time <= end_time:
            print("Hora de fechar orderns! ⚠️")
            return True
        else:
            print("Não é hora de fechar ordens!")
            return False

    def existsOpenOrder(self):
        orders = mt5.orders_get()
        if orders:
            print("Existe ordem em aberto!")
            return True
        else:
            print("Não existe ordem em aberto!")
            return False
