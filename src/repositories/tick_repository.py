import env
from src.config.singleton import Singleton
from src.config.db import DatabaseConnection


class TickRepository(Singleton):
    def __init__(self):
        self.db = DatabaseConnection()

    def insert(self, tick, tableName):
        query = f"INSERT INTO {tableName} (symbol, time, volume, bid, ask) VALUES (%s, %s, %s, %s, %s)"
        values = (env.symbol, tick[0], tick[4], tick[1], tick[2])
        self.db.exec(query, values)
        print(f"Tick {env.symbol}: {tick[0]} inserted successfully ✅")
