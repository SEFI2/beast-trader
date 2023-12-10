import backtrader as bt
import pandas_ta as ta
import ccxt

import pandas as pd
import math
import vectorbt as vbt

exchange = ccxt.bitmex({
    #'apiKey': "nQEbL79NBi7cN65VQXSCvmSo",
    #'secret': "R74OKyy8W-xJHmTL3DsGIno32EqLwhA9hRmXvYvLWZ8-I4Zc",
    'apiKey': '0y7QTbMmps5eWg-fmGS3uOC0',
    'secret': 'YWZOQMzCFchD4t05CxE0ptuIgcAblctmdxpH4GVlNKC1Yaxl',
})
exchange.set_sandbox_mode(True)

# Add data feed
# Replace 'data' with your DataFrame containing OHLCV data
bars = exchange.fetch_ohlcv('ETHUSDT', timeframe='1m', limit=900) # 15 hours
print(bars[-2])
print(bars[-1])
df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)

# Create the "Golden Cross" 
length = 7
multiplier = float(3.0)
sti = df.ta.supertrend()
#print(sti)
trend_dir = f"SUPERTd_{length}_{multiplier}"
buy = (sti[trend_dir] > 0) & (sti[trend_dir].shift() < 0)
sell = (sti[trend_dir].shift() > 0) & (sti[trend_dir] < 0)

#df["GC"] = df.ta.sma(50, append=True) > df.ta.sma(200, append=True)

# Create boolean Signals(TS_Entries, TS_Exits) for vectorbt
buy_signals = df.ta.tsignals(buy, asbool=True, append=True)
sell_signals = df.ta.tsignals(sell, asbool=True, append=True)

# Sanity Check (Ensure data exists)
print(buy)
print(buy_signals)

# Create the Signals Portfolio
pf = vbt.Portfolio.from_signals(
    df.close,
    entries=buy_signals.TS_Entries,
    exits=sell_signals.TS_Exits,
    freq="D",
    init_cash=100_000,
    fees=0.0025,
    slippage=0.0025
)

# Print Portfolio Stats and Return Stats
print(pf.stats())
print(pf.returns_stats())

