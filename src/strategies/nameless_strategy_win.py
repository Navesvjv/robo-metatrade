import json
import time
import MetaTrader5 as mt5
from src.config.check import Checks
from src.config.orders.orders_win import OrdersWIN
from src.repositories.trades_win_repository import TradesWINRepository
from src.config.symbols import SymbolEnum, getSymbol


class NamelessStrategyWIN:
    def __init__(self):
        self.check = Checks()
        self.symbol = getSymbol(SymbolEnum.WIN)
        self.ordersWin = OrdersWIN(self.symbol)
        self.tradesWinRepository = TradesWINRepository()

    def execute(self):
        while True:
            can = self.check.canTrade(self.symbol)
            if can == "stop":
                break
            elif can == "continue":
                self.getMarketBook()

            time.sleep(10)

    def getMarketBook(self):
        if mt5.market_book_add(self.symbol):
            items = mt5.market_book_get(self.symbol)
            if items:
                items = json.loads(items)
                items_sell, items_buy = self.getItemsByType(items)

                sumSell = self.sumVolume(items_sell)
                sumBuy = self.sumVolume(items_buy)

                percBuy, percSell = self.getPercentages(sumBuy, sumSell)
                lastId = self.tradesWinRepository.getLastId()
                magic = lastId + 1 if lastId else 1000000

                order = None
                if percSell > 65:
                    order = self.ordersWin.openMarketSell(magic)
                elif percBuy > 65:
                    order = self.ordersWin.openMarketBuy(magic)

                self.tradesWinRepository.insert(order, percSell, percBuy)

    def getPercentages(self, sumBuy, sumSell):
        total = sumBuy + sumSell
        return (sumBuy / total * 100), (sumSell / total * 100)

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
