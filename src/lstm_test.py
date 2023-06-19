import numpy as np
from sklearn.preprocessing import MinMaxScaler
from src.config import getConfig
from src.utils import (
    getNormalizer,
    getIndexColumns,
    removeColumnTime,
    getIndexColumnsToyTest,
)
from keras.models import load_model

env = getConfig()


class LstmTest:
    xTest = []
    yTest = None
    predictions = None
    normalizer = MinMaxScaler(feature_range=(0, 1))

    def __init__(self, fullBase):
        self.fullBase = fullBase
        self.trainNormalizer = getNormalizer()
        self.testNormalizer = MinMaxScaler(feature_range=(0, 1))
        self.extract()
        self.predict()
        self.compare()

    def extract(self):
        fullBase = self.fullBase.copy()
        fullBase = removeColumnTime(fullBase)
        colsT, colsE = getIndexColumns(fullBase)

        self.yTest = fullBase.iloc[-env.numberTest :, getIndexColumnsToyTest(fullBase)]
        self.yTest = self.yTest.reset_index()
        self.testNormalizer.fit_transform(fullBase.iloc[:, colsE].values)

        testBase = fullBase[-env.timeSteps - env.numberTest :].values
        testBase = self.trainNormalizer.transform(testBase)

        for i in range(env.timeSteps, testBase.shape[0]):
            self.xTest.append(testBase[i - env.timeSteps : i, colsT])

        self.xTest = np.array(self.xTest)
        print(self.xTest.shape)

        if len(env.columnsTraining) == 1:
            self.xTest = np.reshape(
                self.xTest,
                (self.xTest.shape[0], self.xTest.shape[1], 1),
            )

    def predict(self):
        model = load_model(env.filePath + "model.h5")
        self.predictions = model.predict(self.xTest)
        self.predictions = self.testNormalizer.inverse_transform(self.predictions)
        print(self.predictions)
        print(self.yTest)

    def compare(self):
        soma = 0
        for i, row in self.yTest.iterrows():
            dif = row["open"] - row["close"]
            dif_calc = row["open"] - self.predictions[i][0]

            if (dif > 0 and dif_calc > 0) or (dif < 0 and dif_calc < 0):
                soma += abs(dif)
            else:
                soma -= abs(dif)

            print(
                f"OPEN: {row['open']} - CLOSE: {row['close']} === {dif} / {'UP' if dif < 0 else 'DOWN'}"
            )
            print(f"Calculated: {dif_calc}")
            print("\n")

        print(f"RESULTING POINTS: {soma}")
        with open(env.filePath + "arquivo.txt", "w") as arquivo:
            arquivo.write(f"Calculated: {soma}")
