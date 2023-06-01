import matplotlib.pyplot as plt
import numpy as np


class BarChart:
    def __init__(self, categories):
        self.categories = categories
        self.values = [0] * len(categories)
        self.colors = {1: "green", 2: "red"}

        self.fig, self.ax = plt.subplots()

        self.ax.spines["right"].set_visible(False)
        self.ax.spines["top"].set_visible(False)
        self.ax.yaxis.tick_left()
        self.ax.xaxis.tick_bottom()
        self.ax.spines["left"].set_linewidth(0.5)
        self.ax.spines["bottom"].set_linewidth(0.5)

        self.bar_plot = self.ax.barh(
            np.arange(len(self.categories)), self.values, color="gray"
        )
        self.mean_line = self.ax.axvline(0, color="blue", linestyle="--", linewidth=1)

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

        mean_volume = np.mean(self.values)
        self.mean_line = self.ax.axvline(
            mean_volume, color="blue", linestyle="--", linewidth=1
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
