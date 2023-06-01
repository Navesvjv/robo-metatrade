import random
import matplotlib.pyplot as plt


class VolumeChart:
    def plot():
        categorias = ["Compra", "Venda"]
        valores = [10, 15]

        # Configurar o gráfico inicial
        fig, ax = plt.subplots()
        bar_plot = ax.bar(categorias, valores)

        # Definir as propriedades do gráfico
        plt.xlabel("Categorias")
        plt.ylabel("Valores")
        plt.title("Gráfico de Barras Vertical")

        # Atualizar os valores em tempo real
        while True:
            # Gerar novos valores aleatórios
            novos_valores = [random.randint(5, 20) for _ in range(len(valores))]

            # Atualizar os valores do gráfico de barras
            for bar, novo_valor in zip(bar_plot, novos_valores):
                bar.set_height(novo_valor)

            # Atualizar o gráfico
            plt.draw()
            plt.pause(1)  # Pausa por 1 segundo

        # Fechar a janela ao interromper o programa
        plt.close()
