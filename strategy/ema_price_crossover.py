import pandas as pd
import vectorbt as vbt
import pandas_ta as ta

def run_price_crossover_strategy(df, length, threshold_percentage):
    
    ema800 = ta.ema(df.close, length)
    ema_threshold = ema800  * (100 - threshold_percentage) / 100
    buy_signals = (df.close > ema800) & (df.volume > 0)
    sell_signals = (df.close < ema_threshold)
    return (buy_signals, sell_signals)

def proxy_ema_price_crossover(high, low, close, volume, length, threshold_percentage):
    df = pd.DataFrame(dict(open=open, high=high, low=low, close=close, volume=volume))
    return run_price_crossover_strategy(df, length, threshold_percentage)

def strategy_ema_price_crossover(df):
    indicator = vbt.IndicatorFactory(
        class_name="EMAPriceCrossOver",
        short_name="EMAPX",
        input_names=["high", "low", "close", "volume"],
        param_names=["length", "threshold_percentage"],
        output_names=["buy_signals", "sell_signals"],
    ).from_apply_func(
        proxy_ema_price_crossover,
        length=200,
        threshold_percentage=1,
        keep_pd=True,
        to_2d=False
    )

    length_arr = [20]
    threshold_percentage_arr = [1]

    res = indicator.run(
        df.high, df.low, df.close, df.volume,
        length=length_arr,
        threshold_percentage=threshold_percentage_arr
    )
    return (
        res.buy_signals,
        res.sell_signals
    )

