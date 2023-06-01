from src.config.mt5 import Metatrader
from src.recordings.tick_recorder import TickRecorder
from src.testes.print_orders import PrintOrders

metatrader = Metatrader()
metatrader.initialize()

printOrders = PrintOrders()
printOrders.getOrders()


# tickRecorde = TickRecorder()
# tickRecorde.record1min()

metatrader.shutdown()

# from datetime import datetime
# from src.repositories.tick_repository import TickRepository

# repo = TickRepository()

# tick = {}
# tick["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-7]
# tick["volume"] = 3425
# tick["bid"] = 100.032
# tick["ask"] = 100.014

# repo.insert(tick, "ticks_win_1min")
