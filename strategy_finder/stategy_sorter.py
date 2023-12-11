
from strategy.ema import strategy_ema
from strategy.supertrend import strategy_supertrend
from strategy.sma import strategy_sma
from strategy.scalping import strategy_scalping
from strategy.rsi_ma import strategy_rsi_ma
import time
from strategy_finder.strategy_finder import StrategyFinder
import copy

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

def get_existing_best_strategy(symbol, timeframe):
    print(f"INF! Retrieve the existing best strategy for {symbol}")
    copy_list = copy.deepcopy(strategies_list)
    finder = StrategyFinder(symbol, timeframe, copy_list)
    stategies_list = finder.retrieve_existing_stategies_list()
    best_strategy = stategies_list[0]
    print(f"Current best strategy for {symbol} is {best_strategy['name']} with profit {best_strategy['profit']}")
    return best_strategy

def find_best_strategy(df, symbol, timeframe):
    print(f"INF! Finding the best strategy for {symbol}")

    copy_list = copy.deepcopy(strategies_list)
    finder = StrategyFinder(symbol, timeframe, copy_list)
    finder.update_strategies_list(df)

    stategies_list = finder.get_stategies_list()
    best_strategy = stategies_list[0]
    print(f"Choosing best stategy for {symbol} with strategy {best_strategy['name']} and profit {best_strategy['profit']}")
    return best_strategy