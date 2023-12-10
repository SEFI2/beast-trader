
from strategy.ema import strategy_ema
from strategy.supertrend import strategy_supertrend
from strategy.sma import strategy_sma
from strategy.scalping import strategy_scalping
from strategy.rsi_ma import strategy_rsi_ma
import time
from strategy_finder.strategy_finder import StrategyFinder
import copy
from data_collector.data_collector import DataCollector


def init_data(exchange, symbols):
    print(symbols)

    timeframe = "1m"
    configurations = []
    for symbol in symbols:
        data_collector = DataCollector(exchange, symbol, timeframe)
        data_collector.collect()
