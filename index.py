from src.config.mt5 import Metatrader
from src.recordings.tick_recorder import TickRecorder
from src.testes.print_orders import PrintOrders
from src.charts.volume import VolumeChart
from src.charts.chart import BarChart


data = [
    {"type": 1, "price": 108890.0, "volume": 578},
    {"type": 1, "price": 108880.0, "volume": 842},
    {"type": 1, "price": 108870.0, "volume": 243},
    {"type": 2, "price": 108860.0, "volume": 153},
    {"type": 2, "price": 108850.0, "volume": 453},
    {"type": 2, "price": 108840.0, "volume": 244},
]

categories = [item["price"] for item in data]
chart = BarChart(categories)

chart.update_values(data)
