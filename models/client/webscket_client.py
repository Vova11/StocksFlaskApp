import cbpro
import time
import pandas as pd
import numpy as np
import json


class TextWebSocketClient(cbpro.WebsocketClient):
    def on_open(self):
        self.url = 'wss://ws-feed-public.sandbox.exchange.coinbase.com'
        self.message_count = 0

    def on_message(self, msg):
        self.message_count += 1
        msg_type = msg.get('type', None)
        print(msg_type)
        if msg_type == 'ticker':
            time_val = msg.get('time', ('-'*27))
            price_val = msg.get('price', None)
            price_val = float(price_val) if price_val is not None else 'None'
            product_id = msg.get('product_id', None)

            df = pd.DataFrame(
                msg, columns=[msg['product_id'], msg['price']], index=[0])

            print(df)
            # df = pd.DataFrame(msg, columns=['product_id', 'price'])
            # df = df.set_index('time')
            # print(df)
            # print(pd.DataFrame.from_dict(msg))
            # print(
            #     f"{time_val:30} {price_val:.3f} {product_id}\tchanel type: {msg_type}")

    def on_close(self):
        print(
            f"<-- Websocket connection closed -->\n\tTotal messages: {self.message_count}")


stream = TextWebSocketClient(products=['BTC-USD'], channels=['ticker'])
stream.start()
# time.sleep(20)
# stream.close()
