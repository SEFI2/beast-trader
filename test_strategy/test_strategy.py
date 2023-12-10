import vectorbt as vbt

def test_strategy(df, strategy_func):
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

    # print("Stats:")
    # print(pf.stats())

    # print()
    # print("Returns:")
    # print(pf.returns_stats())

    # print("Asset returns:")
    # print(pf.asset_returns())
    # print(pf.total_profit())
    # print(pf.total_return())
    return pf.total_profit()

