import env as env
import MetaTrader5 as mt5


class Metatrader:
    def __init__(self):
        if not mt5.initialize(
            login=env.account, server=env.server, password=env.password
        ):
            raise Exception(
                f"Falha ao inicializar o metatrader 5 ❌\n Error: {mt5.last_error()}"
            )

    def shutdown(self):
        mt5.shutdown()
        print(f"Metatrader closed! ✅")
