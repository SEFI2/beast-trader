import pandas as pd
import pandas_ta as ta


def strategy_macd_9(df):
    df.ta.macd(close="close", append=True)
    macd = ta.macd(df.close)

    buy_signals = (df['MACD'] > df['MACD_9']) & (df['MACD'].shift(1) < df['MACD_9'].shift(1))
    sell_signals = df.loc[(df['MACD'] < df['MACD_9']) & (df['MACD'].shift(1) > df['MACD_9'].shift(1)), 'Signal'] = -1  # Sell Signal

    return (
        buy_signals,
        sell_signals
    )
