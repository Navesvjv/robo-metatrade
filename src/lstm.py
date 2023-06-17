import numpy as np
import pandas as pd
from datetime import datetime
import MetaTrader5 as mt5
from enum import Enum
from src.db import DbConnection
from src.symbol import getSymbol
from keras.models import Sequential, load_model
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
timeSteps = 20
withDropout = False
lstmRepetition = 0

columnsTraining = set(["open", "close"])
columnsExpected = set(["close"])
columns = list(columnsTraining | columnsExpected)
denseActivation = DenseActivation.SIGMOID.value
compilerOptmizer = CompilerOptmizer.ADAM.value
regressorEpocs = 100
regressorBatchSize = 10

joinedColumnsTraining = "-".join(sorted(columnsTraining))
joinedColumnsExpected = "-".join(sorted(columnsExpected))
timestampCurrent = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
concatenatedColumns = (
    "-".join(
        [str(numberTest)]
        + [str(timeSteps)]
        + [str("true" if withDropout else "false")]
        + [str(lstmRepetition)]
        + [f"{joinedColumnsTraining}_{joinedColumnsExpected}"]
        + [denseActivation]
        + [compilerOptmizer]
        + [str(regressorEpocs)]
        + [str(regressorBatchSize)]
    )
    + ".h5"
)

print(concatenatedColumns)


class LSTMModel:
    base_completa = None

    base_treinamento = None
    base_treinamento_normalizada = None
    treinamento_previsores = []
    treinamento_preco_real = []

    base_teste = None
    base_teste_normalizada = None
    teste_previsores = []
    teste_precos_esperados = None

    def __init__(self):
        self.dbConnection = DbConnection()
        self.regressor = Sequential()
        self.normalizador_treinamento = MinMaxScaler(feature_range=(0, 1))
        self.normalizador_previsao = MinMaxScaler(feature_range=(0, 1))

        # self.getDataFromMt5()
        self.getDataFromDb()
        self.extractDataToTrain()
        self.extractDataToPredict()
        self.extract()
        self.prever()
        # self.train()
        # self.test()

    def prever(self):
        modelo = load_model(concatenatedColumns)
        previsoes = modelo.predict(self.teste_previsores)
        previsoes = self.normalizador_previsao.inverse_transform(previsoes)
        print(previsoes)
        print(self.teste_precos_esperados)

    def test(self):
        previsoes = self.regressor.predict(self.teste_previsores)
        previsoes = self.normalizador_previsao.inverse_transform(previsoes)
        print(previsoes)
        print(self.teste_precos_esperados)

    def extract(self):
        # TRAIN
        self.base_treinamento = self.base_completa[:-numberTest].values
        self.base_treinamento_normalizada = self.normalizador_treinamento.fit_transform(
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

        if len(columnsTraining) == 1:
            self.treinamento_previsores = np.reshape(
                self.treinamento_previsores,
                (
                    self.treinamento_previsores.shape[0],
                    self.treinamento_previsores.shape[1],
                    1,
                ),
            )

        # TEST
        self.base_teste = self.base_completa[-timeSteps - numberTest :].values
        self.teste_precos_esperados = self.base_teste[
            -numberTest:, self.parseColumns(columnsExpected)
        ]
        self.base_teste_normalizada = self.normalizador_treinamento.transform(
            self.base_teste
        )

        self.normalizador_previsao.fit_transform(
            self.base_treinamento[:, self.parseColumns(columnsExpected)]
        )

        for i in range(timeSteps, len(self.base_teste_normalizada)):
            self.teste_previsores.append(
                self.base_teste_normalizada[
                    i - timeSteps : i, self.parseColumns(columnsTraining)
                ]
            )
        self.teste_previsores = np.array(self.teste_previsores)

        if len(columnsTraining) == 1:
            self.teste_previsores = np.reshape(
                self.teste_previsores,
                (
                    self.teste_previsores.shape[0],
                    self.teste_previsores.shape[1],
                    1,
                ),
            )

    def train(self):
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
        if withDropout:
            self.regressor.add(Dropout(0.3))

        returnSequences = True
        for i in range(lstmRepetition):
            if i == (lstmRepetition - 1):
                returnSequences = False
            self.regressor.add(LSTM(units=50, return_sequences=returnSequences))
            if withDropout:
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
            filepath=concatenatedColumns, monitor="loss", save_best_only=True, verbose=1
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
