from src.config.mt5 import Metatrader
from src.strategies.nameless_strategy import NamelessStrategy

metatrader = Metatrader()
metatrader.initialize()

namelessStrategy = NamelessStrategy()
namelessStrategy.handler()
