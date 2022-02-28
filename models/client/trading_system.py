import cbpro
from dotenv import load_dotenv
import os
from auth_credentials import api_key, api_secret, api_passphrase, api_url
load_dotenv()

BUY = 'buy'
SELL = 'sell'


class TradingSystems:

    def __init__(self, cb_pro_client):
        self.client = cb_pro_client

    def trade(self, action, limitPrice, quantity):
        if action == BUY:
            response = self.client.buy(
                price=limitPrice,
                size=self.round(quantity * 0.99),
                order_type='limit',
                product_id='BTC-USD',
                overdraft_enabled=False
            )
        elif action == SELL:
            response = self.client.sell(
                price=limitPrice,
                size=self.round(quantity * 0.99),
                order_type='limit',
                product_id='BTC-USD',
                overdraft_enabled=False
            )

        print(response)

    def viewAccounts(self, accountCurrency):
        accounts = self.client.get_accounts()
        account = list(
            filter(lambda x: x['currency'] == accountCurrency, accounts))[0]
        return account

    def viewOrder(self, order_id):
        return self.client.get_order(order_id)

    def round(self, val):
        newval = int(val * 10000000)/10000000
        return newval

    def getCurrentPricefBitcoin(self):
        tick = self.client.get_product_ticker(product_id='BTC-USD')
        return tick['bid']


if __name__ == "__main__":
    auth_client = cbpro.AuthenticatedClient(
        api_key, api_secret, api_passphrase, api_url)

    tradingSystems = TradingSystems(auth_client)
    # print(tradingSystems.viewAccounts('USD')['balance'])
    current_price = tradingSystems.getCurrentPricefBitcoin()
    usd_balance = tradingSystems.viewAccounts('USD')['balance']
    print(usd_balance)
    tradingSystems.trade(SELL, float(current_price), float(
        usd_balance)/float(current_price))

    # lastOrderInfo = tradingSystems.viewOrder(
    #     'd51562c8-5ea8-4dad-b89d-79071ef26b1b')
    # print(lastOrderInfo)

 # print(tradingSystems.viewAccounts('BTC')['balance'])
# print(tradingSystems.viewAccounts('BTC')['balance'])
