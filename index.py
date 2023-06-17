from src.db import DbConnection
from src.mt import Metatrader
from src.check import Checks
from src.copy_rates import CopyRates
from src.lstm import LSTMModel


class Init:
    def __init__(self):
        self.check = Checks()

        if not self.check.isHoliday() and not self.check.isWeekend():
            self.mt = Metatrader()
            self.lstm = LSTMModel()
            # self.dbConnection = DbConnection()
            # self.copyRates = CopyRates()

            # self.data = self.copyRates.get()
            # self.lstm.exec(self.data)


Init()
