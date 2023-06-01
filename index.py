import matplotlib.pyplot as plt
import numpy as np


class BarChart:
    def __init__(self, categories):
        self.categories = categories
        self.values = []
        self.fig, self.ax = plt.subplots(2, 1, figsize=(8, 6))
        self.bar_container = self.ax[0].bar(self.categories, self.values)

    def update(self, data):
        self.values = [item["volume"] for item in data]
        average_volume = np.mean(self.values)

        for bar, value in zip(self.bar_container, self.values):
            bar.set_height(value)

        self.ax[0].set_ylim(0, max(self.values) * 1.1)
        self.ax[0].set_ylabel("Volume")

        self.ax[1].bar(0, average_volume, color="red")
        self.ax[1].set_xlim(-0.5, 0.5)
        self.ax[1].set_ylim(0, max(self.values) * 1.1)
        self.ax[1].set_xticks([])
        self.ax[1].set_yticks([])
        self.ax[1].spines["left"].set_visible(False)
        self.ax[1].spines["right"].set_visible(False)
        self.ax[1].spines["top"].set_visible(False)
        self.ax[1].spines["bottom"].set_visible(False)
        self.ax[1].annotate(
            f"Average: {average_volume}",
            xy=(0, average_volume),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            color="red",
        )

        plt.tight_layout()
        plt.draw()
        plt.pause(0.001)
