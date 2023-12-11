import vectorbt as vbt
import pandas as pd

def test_window_strategy(df_full, df, strategy_func):
    df = df_full.loc[df.index]
    (buy, sell) = strategy_func(df)
    pf = vbt.Portfolio.from_signals(
        df.close,
        entries=buy,
        exits=sell,
        short_entries=False,
        short_exits=False,
        init_cash=100_000,
        fees=0, # TODO
        slippage=0.0025
    )
    return pf.total_profit()

def test_strategy(df, strategy_func):
    window = 900
    profits = df.groupby(pd.Grouper(freq='15H')).apply(lambda sub_df: test_window_strategy(df, sub_df, strategy_func))
    #print ("profits", profits)
    return profits

