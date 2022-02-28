# import yfinance as yf
# import pandas as pd
# import numpy as np
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json
from .main import Fin


class BoilingerBand(Fin):
    def __init__(self, ticker, SMA=30, dev=2):
        super().__init__(ticker)
        self.ticker = ticker
        self.SMA = SMA
        self.dev = dev
        self.prepare_data()

    def __str__(self):
        return f"{self.ticker} {self.SMA} - default is set to 30 {self.dev} default is set to 2, is required"

    def __repr__(self):
        rep = "BoilingerBand class(ticker = {}, SMA = {}, dev = {})"
        return rep.format(self.ticker, self.SMA, self.dev)

    def prepare_data(self):
        '''Prepares the data for strategy backtesting (strategy-specific).
        '''
        data = self.data.copy()
        data["SMA"] = data["price"].rolling(self.SMA).mean()
        data["Lower"] = data["SMA"] - \
            data["price"].rolling(self.SMA).std() * self.dev
        data["Upper"] = data["SMA"] + \
            data["price"].rolling(self.SMA).std() * self.dev
        self.data = data

    def create_bb_plot(self):

        df = self.data
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            vertical_spacing=0.1, row_width=[0.2, 0.7])
        # ----------------
        # Candlestick Plot
        fig.add_trace(go.Candlestick(x=df.index,
                                     open=df['Open'],
                                     high=df['High'],
                                     low=df['Low'],
                                     close=df['price'], showlegend=False,
                                     name='candlestick'),
                      row=1, col=1)

        # Moving Average
        fig.add_trace(go.Scatter(x=df.index,
                                 y=df['SMA'],
                                 line_color='black',
                                 name='sma'),
                      row=1, col=1)

        # Upper Bound
        fig.add_trace(go.Scatter(x=df.index,
                                 y=df['Upper'],
                                 line_color='gray',
                                 line={'dash': 'dash'},
                                 name='upper band',
                                 opacity=0.5),
                      row=1, col=1)

        # Lower Bound fill in between with parameter 'fill': 'tonexty'
        fig.add_trace(go.Scatter(x=df.index,
                                 y=df['Lower'],
                                 line_color='gray',
                                 line={'dash': 'dash'},
                                 fill='tonexty',
                                 name='lower band',
                                 opacity=0.5),
                      row=1, col=1)

        fig.update_layout(
            autosize=False,
            width=1200,
            height=800,
        )

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON
