from .main import Fin
import plotly
import plotly.graph_objs as go
import plotly.express as px
import json

import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
plt.style.use('fivethirtyeight')


class Fib(Fin):

    def plot_fib(self):
        # Calculate the max and min close price
        df = self.data
        maximum_price = df['price'].max()
        minimum_price = df['price'].min()
        difference = maximum_price - minimum_price  # Get the difference
        first_level = maximum_price - difference * 0.236
        second_level = maximum_price - difference * 0.382
        third_level = maximum_price - difference * 0.5
        fourth_level = maximum_price - difference * 0.618
        # Print the price at each level
        print("Level Percentage\t", "Price ($)")
        print("00.0%\t\t", maximum_price)
        print("23.6%\t\t", first_level)
        print("38.2%\t\t", second_level)
        print("50.0%\t\t", third_level)
        print("61.8%\t\t", fourth_level)
        print("100.0%\t\t", minimum_price)

        new_df = df
        fig = go.Figure()

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            vertical_spacing=0.1, row_width=[0.2, 0.7])
        # ----------------
        # Candlestick Plot
        fig.add_trace(go.Candlestick(x=df.index,
                                     open=df['Open'],
                                     high=df['High'],
                                     low=df['Low'],
                                     close=df['price'], showlegend=True,
                                     name='candlestick'),
                      row=1, col=1)

        # Moving Average
        fig.add_hline(maximum_price, line_dash="dash", line_color="red", annotation_text="maximum_price",
                      annotation_position="bottom left")
        fig.add_hline(first_level, line_dash="dash", line_color="orange", annotation_text="first_level",
                      annotation_position="bottom left")
        fig.add_hline(second_level, line_dash="dash", line_color="yellow", annotation_text="second_level",
                      annotation_position="bottom left")
        fig.add_hline(third_level, line_dash="dash", line_color="green", annotation_text="third_level",
                      annotation_position="bottom left")
        fig.add_hline(fourth_level, line_dash="dash", line_color="blue", annotation_text="fourth_level",
                      annotation_position="bottom left")
        fig.add_hline(minimum_price, line_dash="dash", line_color="purple", annotation_text="minimum_price",
                      annotation_position="bottom left")

        fig.update_layout(
            autosize=False,
            width=1200,
            height=800,
            xaxis=dict(
                rangeselector=dict(
                    buttons=list(
                        [
                            dict(count=1, label="1m", step="month",
                                 stepmode="backward"),
                            dict(count=6, label="6m", step="month",
                                 stepmode="backward"),
                            dict(count=1, label="YTD",
                                 step="year", stepmode="todate"),
                            dict(count=1, label="1y", step="year",
                                 stepmode="backward"),
                            dict(step="all"),
                        ]
                    )
                ),
                rangeslider=dict(visible=True),
                type="date",
            )
        )

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON

    def plot_fib_two(self):
        df = self.data
        highest_swing = -1
        lowest_swing = -1
        for i in range(1, df.shape[0]-1):
            if df['High'][i] > df['High'][i-1] and df['High'][i] > df['High'][i+1] and (highest_swing == -1 or df['High'][i] > df['High'][highest_swing]):
                highest_swing = i

            if df['Low'][i] < df['Low'][i-1] and df['Low'][i] < df['Low'][i+1] and (lowest_swing == -1 or df['Low'][i] < df['Low'][lowest_swing]):
                lowest_swing = i
        ratios = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
        colors = ["black", "red", "green", "blue", "cyan", "magenta", "yellow"]
        levels = []
        max_level = df['High'][highest_swing]
        min_level = df['Low'][lowest_swing]

        for ratio in ratios:
            if highest_swing > lowest_swing:  # Uptrend
                levels.append(max_level - (max_level-min_level)*ratio)
            else:  # Downtrend
                levels.append(min_level + (max_level-min_level)*ratio)

        title = "Some title"
        fig = px.line(df, x=df.index,
                      y=df['price'], title='Fabionachi retracement levels')
        start_date = df.index[min(highest_swing, lowest_swing)]
        end_date = df.index[max(highest_swing, lowest_swing)]
        # ig.add_hline(y=minimum_price, line_dash="dash", line_color="purple")
        for i in range(len(levels)):
            fig.add_hline(levels[i], line_dash="dash", line_color=colors[i])

        fig.update_layout(
            autosize=False,
            width=1200,
            height=800,
            xaxis=dict(
                rangeselector=dict(
                    buttons=list(
                        [
                            dict(count=1, label="1m", step="month",
                                 stepmode="backward"),
                            dict(count=6, label="6m", step="month",
                                 stepmode="backward"),
                            dict(count=1, label="YTD",
                                 step="year", stepmode="todate"),
                            dict(count=1, label="1y", step="year",
                                 stepmode="backward"),
                            dict(step="all"),
                        ]
                    )
                ),
                rangeslider=dict(visible=True),
                type="date",
            )
        )

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON
