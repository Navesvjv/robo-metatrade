selectLimit = None  # None or number (int)
numberTest = 100
timeSteps = 100
withDropout = False
lstmRepetition = 3  # Pelo menos 1
columnsTraining = ["open", "close"]  # sempre ter open e close
columnsExpected = ["close"]
denseActivation = "sigmoid"  # 'sigmoid' / 'linear'
compilerOptmizer = "rmsprop"  # 'adam' / 'rmsprop'
regressorEpocs = 100
regressorBatchSize = 10

# ACCOUNT
account = 52989530
password = "Naves223540@@"
server = "XPMT5-DEMO"

# TRADE TIME
start_trading_time = "09:10"
stop_trading_time = "16:00"
close_orders_time = "16:30"

# DATABASE
db_host = "localhost"
db_user = "root"
db_name = "metatrader"
db_pass = "00987"
