import env
import holidays
import MetaTrader5 as mt5
from .mt5 import Metatrader
from datetime import datetime
from src.config.singleton import Singleton
from src.config.orders.orders_win import OrdersWIN


class Checks(Singleton):
    def __init__(self):
        if self._wasInstantiated is None:
            self.metatrader = Metatrader()
            self.ordersWin = OrdersWIN()

        self._wasInstantiated = True

    def canTrade(self, symbol):
        if self.isTimeCloseOrders:
            if self.existsAnyOpenPosition():
                self.metatrader.closeAllPositions()

            return "stop"

        elif self.isTimeTrading():
            if self.existsOpenPositionBySymbol(symbol):
                return "await"
            return "continue"
        else:
            return "stop"

    def existsAnyOpenPosition(self):
        positions = mt5.positions_get()

        if positions:
            print(f"Existe posição em aberto!")
            return True
        else:
            print(f"Não existe posição em aberto!")
            return False

    def existsOpenPositionBySymbol(self, symbol):
        positions = mt5.positions_get()
        openPositions = [p for p in positions if p.symbol == symbol]

        if openPositions:
            print(f"Existe posição em aberto para o {symbol}!")
            return True
        else:
            print(f"Não existe posição em aberto para o {symbol}!")
            return False

    def isTimeTrading(self) -> bool:
        currentTime = datetime.now().time()
        startTime = datetime.strptime(env.start_trading_time, "%H:%M").time()
        endTime = datetime.strptime(env.stop_trading_time, "%H:%M").time()

        if startTime <= currentTime <= endTime:
            print("Hora de operar!")
            return True
        else:
            print("Não é hora de operar! ❌")
            return False

    def isTimeCloseOrders(self) -> bool:
        currentTime = datetime.now().time()
        closeTime = datetime.strptime(env.close_orders_time, "%H:%M").time()

        if currentTime >= closeTime:
            print("Hora de fechar orderns! ⚠️")
            return True
        else:
            print("Não é hora de fechar ordens!")
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
