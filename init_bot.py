
from strategy.ema import strategy_ema
from strategy.supertrend import strategy_supertrend
from strategy.sma import strategy_sma
from strategy.scalping import strategy_scalping
from strategy.rsi_ma import strategy_rsi_ma
import time
from strategy_finder.strategy_finder import StrategyFinder
import copy
from data_collector.data_collector import DataCollector

strategies_list = [
        {
            "name": "supertrend",
            "func": strategy_supertrend,
            "profit": 0,
        },
        {
            "name": "EMA",
            "func": strategy_ema,
            "profit": 0,
        },
        {
            "name": "SMA",
            "func": strategy_sma,
            "profit": 0,
        },
        {
            "name": "RSI_MA",
            "func": strategy_rsi_ma,
            "profit": 0,
        },
        {
            "name": "Scalping",
            "func": strategy_scalping,
            "profit": 0,
        }
    ]

def run_live_bot(config):
    symbol = config["symbol"]
    finder = config["finder"]
    data_collector = config["data_collector"] 
    df = data_collector.get_last_5_hours_data()
    if df.empty:
        return False

    contains_none = df.isna().any().any()
    contains_zeros = (df['close'] == 0).any()
    if contains_none or contains_zeros:
        return False
    finder.update_strategies_list(df)
    stategies_list = finder.get_stategies_list()
    best_strategy = stategies_list[0]

    print(f"Running best stategy for {symbol} with strategy {best_strategy['name']} and profit {best_strategy['profit']}")
    #run_live_strategy(df, symbol, best_strategy['func'])
    return True

def run_all_bots(configurations):
    for config in configurations:
        run_live_bot(config)
        time.sleep(0.5)

def init_all_bots():
    markets = exchange.load_markets()
    symbols = list(markets.keys())
    filtered_symbols = [x for x in symbols if "USD" in x]

    print(filtered_symbols)
    print("Num of symbols", len(filtered_symbols))
    balance = exchange.fetch_balance()
    usdt_balance = balance['USDT']['total']
    print("current balance", usdt_balance)

    timeframe = "1m"
    configurations = []
    for symbol in filtered_symbols:
        data_collector = DataCollector(exchange, symbol, timeframe)
        copy_list = copy.deepcopy(strategies_list)
        finder = StrategyFinder(symbol, copy_list)
        bot_config = {
            "finder": finder,
            "symbol": symbol,
            "data_collector": data_collector
        }
        configurations.append(bot_config)
        #break
    print("configurations", configurations)
    run_all_bots(configurations)
