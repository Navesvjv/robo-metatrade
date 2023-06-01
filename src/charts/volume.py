import matplotlib.pyplot as plt


class VolumeChart:
    def __init__(self):
        categorias = ["109045", "109050", "109055"]
        valores = [10, 15, 12]

        fig, ax = plt.subplots()
        self.bar_plot = ax.barh(categorias, valores)

        plt.xlabel("Volumes")
        plt.ylabel("Prices")
        plt.title("Gráfico de Barras Horizontal")

    def plot(self, values):
        for bar, newValue in zip(self.bar_plot, values):
            bar.set_width(newValue)

        plt.draw()
        plt.pause(1)

    def close():
        plt.close()
