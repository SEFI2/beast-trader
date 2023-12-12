import vectorbt as vbt
import pandas as pd

def test_window_strategy(df_full, df, strategy_funcs):
    df = df_full.loc[df.index]
    buy = None
    sell = None
    for index, strategy_func in enumerate(strategy_funcs):
        (buy_new, sell_new) = strategy_func(df)
        if buy is None:
            buy = buy_new.astype(int)
            sell = sell_new.astype(int)
        else:
            buy = buy + buy_new.astype(int) * (1 + 1/(index + 1))
            sell = sell + sell_new.astype(int) * (1 + 1/(index + 1))
    print("buy")
    print(buy)
    print("sell")
    print(sell)
    print((len(strategy_funcs)+1) // 2)
    buy = buy >= len(strategy_funcs)
    sell = sell >= len(strategy_funcs)
    true_count = (buy == True).sum()
    print("true_count", true_count)
    true_count = (sell == True).sum()
    print("sell true_count", true_count)
    
    print(buy)
    print(sell)
    pf = vbt.Portfolio.from_signals(
        df.close,
        entries=buy,
        exits=sell,
        #short_entries=False,
        #short_exits=False,
        init_cash=100_000,
        fees=0, # TODO
        slippage=0.0025
    )
    return pf.total_return() * 100

def test_strategy(df, strategy_funcs):
    window = 900
    profits = df.groupby(pd.Grouper(freq='15H')).apply(lambda sub_df: test_window_strategy(df, sub_df, strategy_funcs))
    #print ("profits", profits)
    return profits

