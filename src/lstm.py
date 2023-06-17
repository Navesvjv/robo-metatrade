import numpy as np
import pandas as pd
import MetaTrader5 as mt5
from enum import Enum
from src.db import DbConnection
from src.symbol import getSymbol
from keras.models import Sequential
from datetime import timedelta, datetime
from keras.layers import Dense, Dropout, LSTM
from sklearn.preprocessing import MinMaxScaler
from keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint


class DenseActivation(Enum):
    LINEAR = "linear"
    SIGMOID = "sigmoid"


class CompilerOptmizer(Enum):
    ADAM = "adam"
    RMSPROP = "rmsprop"


selectLimit = None  # None

numberTest = 5
timeSteps = 5

columnsTraining = set(["open", "close"])
columnsExpected = set(["close"])
columns = list(columnsTraining | columnsExpected)
denseActivation = DenseActivation.SIGMOID.value
compilerOptmizer = CompilerOptmizer.ADAM.value
regressorEpocs = 200
regressorBatchSize = 30


class LSTMModel:
    base_completa = None

    base_treinamento = None
    base_treinamento_normalizada = None
    treinamento_previsores = []
    treinamento_preco_real = []

    base_teste = None
    base_teste_normalizada = None
    teste_previsoes = []
    teste_preco_real = []

    def __init__(self):
        self.dbConnection = DbConnection()
        self.regressor = Sequential()
        self.normalizador = MinMaxScaler(feature_range=(0, 1))

        # self.getDataFromMt5()
        self.getDataFromDb()
        self.extract()
        self.train()
        self.test()

    def test(self):
        pass

    def extract(self):
        # self.base_teste = self.base_completa[-numberTest:].values
        # self.base_teste_normalizada = self.normalizador.transform(self.base_teste)

        self.base_treinamento = self.base_completa[:-numberTest].values
        self.base_treinamento_normalizada = self.normalizador.fit_transform(
            self.base_treinamento
        )

        for i in range(timeSteps, len(self.base_treinamento_normalizada)):
            self.treinamento_previsores.append(
                self.base_treinamento_normalizada[
                    i - timeSteps : i, self.parseColumns(columnsTraining)
                ]
            )
            self.treinamento_preco_real.append(
                self.base_treinamento_normalizada[i, self.parseColumns(columnsExpected)]
            )

        self.treinamento_previsores = np.array(self.treinamento_previsores)
        self.treinamento_preco_real = np.array(self.treinamento_preco_real)

    def train(self):
        if len(columnsTraining) == 1:
            self.treinamento_previsores = np.reshape(
                self.treinamento_previsores,
                (
                    self.treinamento_previsores.shape[0],
                    self.treinamento_previsores.shape[1],
                    1,
                ),
            )

        self.regressor.add(
            LSTM(
                units=100,
                return_sequences=True,
                input_shape=(
                    self.treinamento_previsores.shape[1],
                    len(columnsTraining),
                ),
            )
        )
        self.regressor.add(Dropout(0.3))
        self.regressor.add(LSTM(units=50, return_sequences=True))
        self.regressor.add(Dropout(0.3))
        self.regressor.add(LSTM(units=50, return_sequences=True))
        self.regressor.add(Dropout(0.3))
        self.regressor.add(LSTM(units=50))
        self.regressor.add(Dropout(0.3))

        self.regressor.add(Dense(units=1, activation=denseActivation))
        self.regressor.compile(
            optimizer=compilerOptmizer,
            loss="mean_squared_error",
            metrics=["mean_absolute_error"],
        )

        # es = EarlyStopping(monitor="loss", min_delta=1e-10, patience=10, verbose=1)
        # rlr = ReduceLROnPlateau(monitor="loss", factor=0.2, patience=5, verbose=1)
        mcp = ModelCheckpoint(
            filepath="pesos.h5", monitor="loss", save_best_only=True, verbose=1
        )

        self.regressor.fit(
            self.treinamento_previsores,
            self.treinamento_preco_real,
            epochs=regressorEpocs,
            batch_size=regressorBatchSize,
            callbacks=[mcp],
        )

    def convertExpectedValue(self, open, close):
        return -1 if open > close else 1 if open < close else 0

    def adjustedDate(self):
        delta = timedelta(hours=-3)
        self.base_completa["time"] = [
            (datetime.fromtimestamp(x) - delta) for x in self.base_completa["time"]
        ]

    def convertToDf(self):
        self.base_completa = pd.DataFrame(self.base_completa)
        self.base_completa = self.base_completa.dropna()

    def getDataFromDb(self):
        data = self.dbConnection.fetchAllWinH1(columns, selectLimit)
        self.base_completa = pd.DataFrame(data, columns=columns)

    def saveDataToDb(self):
        self.dbConnection.exec("truncate win_h1", [])
        data = self.base_completa.values.tolist()
        self.dbConnection.insertWinH1(data)

    def getDataFromMt5(self):
        numero_barras = 20000
        self.base_completa = mt5.copy_rates_from_pos(
            "WIN$", mt5.TIMEFRAME_H1, 0, numero_barras
        )

        self.convertToDf()
        self.adjustedDate()
        self.saveDataToDb()

    def parseColumns(self, columns):
        if not len(columns) > 0:
            raise Exception("Columns Training nao pode ser vazio!")

        arr = []
        for i in columns:
            arr.append(self.base_completa.columns.get_loc(str(i)))

        return arr
