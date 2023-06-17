import env as env
import MetaTrader5 as mt5
from .singleton import Singleton
from .db import DatabaseConnection
from .check import Checks
from src.strategies.nameless_strategy_win import NamelessStrategyWIN


class Metatrader(Singleton):
    def __init__(self):
        if self._wasInstantiated is None:
            self.checks = Checks()

            if not self.checks.isHoliday() and not self.checks.isWeekend():
                self.namelessStrategyWIN = NamelessStrategyWIN()
                self.initialize()

        self._wasInstantiated = True

    def initialize(self):
        try:
            if not mt5.initialize(
                login=env.account, server=env.server, password=env.password
            ):
                raise Exception(
                    f"Falha ao inicializar o metatrader 5 ❌\n Error: {mt5.last_error()}"
                )
            else:
                print(f"MetaTrader inicializado! ✅")

            DatabaseConnection()
        except Exception as exc:
            print(exc)
            quit()

        self.callStrategies()

    def callStrategies(self):
        if env.execSymbols:
            for symb in env.execSymbols:
                if symb == "WIN":
                    self.namelessStrategyWIN.execute()
        else:
            print("Nenhum simbolo informado na env.execSymbols ❌")
            self.shutdown()

    def closeAllPositions(self):
        positions = mt5.positions_get()

        for position in positions:
            result = mt5.position_close(position)

            if result.retcode == mt5.TRADE_RETCODE_DONE:
                print(f"Posição {position.ticket} fechada com sucesso.")
            else:
                print(f"Erro ao fechar a posição {position.ticket}: {result.comment}")

    def shutdown(self):
        mt5.shutdown()
        print(f"Closed Metatrader! ✅")
        quit()
