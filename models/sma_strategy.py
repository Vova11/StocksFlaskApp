from .main import Fin
import plotly
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
from itertools import product


class SMABacktester(Fin):

    def __str__(self):
        return ''' Class for the vectorized backtesting of SMA-based trading strategies.
    '''

    def __repr__(self):
        return "SMABacktester(ticker = {}, SMA_S = {} default 200, SMA_L = {} default 50)".format(self.ticker, self.SMA_S, self.SMA_L)

    def __init__(self, ticker, SMA_S=50, SMA_L=200):
        super().__init__(ticker)
        self.ticker = ticker
        self.clean_data()
        self.SMA_S = SMA_S
        self.SMA_L = SMA_L
        self.results = None
        self.prepare_data()

    def clean_data(self):
        raw = self.data.copy()
        data = raw.dropna()
        return data

    def prepare_data(self):
        '''Prepares the data for strategy backtesting (strategy-specific).
        '''
        raw = self.data.copy()
        raw["SMA_S"] = raw["price"].rolling(self.SMA_S).mean()  # add short SMA
        raw["SMA_L"] = raw["price"].rolling(self.SMA_L).mean()  # add Long SMA
        self.data = raw.dropna()
        return self.data

    def set_parameters(self, SMA_S=None, SMA_L=None):
        ''' Updates SMA parameters and the prepared dataset.
        '''
        if SMA_S is not None:
            self.SMA_S = SMA_S
            self.data["SMA_S"] = self.data["price"].rolling(self.SMA_S).mean()
        if SMA_L is not None:
            self.SMA_L = SMA_L
            self.data["SMA_L"] = self.data["price"].rolling(self.SMA_L).mean()

    def test_strategy(self):
        ''' Backtests the SMA-based trading strategy.
        '''
        data = self.data.copy().dropna()
        data["position"] = np.where(
            self.data["SMA_S"] > data["SMA_L"], 1, -1)
        data["strategy"] = data["position"].shift(
            1) * self.data["returns"]
        data.dropna(inplace=True)
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
        print(df)
        title = "{} | SMA_S = {} | SMA_L = {}".format(
            self.ticker, self.SMA_S, self.SMA_L)
        fig = px.line(df, title=title)
        fig.update_layout(
            autosize=False,
            width=1200,
            height=800,
        )

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

    def test_strategy(self):
        ''' Backtests the SMA-based trading strategy.
        '''
        data = self.data.copy().dropna()
        data["position"] = np.where(data["SMA_S"] > data["SMA_L"], 1, -1)
        data["strategy"] = data["position"].shift(1) * data["returns"]
        data.dropna(inplace=True)
        data["creturns"] = data["returns"].cumsum().apply(np.exp)
        data["cstrategy"] = data["strategy"].cumsum().apply(np.exp)
        self.results = data

        # absolute performance of the strategy
        perf = data["cstrategy"].iloc[-1]
        # out-/underperformance of strategy
        outperf = perf - data["creturns"].iloc[-1]
        return round(perf, 6), round(outperf, 6)

    def optimize_parameters(self, SMA_S_range, SMA_L_range):
        ''' Finds the optimal strategy (global maximum) given the SMA parameter ranges.

        Parameters
        ----------
        SMA_S_range, SMA_L_range: tuple
            tuples of the form (start, end, step size)
        '''

        combinations = list(product(range(*SMA_S_range), range(*SMA_L_range)))

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
            data=combinations, columns=["SMA_S", "SMA_L"])
        many_results["performance"] = results
        self.results_overview = many_results

        return opt, best_perf
