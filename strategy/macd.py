import pandas as pd
import pandas_ta as ta

def strategy_macd(df, n_fast=12, n_slow=26, n_signal=9):
    macd = ta.macd(df.close, n_fast, n_slow, n_signal)
    print(macd)
    buy_signals = macd['MACD_12_26_9'] > macd['MACDh_12_26_9']
    sell_signals = macd['MACD_12_26_9'] < macd['MACDs_12_26_9']

    return (
        buy_signals,
        sell_signals
    )
