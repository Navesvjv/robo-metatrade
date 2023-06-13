import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from sklearn.preprocessing import MinMaxScaler
from src.config.db import DatabaseConnection

model = Sequential()
db = DatabaseConnection()
normalizador = MinMaxScaler(feature_range=(0, 1))

numero_de_previsores = 90
numero_de_celulas_de_memoria = 100

query = f""""
    SELECT * FROM win_1min
"""

base = pd.read_sql(query, db.connection)

# base[base.isna().any(axis=1)]  # Mostra se tem algum NaN
# base = base.dropna() # Remove os NaN

base_treinamento = base.iloc[:, 1:2].values  # rows, columns
base_treinamento_normalizada = normalizador.fit_transform(base_treinamento)


previsores = []
preco_real = []
for i in range(numero_de_previsores, len(base_treinamento_normalizada)):
    previsores.append(base_treinamento_normalizada[i - numero_de_previsores : i, 0])
    preco_real.append(base_treinamento_normalizada[i, 0])

previsores, preco_real = np.array(previsores), np.array(preco_real)
previsores = np.reshape(previsores, (previsores.shap[0], previsores.shape[1], 1))

model.add(
    LSTM(
        units=numero_de_celulas_de_memoria,
        return_sequences=True,
        input_shape=(previsores.shape[1], 1),
    )
)

model.add(Dropout(0.3))
