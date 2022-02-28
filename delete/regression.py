# from .main import Fin
# import plotly
# import plotly.graph_objs as go
# import plotly.express as px
# import pandas as pd
# import numpy as np
# import json
# from plotly.subplots import make_subplots
# from sklearn.linear_model import LinearRegression


# class Regression(Fin):
#     def __init__(self, ticker):
#         super().__init__(ticker)
#         self.ticker = ticker
#         self.add_extra_legs()
#         self.prepare_data()

#     def prepare_data(self):
#         raw = self.data
#         raw["lag1"] = raw.returns.shift(1)
#         data = raw.dropna(inplace=True)
#         return self.data

#     def plot_price(self):
#         df = self.data
#         fig = px.line(x=df.index, y=df.price)
#         fig.update_layout(
#             autosize=False,
#             width=1200,
#             height=800,
#         )
#         graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#         return graphJSON

#     def plot_scater(self):
#         df = self.data

#         fig = px.scatter(df, x=df["lag1"], y=df["returns"])
#         fig.update_layout(
#             autosize=False,
#             width=1200,
#             height=800,
#         )
#         graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#         return graphJSON

#     def sickit(self):
#         data = self.data
#         lm = LinearRegression(fit_intercept=True)
#         lm.fit(data.lag1.to_frame(), data.returns)
#         data["pred"] = lm.predict(data.lag1.to_frame())
#         # slope of the line
#         slope = lm.coef_
#         print(slope)
#         intercept = lm.intercept_
#         print(intercept)

#         fig = px.scatter(data, x=data.lag1, y=data.returns,
#                          title="A simple Linear Model to predict Financial Returns")

#         fig.add_trace(
#             go.Scatter(
#                 x=data.lag1,
#                 y=data["pred"],
#                 mode="lines",
#                 line=go.scatter.Line(color="red"),
#                 showlegend=False)
#         )

#         graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#         return graphJSON

#     def returns(self):
#         df = self.data
#         fig = make_subplots(rows=2, cols=1,
#                             vertical_spacing=0.2, row_width=[0.2, 0.7])
#         # ----------------

#         # Returns
#         fig.add_trace(go.Scatter(x=df.index,
#                                  y=df['returns'],
#                                  line_color='blue',
#                                  name='returns'),
#                       row=1, col=1)

#         # Prediction
#         fig.add_trace(go.Scatter(x=df.index,
#                                  y=df['pred'],
#                                  line_color='red',
#                                  name='prediction',
#                                  opacity=0.5),
#                       row=1, col=1)
#         fig.update_layout(
#             autosize=False,
#             width=1200,
#             height=800,
#         )
#         graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#         return graphJSON

#     def forecast_prediciton(self):
#         # forecasted return is positive +1 / negative is -1
#         data = self.data
#         data.pred = np.sign(data.pred)
#         corrcet_wrong_preditions = np.sign(data.returns * data.pred)
#         hits = np.sign(data.returns * data.pred).value_counts()
#         hit_ratio = hits[1.0] / sum(hits)
#         return data.pred[-1], hit_ratio

#     def add_extra_legs(self):
#         cols = []
#         raw = self.data
#         lags = 5
#         for lag in range(1, lags + 1):
#             col = "lag{}".format(lag)
#             raw[col] = raw.returns.shift(lag)
#             cols.append(col)
#         self.data = raw
#         return self.data

#     def new_prediciton(self):
#         data = self.data
#         lm = LinearRegression(fit_intercept=True)
#         lm.fit(data[['lag1', 'lag2', 'lag3', 'lag4', 'lag5']], data.returns)
#         print(lm.coef_)  # coeficiant in total 5
#         print(lm.intercept_)  # intercept
#         data["pred"] = lm.predict(
#             data[['lag1', 'lag2', 'lag3', 'lag4', 'lag5']].values)
#         data.pred = np.sign(data.pred)
#         print(data.pred.value_counts)
#         hits = np.sign(data.returns * data.pred).value_counts()
#         hit_ratio = hits[1.0] / sum(hits)
#         return hit_ratio

#     def back_testing(self):
#         data = self.data
#         data["strategy"] = data.pred * data.returns
#         data["creturns"] = data["returns"].cumsum().apply(np.exp)
#         data["cstrategy"] = data["strategy"].cumsum().apply(np.exp)
#         buy_or_sell = data.pred[-1]
#         print(buy_or_sell)
#         fig = make_subplots(rows=2, cols=1,
#                             vertical_spacing=0.2, row_width=[0.2, 0.7])
#         # ----------------

#         # Returns
#         fig.add_trace(go.Scatter(x=data.index,
#                                  y=data['creturns'],
#                                  line_color='blue',
#                                  name='returns'),
#                       row=1, col=1)

#         # Prediction
#         fig.add_trace(go.Scatter(x=data.index,
#                                  y=data['cstrategy'],
#                                  line_color='red',
#                                  name='cstrategy',
#                                  opacity=0.5),
#                       row=1, col=1)
#         fig.update_layout(
#             autosize=False,
#             width=1200,
#             height=800,
#         )

#         # data["trades"] = data.pred.diff().fillna(0).abs()
#         graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#         return graphJSON
