import env
import holidays
import MetaTrader5 as mt5
from datetime import datetime


class Checks:
    def canTrade(self) -> bool:
        if self.isHoliday():
            return False
        elif self.isWeekend():
            return False
        elif self.isTimeCloseOrders():
            return False
        elif self.existsAnyOpenPosition():
            return False
        elif self.isTimeTrading():
            return True

        return False

    def existsAnyOpenPosition(self) -> bool:
        positions = mt5.positions_get()

        if positions:
            print(f"Existe posição em aberto!")
            return True

        return False

    def existsOpenPositionBySymbol(self, symbol) -> bool:
        positions = mt5.positions_get()
        openPositions = [p for p in positions if p.symbol == symbol]

        if openPositions:
            print(f"Existe posição em aberto para o {symbol}!")
            return True

        return False

    def isTimeTrading(self) -> bool:
        currentTime = datetime.now().time()
        startTime = datetime.strptime(env.start_trading_time, "%H:%M").time()
        endTime = datetime.strptime(env.stop_trading_time, "%H:%M").time()

        if startTime <= currentTime <= endTime:
            return True

        print("Não é hora de operar! ❌")
        return False

    def isTimeCloseOrders(self) -> bool:
        currentTime = datetime.now().time()
        closeTime = datetime.strptime(env.close_orders_time, "%H:%M").time()

        if currentTime >= closeTime:
            print("Hora de fechar orderns! ⚠️")
            return True

        return False

    def isWeekend(self) -> bool:
        today = datetime.today()

        if today.weekday() >= 5:
            print("É fim de semana! ❌")
            return True

        return False

    def isHoliday(self) -> bool:
        today = datetime.today()
        brHolidays = holidays.BR()

        if today in brHolidays:
            print("Hoje é feriado! ❌")
            return True

        return False
