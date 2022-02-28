import cbpro
import time
import datetime
public_client = cbpro.PublicClient()

current_value_LTC = 0
current_value_ETH = 0
current_value_BTC = 0
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
appendFile = open('statistics.log', 'a')
appendFile.write('\n\ncurrent_price.py started at: ')
appendFile.write(st)
appendFile.write('\n')
appendFile.close()

while True:

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    # Read price:

    # LTC-USD
    try:
        current_value_LTC = public_client.get_product_ticker(
            product_id='LTC-USD')
    except:
        print('\n\nERROR added to CurrentPrice.error.log')
        appendFile = open('CurrentPrice.error.log', 'a')  # a for append
        appendFile.write('\n')
        appendFile.write(st)
        appendFile.write(' - Error while getting current_value_LTC')
        appendFile.close()
        pass
    try:
        current_value_LTC = str(current_value_LTC['price'])
    except:
        print('\n\nERROR added to CurrentPrice.error.log')
        appendFile = open('CurrentPrice.error.log', 'a')  # a for append
        appendFile.write('\n')
        appendFile.write(st)
        appendFile.write(' - Error while setting current_value_LTC to str')
        appendFile.write('\n')
        appendFile.close()
        pass

    # ETH-USD
    try:
        current_value_ETH = public_client.get_product_ticker(
            product_id='ETH-USD')
    except:
        print('\n\nERROR added to CurrentPrice.error.log')
        appendFile = open('CurrentPrice.error.log', 'a')  # a for append
        appendFile.write('\n')
        appendFile.write(st)
        appendFile.write(' - Error while getting current_value_ETH')
        appendFile.write('\n')
        appendFile.close()
    try:
        current_value_ETH = str(current_value_ETH['price'])
    except:
        print('\n\nERROR added to CurrentPrice.error.log')
        appendFile = open('CurrentPrice.error.log', 'a')  # a for append
        appendFile.write('\n')
        appendFile.write(st)
        appendFile.write(' - Error while setting current_value_LTC to str')
        appendFile.write('\n')
        appendFile.close()
        pass

    # BTC-USD
    try:
        current_value_BTC = public_client.get_product_ticker(
            product_id='BTC-USD')
    except:
        print('\n\nERROR added to CurrentPrice.error.log')
        appendFile = open('CurrentPrice.error.log', 'a')  # a for append
        appendFile.write('\n')
        appendFile.write(st)
        appendFile.write(' - Error while getting current_value_BTC')
        appendFile.write('\n')
        appendFile.close()
    try:
        current_value_BTC = str(current_value_BTC['price'])
    except:
        print('\n\nERROR added to CurrentPrice.error.log')
        appendFile = open('CurrentPrice.error.log', 'a')  # a for append
        appendFile.write('\n')
        appendFile.write(st)
        appendFile.write(' - Error while setting current_value_BTC to str')
        appendFile.write('\n')
        appendFile.close()
        pass

    # Write price:
    # LTC-USD
    appendFile = open('LTC-USD.txt', 'w')
    try:
        appendFile.write(current_value_LTC)
    except:
        print('ERROR writing the price to file - possible site down')
        print('Check site status at: https://status.gdax.com/')
        appendFile.write(
            'ERROR writing the price to file - possible site down')
    appendFile.close()
    # ETH-USD
    appendFile = open('ETH-USD.txt', 'w')
    try:
        appendFile.write(current_value_ETH)
    except:
        print('ERROR writing the price to file - possible site down')
        print('Check site status at: https://status.gdax.com/')
        appendFile.write(
            'ERROR writing the price to file - possible site down')
    appendFile.close()
    # BTC-USD
    appendFile = open('BTC-USD.txt', 'w')
    try:
        appendFile.write(current_value_BTC)
    except:
        print('ERROR writing the price to file - possible site down')
        print('Check site status at: https://status.gdax.com/')
        appendFile.write(
            'ERROR writing the price to file - possible site down')
    appendFile.close()

    # Print:
    print()
    print()
    print()
    print(st)
    print()
    print('----------')
    print('LTC-USD:')
    print('Current value:', current_value_LTC)
    print('----------')
    print()
    print('----------')
    print('ETH-USD:')
    print('Current value:', current_value_ETH)
    print('----------')
    print()
    print('----------')
    print('BTC-USD:')
    print('Current value:', current_value_BTC)
    print('----------')

    time.sleep(1)


# import json

# import pandas as pd
# import websocket
# import time

# df = pd.DataFrame(columns=['price'])


# def on_message(ws, message):
#     msg = json.loads(message)

#     data = pd.DataFrame(
#         {'price': msg['price'], 'date': msg['time']}, index=[0])
#     data["date"] = pd.to_datetime(msg['time']).strftime('%Y-%m-%d %H:%M:%S')
#     data.set_index("date", inplace=True)
#     print(data)


# def on_error(ws, error):
#     print(error)


# def on_close(ws):
#     print("### closed ###")


# def on_open(ws):
#     print("opened connection")
#     subscribe_message = {
#         'type': 'subscribe',
#         'channels': [
#             {
#                 "name": "ticker",
#                 "product_ids": [
#                     "BTC-USD"
#                 ]
#             }
#         ]
#     }
#     ws.send(json.dumps(subscribe_message))


# if __name__ == "__main__":
#     # wss://ws-feed.pro.coinbase.com
#     # ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)

#     ws = websocket.WebSocketApp("wss://ws-feed-public.sandbox.exchange.coinbase.com",
#                                 on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
#     ws.run_forever()


# import json

# import pandas as pd
# import websocket
# import time

# df = pd.DataFrame(columns=['price'])


# def on_message(ws, message):
#     msg = json.loads(message)

#     data = pd.DataFrame(
#         {'price': msg['price'], 'date': msg['time']}, index=[0])
#     data["date"] = pd.to_datetime(msg['time']).strftime('%Y-%m-%d %H:%M:%S')
#     data.set_index("date", inplace=True)
#     print(data)


# def on_error(ws, error):
#     print(error)


# def on_close(ws):
#     print("### closed ###")


# def on_open(ws):
#     print("opened connection")
#     subscribe_message = {
#         'type': 'subscribe',
#         'channels': [
#             {
#                 "name": "ticker",
#                 "product_ids": [
#                     "BTC-USD"
#                 ]
#             }
#         ]
#     }
#     ws.send(json.dumps(subscribe_message))


# if __name__ == "__main__":
#     # wss://ws-feed.pro.coinbase.com
#     # ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)

#     ws = websocket.WebSocketApp("wss://ws-feed-public.sandbox.exchange.coinbase.com",
#                                 on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
#     ws.run_forever()
