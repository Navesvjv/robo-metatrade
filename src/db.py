import env
import mysql.connector
from src.singleton import Singleton


class DbConnection(Singleton):
    conn = None

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

    def fetchAllWinH1(self, columns, limit=None):
        cursor = self.conn.cursor()
        limit = f" limit {limit} " if limit else ""
        cursor.execute(f"select {', '.join(columns)} from win_h1 {limit}")
        data = cursor.fetchall()
        cursor.close()

        return data

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
            host=env.db_host,
            user=env.db_user,
            password=env.db_pass,
            database=env.db_name,
        )

        if self.conn.is_connected():
            print(f"Database connected! ✅")
        else:
            raise Exception("Database connection not established! ❌")

    def closeDbConnection(self):
        self.conn.close()
        print("Closed database! ✅")
