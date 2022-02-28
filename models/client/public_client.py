import cbpro


class PublicClient():

    def __init__(self, ticker):
        self.ticker = ticker

    def result(self):
        pc = cbpro.PublicClient()
        result = pc.get_product_ticker(self.ticker)
        return result


# p = PublicClient('BTC-USD')
# data = p.result()
# print(data)
