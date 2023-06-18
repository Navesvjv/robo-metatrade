import numpy as np
from sklearn.preprocessing import MinMaxScaler
from src.config import getConfig
from src.utils import getNormalizer, getIndexColumns, removeColumnTime
from keras.models import load_model

env = getConfig()


class LstmTest:
    xTest = []
    yTest = None
    normalizer = MinMaxScaler(feature_range=(0, 1))

    def __init__(self, fullBase):
        self.fullBase = fullBase
        self.trainNormalizer = getNormalizer()
        self.testNormalizer = MinMaxScaler(feature_range=(0, 1))
        self.extract()
        self.predict()

    def extract(self):
        fullBase = self.fullBase.copy()
        fullBase = removeColumnTime(fullBase)
        colsT, colsE = getIndexColumns(fullBase)

        self.yTest = fullBase.iloc[-env.numberTest :, colsE]
        self.testNormalizer.fit_transform(fullBase.iloc[:, colsE].values)

        testBase = fullBase[-env.timeSteps - env.numberTest :].values
        testBase = self.trainNormalizer.transform(testBase)

        for i in range(env.timeSteps, len(testBase)):
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
        predictions = model.predict(self.xTest)
        print(predictions.shape)

        predictions_reshaped = predictions.reshape(
            (predictions.shape[0], predictions.shape[1])
        )
        print(predictions_reshaped.shape)

        # a = np.array(predictions)
        # a = a.reshape(a, (a.shape[0], a.shape[1]))

        b = self.testNormalizer.inverse_transform(predictions_reshaped)
        print(b)
