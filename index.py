from src.config.mt5 import Metatrader
from src.strategies.nameless_strategy import NamelessStrategy

metatrader = Metatrader()
namelessStrategy = NamelessStrategy()

namelessStrategy.execute()
metatrader.shutdown()
