import matplotlib.pyplot as plt
import numpy as np


class BarChart:
    def __init__(self, categories):
        self.categories = categories
        self.values = [0] * len(categories)
        self.colors = {1: "blue", 2: "red"}

        self.fig, self.ax = plt.subplots()
        self.bar_plot = self.ax.barh(
            np.arange(len(self.categories)), self.values, color="gray"
        )

        plt.xlabel("Volume")
        plt.ylabel("Preço")
        plt.title("Gráfico de Barras")

    def update_values(self, data):
        self.values = [item["volume"] for item in data]
        colors = [self.colors[item["type"]] for item in data]

        self.ax.clear()
        self.bar_plot = self.ax.barh(
            np.arange(len(self.categories)), self.values, color=colors
        )

        plt.yticks(np.arange(len(self.categories)), self.categories)
        plt.draw()

        # Exibir o gráfico
        plt.show()


# Exemplo de uso
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
