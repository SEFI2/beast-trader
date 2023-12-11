import pandas as pd
import vectorbt as vbt
import pandas_ta as ta
def run_supertrend_strategy(df, length, multiplier):
    multiplier = float(multiplier)
    sti = ta.supertrend(df.high, df.low, df.close, length, multiplier)
    trend_dir = f"SUPERTd_{length}_{multiplier}"
    #print(sti)
    buy_signals = (sti[trend_dir] == 1) & (sti[trend_dir].shift() == -1)
    sell_signals = (sti[trend_dir] == -1) & (sti[trend_dir].shift() == 1)
    return (buy_signals, sell_signals)

def proxy_supertrend(high, low, close, length, multiplier):
    df = pd.DataFrame(dict(open=open, high=high, low=low, close=close))
    return run_supertrend_strategy(df, length, multiplier)

def strategy_supertrend(df):
    indicator = vbt.IndicatorFactory(
        class_name="SupertrendIndicator",
        short_name="Supertrend",
        input_names=["high", "low", "close"],
        param_names=["length", "multiplier"],
        output_names=["buy_signals", "sell_signals"],
    ).from_apply_func(
        proxy_supertrend,
        length=7,
        multiplier=3,
        keep_pd=True,
        to_2d=False
    )

    # length_arr = [7, 10, 5, 7,]
    # multiplier_arr = [3, 3, 2, 2]

    res = indicator.run(
        df.high, df.low, df.close,
        length=7,
        multiplier=3
    )
    return (
        res.buy_signals,
        res.sell_signals
    )

