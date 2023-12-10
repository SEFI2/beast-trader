
def strategy_sma(df):
    sma50 = df.ta.sma(length=50)
    sma200 = df.ta.sma(length=200)

    buy_signals = sma50 > sma200  # 50-day crosses above 200-day
    sell_signals = sma50 < sma200
    return (
        buy_signals,
        sell_signals
    )
