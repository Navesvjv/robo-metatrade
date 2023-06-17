import pickle
from src.config import getConfig
from datetime import datetime, timedelta

env = getConfig()


def getIndexColumns(fullBase):
    return (
        [fullBase.columns.get_loc(str(i)) for i in env.columnsTraining],
        [fullBase.columns.get_loc(str(i)) for i in env.columnsExpected],
    )


def saveNormalizer(normalizer):
    with open(env.filePath + "training_normalizer.pkl", "wb") as file:
        pickle.dump(normalizer, file)


def getNormalizer():
    with open(env.filePath + "training_normalizer.pkl", "rb") as file:
        return pickle.load(file)


def convertDate(fullBase):
    delta = timedelta(hours=-3)
    return [(datetime.fromtimestamp(x) - delta) for x in fullBase["time"]]
