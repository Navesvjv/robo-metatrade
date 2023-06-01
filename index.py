import matplotlib.pyplot as plt
import numpy as np


class BarChart:
    def __init__(self, categories):
        self.categories = categories
        self.values = [0] * len(categories)
        self.colors = {1: "blue", 2: "red"}

        self.fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
        self.bar_plot = ax1.barh(
            np.arange(len(self.categories)), self.values, color="gray"
        )
        self.average_bar = ax2.bar(0, 0, color="green")

        ax1.set_xlabel("Volume")
        ax1.set_ylabel("Preço")
        ax1.set_title("Gráfico de Barras")
        ax2.set_xlim(-0.5, 0.5)
        ax2.set_ylim(0, max(self.values) * 1.1)
        ax2.set_xticks([])
        ax2.set_yticks([])
        ax2.spines["left"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.spines["top"].set_visible(False)
        ax2.spines["bottom"].set_visible(False)

    def update_values(self, data):
        self.values = [item["volume"] for item in data]
        colors = [self.colors[item["type"]] for item in data]
        average_volume = np.mean(self.values)

        self.bar_plot = self.ax1.barh(
            np.arange(len(self.categories)), self.values, color=colors
        )
        self.average_bar.set_height(average_volume)

        self.ax1.set_yticks(np.arange(len(self.categories)))
        self.ax1.set_yticklabels(self.categories)

        plt.draw()
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
