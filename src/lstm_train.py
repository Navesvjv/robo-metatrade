import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from sklearn.preprocessing import MinMaxScaler
from keras.callbacks import ModelCheckpoint
from src.config import getConfig
from src.utils import getIndexColumns, saveNormalizer, removeColumnTime

env = getConfig()


class LstmTraining:
    predictors = []
    realPrices = []
    regressor = Sequential()
    trainNormalizer = MinMaxScaler(feature_range=(0, 1))

    def __init__(self, fullBase):
        self.fullBase = fullBase
        self.extract()
        self.training()
        saveNormalizer(self.trainNormalizer)

    def extract(self):
        fullBase = self.fullBase.copy()
        fullBase = removeColumnTime(fullBase)
        colsT, colsE = getIndexColumns(fullBase)

        fullBaseNormalized = self.trainNormalizer.fit_transform(fullBase.values)
        trainingBase = fullBaseNormalized[: -env.numberTest]

        for i in range(env.timeSteps, trainingBase.shape[0]):
            self.predictors.append(trainingBase[i - env.timeSteps : i, colsT])
            self.realPrices.append(trainingBase[i, colsE])

        self.predictors = np.array(self.predictors)
        self.realPrices = np.array(self.realPrices)

        if len(env.columnsTraining) == 1:
            self.predictors = np.reshape(
                self.predictors,
                (
                    self.predictors.shape[0],
                    self.predictors.shape[1],
                    1,
                ),
            )

    def training(self):
        self.regressor.add(
            LSTM(
                units=100,
                return_sequences=True,
                input_shape=(self.predictors.shape[1], len(env.columnsTraining)),
            )
        )
        if env.withDropout:
            self.regressor.add(Dropout(0.3))

        returnSequences = True
        for i in range(env.lstmRepetition):
            if i == (env.lstmRepetition - 1):
                returnSequences = False
            self.regressor.add(LSTM(units=100, return_sequences=returnSequences))
            if env.withDropout:
                self.regressor.add(Dropout(0.3))

        self.regressor.add(Dense(units=1, activation=env.activation))
        self.regressor.compile(
            optimizer=env.optmizer,
            loss="mean_squared_error",
            metrics=["mean_absolute_error"],
        )

        # es = EarlyStopping(monitor="loss", min_delta=1e-10, patience=10, verbose=1)
        # rlr = ReduceLROnPlateau(monitor="loss", factor=0.2, patience=5, verbose=1)
        mcp = ModelCheckpoint(
            filepath=env.filePath + "model.h5",
            monitor="loss",
            save_best_only=True,
            verbose=1,
        )

        self.regressor.fit(
            self.predictors,
            self.realPrices,
            epochs=env.epocs,
            batch_size=env.batchSize,
            callbacks=[mcp],
        )
