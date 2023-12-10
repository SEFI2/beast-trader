import vectorbt as vbt

def indicator_scalping(close, rsi_window=14, ma_window=50):
    buy_signals = close < close.shift()
    sell_signals = close > close.shift()
    return (buy_signals, sell_signals)

def strategy_scalping(df):
    indicator = vbt.IndicatorFactory(
        class_name="Scalping",
        short_name="Scalping",
        input_names=["close"],
        param_names=[],
        output_names=["buy_signals", "sell_signals"],
    ).from_apply_func(
        indicator_scalping,
        keep_pd=True,
        to_2d=False
    )
    res = indicator.run(df.close)
    return (
        res.buy_signals,
        res.sell_signals
    )
