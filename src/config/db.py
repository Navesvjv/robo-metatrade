import env
import mysql.connector
from .singleton import Singleton


class DatabaseConnection(Singleton):
    def __init__(self):
        self.host = env.db_host
        self.user = env.db_user
        self.password = env.db_pass
        self.database = env.db_name
        self.connection = None
        self._connected = False

        if not self._connected:
            self.connect()

    def exec(self, query, values):
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        self.connection.commit()
        cursor.close()

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )

        if self.connection.is_connected():
            self._connected = True
            print(f"Connected database! ✅")
        else:
            raise Exception("Database connection not established! ❌")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Closed database! ✅")
