import vectorbt as vbt
import numpy as np

def indicator_rsi_ma(close, rsi_window=14, ma_window=50):
    rsi = vbt.RSI.run(close, window=rsi_window).rsi.to_numpy()
    ma = vbt.MA.run(close, window=ma_window).ma.to_numpy()

    trend = np.where(rsi > 70, -1, 0) # exit
    rsi = np.where(rsi > 70, -1, 0)
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
        indicator_rsi_ma,
        rsi_window=7,
        ma_window=20,
    )
    rsi_window_arr = [7, 14, 3, 7]
    ma_window_arr = [20, 50, 10, 50]
    res = indicator.run(
        df.close,
        rsi_window=rsi_window_arr,
        ma_window=ma_window_arr,
        #param_product = True
    )
 
    print("res", res)
    buy_signals = res.value == 1
    sell_signals = res.value == -1
    return (
        buy_signals,
        sell_signals
    )
