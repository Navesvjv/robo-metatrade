import pandas as pd
import mysql.connector
from src.config import getConfig
from src.utils import convertDate
from src.singleton import Singleton

env = getConfig()


class DbConnection(Singleton):
    conn = None
    fullBase = None

    def __init__(self):
        if self._wasInstantiated is None:
            self.openDbConnection()

        self._wasInstantiated = True

    def exec(self, query, data):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()

    def execMany(self, query, data):
        cursor = self.conn.cursor()
        cursor.executemany(query, data)
        self.conn.commit()
        cursor.close()

    def fetchAllWinH1(self):
        if self.fullBase is None:
            cursor = self.conn.cursor()
            limit = f" limit {env.selectLimit} " if env.selectLimit else ""
            cursor.execute(f"select {', '.join(env.columns)} from win_h1 {limit}")
            data = cursor.fetchall()
            cursor.close()

            self.fullBase = pd.DataFrame(data, columns=env.columns)
            self.fullBase = self.fullBase.dropna()
            if "time" in self.fullBase.columns:
                self.fullBase["time"] = convertDate(self.fullBase)

        return self.fullBase

    def insertWinH1(self, data):
        query = """
            INSERT INTO win_h1 (
                time, open, high, low, close, tick_volume, spread, real_volume
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        self.execMany(query, data)

    def openDbConnection(self):
        self.conn = mysql.connector.connect(
            host=env.dbHost,
            user=env.dbUser,
            password=env.dbPass,
            database=env.dbName,
        )

        if self.conn.is_connected():
            print(f"Database connected! ✅")
        else:
            raise Exception("Database connection not established! ❌")

    def closeDbConnection(self):
        self.conn.close()
        print("Closed database! ✅")
