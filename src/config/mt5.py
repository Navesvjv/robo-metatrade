import env as env
import MetaTrader5 as mt5
from singleton import Singleton
from db import DatabaseConnection


class Metatrader(Singleton):
    def __init__(self):
        self.initialize()

    def initialize(self):
        try:
            DatabaseConnection()

            if not mt5.initialize(
                login=env.account, server=env.server, password=env.password
            ):
                raise Exception(
                    f"Falha ao inicializar o metatrader 5 ❌\n Error: {mt5.last_error()}"
                )
        except Exception as exc:
            print(exc)
            quit()

    def shutdown(self):
        mt5.shutdown()
        print(f"Closed Metatrader! ✅")
        quit()
