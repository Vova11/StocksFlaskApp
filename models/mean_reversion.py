from .main import Fin
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
from itertools import product
import pandas as pd
import numpy as np
import json


class MeanRevBacktester(Fin):
    ''' Class for the vectorized backtesting of Bollinger Bands-based trading strategies.
    '''

    def __init__(self, ticker, SMA=30, dev=2):
        '''
        Parameters
        ----------
        symbol: str
            ticker symbol (instrument) to be backtested
        SMA: int
            moving window in bars (e.g. days) for SMA
        dev: int
            distance for Lower/Upper Bands in Standard Deviation units
        start: str
            start date for data import
        end: str
            end date for data import
        tc: float
            proportional transaction/trading costs per trade
        '''
        super().__init__(ticker)
        self.ticker = ticker
        self.SMA = SMA
        self.dev = dev
        # self.tc = tc
        self.results = None
        self.prepare_data()

    def __repr__(self):
        rep = "MeanRevBacktester(symbol = {}, SMA = {}, dev = {})"
        return rep.format(self.symbol, self.SMA, self.dev)

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

    def plot_bollinger_bands(self):
        df = self.data
        fig = make_subplots(rows=2, cols=1,
                            vertical_spacing=0.2, row_width=[0.2, 0.7])
        # ----------------

        # Price
        fig.add_trace(go.Scatter(x=df.index,
                                 y=df['price'],
                                 line_color='black',
                                 name='sma'),
                      row=1, col=1)

        # SMA
        fig.add_trace(go.Scatter(x=df.index,
                                 y=df['SMA'],
                                 line_color='gray',
                                 line={'dash': 'dash'},
                                 name='upper band',
                                 opacity=0.5),
                      row=1, col=1)

        # Lower
        fig.add_trace(go.Scatter(x=df.index,
                                 y=df['Lower'],
                                 name='Lower band',
                                 opacity=0.5),
                      row=1, col=1)

        # Upper
        fig.add_trace(go.Scatter(x=df.index,
                                 y=df['Upper'],
                                 line_color='gray',
                                 name='Upper band',
                                 opacity=0.5),
                      row=1, col=1)

        fig.update_layout(
            autosize=False,
            width=1200,
            height=800,
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label="1m",
                             step="month",
                             stepmode="backward"),
                        dict(count=6,
                             label="6m",
                             step="month",
                             stepmode="backward"),
                        dict(count=1,
                             label="YTD",
                             step="year",
                             stepmode="todate"),
                        dict(count=1,
                             label="1y",
                             step="year",
                             stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

    def plot_bb_hold_sell(self):
        df = self.results
        data = df[['price', 'Lower', 'Upper', 'SMA', 'position']]

        data = [
            go.Scatter(x=data.index, y=data.price, name='Price'),
            go.Scatter(x=data.index, y=data.Upper, name='Upper'),
            go.Scatter(x=data.index, y=data.Lower, name='Lower'),
            go.Scatter(x=data.index, y=data.position, name='Position',
                       yaxis='y2')  # binding to the second y axis
        ]

        # settings for the new y axis
        y2 = go.YAxis(overlaying='y', side='right')
        # adding the second y axis
        layout = go.Layout(yaxis2=y2)
        fig = go.Figure(data=data, layout=go.Layout(
            autosize=False,
            width=1200,
            height=800,
            yaxis2=y2,
            xaxis=dict(
                rangeslider=dict(
                    visible=True
                )
            ))
        )
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

    def set_parameters(self, SMA=None, dev=None):
        ''' Updates parameters (SMA, dev) and the prepared dataset.
        '''
        if SMA is not None:
            self.SMA = SMA
            self.data["SMA"] = self.data["price"].rolling(self.SMA).mean()
            self.data["Lower"] = self.data["SMA"] - \
                self.data["price"].rolling(self.SMA).std() * self.dev
            self.data["Upper"] = self.data["SMA"] + \
                self.data["price"].rolling(self.SMA).std() * self.dev

        if dev is not None:
            self.dev = dev
            self.data["Lower"] = self.data["SMA"] - \
                self.data["price"].rolling(self.SMA).std() * self.dev
            self.data["Upper"] = self.data["SMA"] + \
                self.data["price"].rolling(self.SMA).std() * self.dev

    def test_strategy(self):
        ''' Backtests the Bollinger Bands-based trading strategy.
        '''
        data = self.data.copy().dropna()
        data["distance"] = data.price - data.SMA
        data["position"] = np.where(data.price < data.Lower, 1, np.nan)
        data["position"] = np.where(
            data.price > data.Upper, -1, data["position"])
        data["position"] = np.where(
            data.distance * data.distance.shift(1) < 0, 0, data["position"])
        data["position"] = data.position.ffill().fillna(0)
        data["strategy"] = data.position.shift(1) * data["returns"]
        data.dropna(inplace=True)

        # determine the number of trades in each bar
        data["trades"] = data.position.diff().fillna(0).abs()

        # subtract transaction/trading costs from pre-cost return
        data.strategy = data.strategy - data.trades * 0.00007
        # print(data['trades'])
        # data['strategy'] = data['strategy'] - data['trades']

        data["creturns"] = data["returns"].cumsum().apply(np.exp)
        data["cstrategy"] = data["strategy"].cumsum().apply(np.exp)
        self.results = data

        # absolute performance of the strategy
        perf = data["cstrategy"].iloc[-1]
        # out-/underperformance of strategy
        outperf = perf - data["creturns"].iloc[-1]

        return round(perf, 6), round(outperf, 6)

    def plot_results(self):
        ''' Plots the performance of the trading strategy and compares to "buy and hold".
        '''
        df = self.results[["creturns", "cstrategy"]]
        title = "Some title"
        fig = px.line(df, title=title)
        fig.update_layout(
            autosize=False,
            width=1200,
            height=800,
        )

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

    def optimize_parameters(self, SMA_range, dev_range):
        ''' Finds the optimal strategy (global maximum) given the Bollinger Bands parameter ranges.

        Parameters
        ----------
        SMA_range, dev_range: tuple
            tuples of the form (start, end, step size)
        '''

        combinations = list(product(range(*SMA_range), range(*dev_range)))

        # test all combinations
        results = []
        for comb in combinations:
            self.set_parameters(comb[0], comb[1])
            results.append(self.test_strategy()[0])

        best_perf = np.max(results)  # best performance
        opt = combinations[np.argmax(results)]  # optimal parameters

        # run/set the optimal strategy
        self.set_parameters(opt[0], opt[1])
        self.test_strategy()

        # create a df with many results
        many_results = pd.DataFrame(
            data=combinations, columns=["SMA", "dev"])
        many_results["performance"] = results
        self.results_overview = many_results

        return opt, best_perf
