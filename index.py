from src.db import DbConnection
from src.mt import Metatrader
from src.check import Checks
from src.lstm_train import LstmTraining
from src.lstm_test import LstmTest

# from src.lstm import LSTMModel


class Init:
    def __init__(self):
        self.check = Checks()
        self.dbConnection = DbConnection()

        self.mt = Metatrader()
        self.lstmTraining = LstmTraining(self.dbConnection.fetchAllWinH1())
        self.lstmTest = LstmTest(self.dbConnection.fetchAllWinH1())

        # self.lstm = LSTMModel()

        # if not self.check.isHoliday() and not self.check.isWeekend():
        # self.dbConnection = DbConnection()
        # self.copyRates = CopyRates()

        # self.data = self.copyRates.get()
        # self.lstm.exec(self.data)


Init()
