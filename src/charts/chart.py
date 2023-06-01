import matplotlib.pyplot as plt


class BarChart:
    def __init__(self, categories):
        self.categories = categories
        self.values = [0] * len(categories)

        # Definir as cores para cada tipo
        self.colors = {1: "blue", 2: "red"}

        # Configurar o gráfico inicial
        self.fig, self.ax = plt.subplots()
        self.bar_plot = self.ax.bar(
            range(len(self.categories)), self.values, color="gray"
        )

        # Definir as propriedades do gráfico
        plt.xlabel("Preço")
        plt.ylabel("Volume")
        plt.title("Gráfico de Barras")

    def update_values(self, data):
        # Atualizar os valores com base nos dados fornecidos
        self.values = [item["volume"] for item in data]

        # Atualizar as cores das barras com base nos tipos
        colors = [self.colors[item["type"]] for item in data]

        # Atualizar o gráfico de barras
        for bar, value, color in zip(self.bar_plot, self.values, colors):
            bar.set_height(value)
            bar.set_color(color)

        # Atualizar os rótulos do eixo x com os preços
        plt.xticks(range(len(self.categories)), self.categories)

        # Atualizar o gráfico
        plt.draw()
