import env
from datetime import datetime


selectLimit = env.selectLimit
numberTest = env.numberTest
timeSteps = env.timeSteps
withDropout = env.withDropout
lstmRepetition = env.lstmRepetition
columnsTraining = set(env.columnsTraining)
columnsExpected = set(env.columnsExpected)
denseActivation = env.denseActivation
compilerOptmizer = env.compilerOptmizer
regressorEpocs = env.regressorEpocs
regressorBatchSize = env.regressorBatchSize

joinedColumnsTraining = "-".join(sorted(columnsTraining))
joinedColumnsExpected = "-".join(sorted(columnsExpected))
timestampCurrent = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

columns = list(columnsTraining | columnsExpected)

concatenatedColumns = "-".join(
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


class AsDict:
    def __init__(self, dicionario):
        self.__dict__.update(dicionario)


def getConfig():
    return AsDict(
        {
            "selectLimit": selectLimit,
            "numberTest": numberTest,
            "timeSteps": timeSteps,
            "withDropout": withDropout,
            "lstmRepetition": lstmRepetition,
            "columnsTraining": columnsTraining,
            "columnsExpected": columnsExpected,
            "columns": columns,
            "activation": denseActivation,
            "optmizer": compilerOptmizer,
            "epocs": regressorEpocs,
            "batchSize": regressorBatchSize,
            "filePath": "models/" + concatenatedColumns + "/",
            "dbHost": env.db_host,
            "dbName": env.db_name,
            "dbUser": env.db_user,
            "dbPass": env.db_pass,
        }
    )
