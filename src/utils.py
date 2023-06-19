import pickle
from src.config import getConfig
from datetime import datetime, timedelta

env = getConfig()

fileNameTrainNormalizer = "train_normalizer"
fileNameTestNormalizer = "test_normalizer"


def getIndexColumns(fullBase):
    colsT = [fullBase.columns.get_loc(str(i)) for i in env.columnsTraining]
    colsE = [fullBase.columns.get_loc(str(i)) for i in env.columnsExpected]
    return colsT, colsE


def getIndexColumnsToyTest(fullBase):
    return [fullBase.columns.get_loc(str(i)) for i in ["open", "close"]]


def saveNormalizer(
    normalizer,
    type="train",
):
    name = fileNameTrainNormalizer
    if type == "test":
        name = fileNameTestNormalizer
    with open(env.filePath + name + ".pkl", "wb") as file:
        pickle.dump(normalizer, file)


def getNormalizer(type="train"):
    name = fileNameTrainNormalizer
    if type == "test":
        name = fileNameTestNormalizer
    with open(env.filePath + name + ".pkl", "rb") as file:
        return pickle.load(file)


def convertDate(fullBase):
    delta = timedelta(hours=-3)
    return [(datetime.fromtimestamp(x) - delta) for x in fullBase["time"]]


def removeColumnTime(fullBase):
    data = fullBase.copy()
    if "time" in data.columns:
        data.drop("time", axis=1)
    return data
