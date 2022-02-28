import yfinance as yf
import pandas as pd
import numpy as np


class Fin():
    ''' Class to download data from yfinance'''

    def __init__(self, ticker):
        self.ticker = ticker
        self.get_data()

    def __str__(self):
        return f"{self.ticker} is required"

    def get_data(self):
        ''' Imports the data '''
        # raw = yf.download(self.ticker, period="5y")
        raw = yf.download(self.ticker, period="7mo", interval="1h")
        # raw = yf.download(self.ticker, period="60d", interval="15m")
        # raw = yf.download(self.ticker, period="max", interval="1d")
        raw.rename(columns={'Close': "price"}, inplace=True)
        raw["returns"] = np.log(raw.price.div(raw.price.shift(1)))
        raw['log_returns'] = np.log(
            raw.price/raw.price.shift(1))  # daily log returns
        self.data = raw
        return self.data
