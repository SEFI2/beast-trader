def strategy_ema(df):
    short = df.ta.ema(length=20)
    long = df.ta.ema(length=50)

    buy_signals = short > long  # 50-day crosses above 200-day
    sell_signals = short < long
    return (
        buy_signals,
        sell_signals
    )

