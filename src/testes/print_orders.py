import env
import time
import MetaTrader5 as mt5


class PrintOrders:
    def getOrders(self):
        while True:
            tick = mt5.symbol_info_tick(env.symbol)._asdict()
            
            if mt5.market_book_add(env.symbol):
                items = mt5.market_book_get(env.symbol)
                if items:
                    sum_buy = 0
                    sum_sell = 0
                    for it in items:
                        print(it._asdict())
                        vol = it._asdict()
                        if vol["type"] == 1:
                            sum_sell += vol["volume"]
                        elif vol["type"] == 2:
                            sum_buy += vol["volume"]
                    
                    print(f"ASK: {tick['ask']} BID: {tick['bid']} VOL_BUY: {sum_buy} VOL_SELL: {sum_sell}")
                
                mt5.market_book_release(env.symbol)
            
            else:
                print(mt5.last_error())

            time.sleep(1)
