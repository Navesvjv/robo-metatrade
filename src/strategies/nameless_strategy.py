import env
import json
import MetaTrader5 as mt5
from src.config.check import Checks
from src.config.orders import Orders


class NamelessStrategy:
    def __init__(self):
        self.check = Checks()
        self.orders = Orders()

    def handler(self):
        if self.check.canOperate():
            if mt5.market_book_add(env.symbol):
                items = mt5.market_book_get(env.symbol)
                if items:
                    items = json.loads(items)
                    items_sell, items_buy = self.getItemsByType(items)

                    sumSell = self.sumVolume(items_sell)
                    sumBuy = self.sumVolume(items_buy)

                    percBuy, percSell = self.getPercentages(sumBuy, sumSell)
                    if percBuy > 70:
                        self.orders.openMarketBuy()
                    elif percSell > 70:
                        self.orders.openMarketSell()

    def getPercentages(self, sumBuy, sumSell):
        total = sumBuy + sumSell
        return (sumBuy / total), (sumSell / total)

    def getItemsByType(self, items):
        items_sell = []
        items_buy = []

        for it in items:
            if it["type"] == 1:
                items_sell.append(it)

            elif it["type"] == 2:
                items_buy.append(it)

        items_sell = sorted(items_sell, key=lambda x: x["price"])
        items_buy = sorted(items_buy, key=lambda x: x["price"], reverse=True)

        return items_sell, items_buy

    def sumVolume(self, items):
        soma = 0
        multiplicador = 1

        for it in items:
            soma = soma + (it["volume"] * multiplicador)
            multiplicador += 0.2

        return soma
