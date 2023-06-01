import random
import matplotlib.pyplot as plt


class VolumeChart:
    def plot(self):
        # Dados iniciais
        categorias = ["Categoria 1", "Categoria 2", "Categoria 3"]
        valores = [10, 15, 12]

        # Configurar o gráfico inicial
        fig, ax = plt.subplots()
        bar_plot = ax.barh(categorias, valores)

        # Definir as propriedades do gráfico
        plt.xlabel("Valores")
        plt.ylabel("Categorias")
        plt.title("Gráfico de Barras Horizontal")

        # Atualizar os valores em tempo real
        while True:
            # Gerar novos valores aleatórios
            novos_valores = [random.randint(5, 20) for _ in range(len(valores))]

            # Atualizar os valores do gráfico de barras
            for bar, novo_valor in zip(bar_plot, novos_valores):
                bar.set_width(novo_valor)

            # Atualizar o gráfico
            plt.draw()
            plt.pause(1)  # Pausa por 1 segundo

        # Fechar a janela ao interromper o programa
        plt.close()
