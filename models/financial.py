from .main import Fin
import plotly
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import json


class FI(Fin):  # Financial Instrument
    ''' Class to analize Financial instruments'''

    def __repr__(self):
        return """Financial Instrument (FI) """

    def __str__(self):
        return "This Class returns Mean Return, Risk and Annual Return/Risk "

    def mean_return(self, freq=None):
        '''calculates mean return
        '''
        if freq is None:
            return self.data.log_returns.mean()
        else:
            resampled_price = self.data.price.resample(freq).last()
            resampled_returns = np.log(
                resampled_price / resampled_price.shift(1))
            return resampled_returns.mean()

    def std_returns(self, freq=None):
        '''calculates the standard deviation of returns (risk)
        '''
        if freq is None:
            return self.data.log_returns.std()
        else:
            resampled_price = self.data.price.resample(freq).last()
            resampled_returns = np.log(
                resampled_price / resampled_price.shift(1))
            return resampled_returns.std()

    def annualized_perf(self):
        '''calculates annulized return and risk
         d'''
        mean_return = round(self.data.log_returns.mean() *
                            252, 5)  # need to be fixed for crypto
        # need to be fixed for crypto
        risk = round(self.data.log_returns.std() * np.sqrt(252), 5)
        return mean_return, risk

    def plot_prices(self):
        df = self.data
        fig = px.line(x=df.index, y=df.price)
        fig.update_layout(
            autosize=False,
            width=1200,
            height=800,
        )
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

    def plot_returns(self):
        df = self.data
        fig = px.histogram(
            df.log_returns,
            x=df.log_returns, y=df.price, nbins=int(np.sqrt(len(self.data)))
        )
        fig.update_layout(
            autosize=False,
            width=1200,
            height=800,
        )
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON
