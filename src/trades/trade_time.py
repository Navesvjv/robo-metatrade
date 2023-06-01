import env
from datetime import datetime
from src.config.singleton import Singleton


class TradeTime(Singleton):
    def isTradingTime() -> bool:
        current_time = datetime.now().time()
        start_time = datetime.strptime(env.start_trading_time, "%H:%M").time()
        end_time = datetime.strptime(env.stop_trading_time, "%H:%M").time()

        return True if start_time <= current_time <= end_time else False

    def isCloseOrdersTime() -> bool:
        current_time = datetime.now().time()
        start_time = datetime.strptime(env.stop_trading_time, "%H:%M").time()
        end_time = datetime.strptime(env.close_orders_time, "%H:%M").time()

        return True if start_time <= current_time <= end_time else False
