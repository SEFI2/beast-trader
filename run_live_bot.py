def run_live_strategy(df, symbol, strategy_func):
    (buy, sell) = strategy_func(df)
    amount = 1
    if buy[-1]:
        #order = exchange.create_market_buy_order(symbol, amount)
        print("Buy")
    elif sell[-1]:
        #order = exchange.create_market_sell_order(symbol, amount)
        print("Sell")
    else:
        print("no orders")
