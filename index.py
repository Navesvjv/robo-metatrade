from src.config.mt5 import Metatrader
from src.strategies.nameless_strategy import NamelessStrategy

metatrader = Metatrader()
namelessStrategy = NamelessStrategy()

metatrader.initialize()
namelessStrategy.execute()
metatrader.shutdown()
