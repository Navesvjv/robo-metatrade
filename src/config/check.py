import env
import holidays
import MetaTrader5 as mt5
from datetime import datetime
from src.config.singleton import Singleton
from config.orders.orders import Orders


class Checks(Singleton):
    def __init__(self):
        if self._wasInstantiated is None:
            self.orders = Orders()

        self._wasInstantiated = True

    def canTrade(self, symbol):
        if self.isTimeCloseOrders:
            if self.existsOpenPosition(symbol):
                self.orders.closeAllOrders()

            return "stop"

        elif self.isTimeTrading():
            if self.existsOpenPosition(symbol):
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

    def existsOpenPosition(self, symbol):
        positions = mt5.positions_get()
        openPositions = [p for p in positions if p.symbol == symbol]

        if openPositions:
            print(f"Existe posição em aberto para o {symbol}!")
            return True
        else:
            print(f"Não existe posição em aberto para o {symbol}!")
            return False

    def isWeekend(self):
        today = datetime.today()
        isWeekend = today.weekday() >= 5
        if isWeekend:
            print("É fim de semana! ❌")
            quit()
        return isWeekend

    def isHoliday(self):
        today = datetime.today()
        brHolidays = holidays.BR()

        if today in brHolidays:
            print("Hoje é feriado! ❌")
            quit()
        else:
            return False
