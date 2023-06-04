import env
import json
from src.config.singleton import Singleton
from src.config.db import DatabaseConnection


class OrdersRepository(Singleton):
    def __init__(self):
        self.db = DatabaseConnection()

    def insert(self, order, percSell, percBuy):
        order = json.loads(order)

        query = f"""
            INSERT INTO orders 
            (magic, symbol, price, volume, type, retcode, perc_sell, perc_buy) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """

        values = (
            order["request"]["magic"],
            env.symbol,
            order["price"],
            order["volume"],
            order["request"]["type"],
            order["retcode"],
            percSell,
            percBuy,
        )

        try:
            self.db.exec(query, values)
            print(f"Tick {env.symbol}: {order} inserted successfully ✅")
        except Exception as exc:
            print(f"Error(Insert Order): {exc}")

    def getLastIdOrder(self):
        query = f"""
            SELECT MAX(id) FROM orders; 
        """

        try:
            return self.db.exec(query)
        except Exception as exc:
            print(f"Error(getLastIdOrder): {exc}")
