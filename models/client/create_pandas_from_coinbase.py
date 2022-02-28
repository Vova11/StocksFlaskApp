import requests
import pandas as pd
import time
from datetime import datetime, timedelta


url = "https://api.pro.coinbase.com"
ticker = 'BTC-USD'
barSize = "900"
timeEnd = datetime.now()

delta = timedelta(seconds=int(barSize))
timeStart = timeEnd - (300*delta)
timeStart = timeStart.isoformat()
timeEnd = timeEnd.isoformat()
parameters = {
    'start': timeStart,
    'end': timeEnd,
    'granularity': barSize
}
data = requests.get(f"{url}/products/{ticker}/candles",
                    params=parameters,
                    headers={"content-type": "applications/json"})
df = pd.DataFrame(data.json(),
                  columns=['time', 'low', 'high', 'open', 'close', 'volume'])
df["date"] = pd.to_datetime(df["time"], unit='s')
df = df[["date", "open", "high", "low", "close"]]
df.set_index("date", inplace=True)
df = df.resample("15 min").agg({
    "open": "first",
    "high": "max",
    "low": "min",
    "close": "last"
})
df.reset_index(inplace=True)
df.dropna()
print(df)
