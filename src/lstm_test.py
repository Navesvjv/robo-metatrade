from sklearn.preprocessing import MinMaxScaler
from src.config import getConfig
from src.utils import getNormalizer

env = getConfig()


class LstmTest:
    previsores = []
    normalizer = MinMaxScaler(feature_range=(0, 1))

    def __init__(self, baseCompleta):
        self.baseCompleta = baseCompleta
        self.normalizer = getNormalizer()
        self.extractData()
        self.predict()

    def extractData(self):
        pass

    def predict():
        pass
