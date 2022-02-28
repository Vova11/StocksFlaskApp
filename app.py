from models.bb import BoilingerBand
from models.financial import FI
from models.sma_strategy import SMABacktester
from models.fib import Fib
from models.prediction import Prediction
from models.mean_reversion import MeanRevBacktester
# from models.regression import Regression
from models.mlbbacktester import MLBacktester
from flask import Flask, redirect, url_for, render_template, request, session
app = Flask(__name__)


app.secret_key = 'BAD_SECRET_KEY'


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        entry_content = request.form.get("ticker")
        if entry_content:
            session['ticker'] = entry_content
            data = BoilingerBand(entry_content)
            bar = data.create_bb_plot()
            kwargs = {
                'plot': bar,
                'ticker': session['ticker'],
                'dev': data.dev,
                'SMA': data.SMA
            }
            return render_template('index.html', **kwargs)
    return render_template('index.html')


@app.route('/fib')
def fib():
    if session['ticker']:
        data = Fib(session['ticker'])
        plot_fib = data.plot_fib()
        plot_fib_two = data.plot_fib_two()
        kwargs = {
            'fib': plot_fib,
            'fib_two': plot_fib_two
        }
        return render_template('fib.html', **kwargs)
    return render_template('fib.html')


@app.route('/financial')
def financial():
    if session['ticker']:
        data = FI(session['ticker'])
        plot_price = data.plot_prices()
        plot_returns = data.plot_returns()
        mean_return_d = data.mean_return()
        mean_return_m = data.mean_return('m')
        mean_return_y = data.mean_return('y')
        std_returns_d = data.std_returns()
        std_returns_m = data.std_returns('m')
        std_returns_y = data.std_returns('y')
        annualized_perf = data.annualized_perf()
        kwargs = {
            'ticker': data.ticker,
            'mean_return_d': mean_return_d,
            'mean_return_m': mean_return_m,
            'mean_return_y': mean_return_y,
            'std_returns_d': std_returns_d,
            'std_returns_m': std_returns_m,
            'std_returns_y': std_returns_y,
            'annualized_perf': annualized_perf,
            'plot_price': plot_price,
            'plot_returns': plot_returns
        }
        return render_template('financial.html', **kwargs)
    return render_template('financial.html')


@app.route('/sma_strategy')
def sma_strategy():
    if session['ticker']:
        data = SMABacktester(session['ticker'])
        test_strategy = data.test_strategy()
        print(test_strategy)
        plot_results = data.plot_results()
        new_graph = data.optimize_parameters((10, 50, 1), (100, 252, 1))
        print(new_graph)
        new_plot_result = data.plot_results()
        optimized_test_strategy = data.test_strategy()
        print(optimized_test_strategy)
        combinations = data.results_overview.index[-1]
        kwargs = {
            'test_strategy': test_strategy,
            'optimized_test_strategy': optimized_test_strategy,
            'plot_results': plot_results,
            'new_plot_result': new_plot_result,
            'combinations': combinations,
            'ticker': session['ticker'],
            'SMA_S': data.SMA_S,
            'SMA_L': data.SMA_L,

        }
    return render_template('sma_strategy.html', **kwargs)


@app.route('/prediciton')
def prediction():
    if session['ticker']:
        data = Prediction(session['ticker'])
        prediction_plot = data.prediction_plot()
        kwargs = {
            'prediction_plot': prediction_plot,

        }
    return render_template('prediction.html', **kwargs)


@app.route('/mean_reversion_bb')
def mean_reversion_bb():
    if session['ticker']:
        data = MeanRevBacktester(session['ticker'])
        test_strategy = data.test_strategy()
        plot_bollinger_bands = data.plot_bollinger_bands()
        trades_old = data.results['trades'].value_counts()
        test_strategy = data.test_strategy()
        optimize = data.optimize_parameters((25, 100, 1), (1, 5, 1))
        new_test_strategy = data.test_strategy()
        plot_results = data.plot_results()
        trades_new = data.results['trades'].value_counts()
        position = data.results.position[-1]
        plot_bb_hold_sell = data.plot_bb_hold_sell()
        kwargs = {
            'plot_bollinger_bands': plot_bollinger_bands,
            'position': position,
            'plot_bb_hold_sell': plot_bb_hold_sell,
            'test_strategy': test_strategy,
            'trades_new': trades_new,
            'trades_old': trades_old,
            'new_test_strategy': new_test_strategy,
            'plot_results': plot_results
        }
    return render_template('mean_reversion.html', **kwargs)


# @app.route('/ml_regression')
# def regression():
    # if session['ticker']:
    #     data = Regression(session['ticker'])
    #     plot_price = data.plot_price()
    #     plot_scater = data.plot_scater()
    #     sickit = data.sickit()
    #     returns = data.returns()
    #     forecast_prediciton = data.forecast_prediciton()
    #     new_prediciton = data.new_prediciton()
    #     back_testing = data.back_testing()
    #     counts = data.trades.value_counts()
    #     kwargs = {
    #         'plot_price': plot_price,
    #         'plot_scater': plot_scater,
    #         'sickit': sickit,
    #         'returns': returns,
    #         'forecast_prediciton': forecast_prediciton,
    #         'new_prediciton': new_prediciton,
    #         'back_testing': back_testing,
    #         'counts': counts
    #     }
    # return render_template('regression.html', **kwargs)


@app.route('/mlbbacktester')
def mlbbacktester():
    if session['ticker']:
        data = MLBacktester(session['ticker'])
        test_strategy = data.test_strategy(train_ratio=0.7, lags=17)
        plot_results = data.plot_results()
        trades_and_hitratio = data.trades_and_hitratio()
        kwargs = {
            'test_strategy': test_strategy,
            'plot_results': plot_results,
            'trades_and_hitratio': trades_and_hitratio

        }

    return render_template('mlbbacktester.html', **kwargs)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
