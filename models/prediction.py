from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
import json
import yfinance as yf
import plotly.graph_objects as go
import plotly
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.switch_backend('Agg')


class Prediction():
    ''' Class to download data from yfinance'''

    def __init__(self, ticker):
        self.ticker = ticker
        self.get_data()

    def __str__(self):
        return f"{self.ticker} is required"

    def get_data(self):
        ''' Imports the data '''
        raw = yf.download(self.ticker, period="max", interval="1d")
        self.data = raw
        return self.data

    def prediction_plot(self):

        data = self.data
        data.reset_index(inplace=True)
        df = data[["Date", "Open"]]
        new_names = {
            "Date": "ds",
            "Open": "y",
        }

        df.rename(columns=new_names, inplace=True)
        print('Fiting the model')
        m = Prophet(
            seasonality_mode="multiplicative"
        )
        m.fit(df)
        future = m.make_future_dataframe(periods=365)
        forecast = m.predict(future)
        fig = plot_plotly(m, forecast)
        graphJSON = json.dumps(fig,
                               cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON
