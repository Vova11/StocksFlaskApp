import cbpro
import requests
import pandas as pd
import time
from datetime import datetime
c = cbpro.PublicClient()

# data = pd.DataFrame(c.get_products())
# print(data.tail().T)

# ticker = c.get_product_ticker(product_id='ADA-USD')
# print(ticker)

# ticker = requests.get(
#     'https://api.pro.coinbase.com/products/ADA-USD/ticker').json()
# print(ticker)


# historical = pd.DataFrame(c.get_product_historic_rates(product_id='ADA-USD'))
# historical.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
# historical['Date'] = pd.to_datetime(historical['Date'], unit='s')
# historical.set_index('Date', inplace=True)
# historical.sort_values(by='Date', ascending=True, inplace=True)
# print(historical)

# order_book = c.get_product_order_book('BTC-USD')
# print(order_book)

# trades = pd.DataFrame(requests.get(
#     'https://api.pro.coinbase.com/products/ETH-USD/trades').json())
# print(trades.tail())


# ws = cbpro.WebsocketClient(url="wss://ws-feed.pro.coinbase.com",
#                            products="ADA-USD",
#                            channels=["ticker"])

# ws.run_forever


class myWebsocketClient(cbpro.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com/"
        self.products = ["ETH-USDT"]
        self.channels = ["ticker"]
        self.message_count = 0

    def on_message(self, msg):
        self.message_count += 1
        if 'price' in msg and 'type' in msg:
            print("Message type:", msg["type"],
                  "\t@ {:.3f}".format(float(msg["price"])))

    def on_close(self):
        print("Closing")


wsClient = myWebsocketClient()
wsClient.start()
print(wsClient.url, wsClient.products, wsClient.channels)
while (wsClient.message_count < 50):
    print("\nmessage_count =", "{} \n".format(wsClient.message_count))
    time.sleep(1)
wsClient.close()
