import vectorbt as vbt
import numpy as np

def strategy_rsi_ma(close, rsi_window=14, ma_window=50):
    rsi = vbt.RSI.run(close, window=rsi_window).rsi.to_numpy()
    ma = vbt.MA.run(close, window=ma_window).ma.to_numpy()
    trend = np.where(rsi > 70, -1, 0) # exit 
    trend = np.where((rsi < 30) & (close < ma) , 1, trend) # entry
    return trend

def strategy_rsi_ma(df):
    indicator = vbt.IndicatorFactory(
        class_name="RsiMa",
        short_name="RsiMa",
        input_names=["close"],
        param_names=["rsi_window", "ma_window"],
        output_names=["value"],
    ).from_apply_func(
        strategy_rsi_ma,
        rsi_window=14,
        ma_window=50,
    )

    res = indicator.run(df.close)
    buy_signals = res.value == 1
    sell_signals = res.value == -1
    return (
        buy_signals,
        sell_signals
    )
