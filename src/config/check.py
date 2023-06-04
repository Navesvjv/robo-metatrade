import env
from datetime import datetime
import MetaTrader5 as mt5
from src.config.singleton import Singleton
from src.config.orders import Orders


class Checks(Singleton):
    def __init__(self):
        if self._wasInstantiated is None:
            self.orders = Orders()

        self._wasInstantiated = True

    def canTrade(self):
        if self.isTimeCloseOrders:
            if self.existsOpenOrder():
                self.orders.closeAllOrders()

            return "stop"

        elif self.isTimeTrading():
            if self.existsOpenOrder():
                return "await"
            return "continue"
        else:
            return "stop"

    def isTimeTrading(self) -> bool:
        current_time = datetime.now().time()
        start_time = datetime.strptime(env.start_trading_time, "%H:%M").time()
        end_time = datetime.strptime(env.stop_trading_time, "%H:%M").time()

        if start_time <= current_time <= end_time:
            print("Hora de operar!")
            return True
        else:
            print("Não é hora de operar! ❌")
            return False

    def isTimeCloseOrders(self) -> bool:
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

    def is_weekend(self):
        today = datetime.today()
        isWeekend = today.weekday() >= 5
        if isWeekend:
            print("É fim de semana! ❌")
        return isWeekend
