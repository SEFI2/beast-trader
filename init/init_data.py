
from strategy.ema import strategy_ema
from strategy.supertrend import strategy_supertrend
from strategy.sma import strategy_sma
from strategy.scalping import strategy_scalping
from strategy.rsi_ma import strategy_rsi_ma
import time
from strategy_finder.strategy_finder import StrategyFinder
import copy
from data_collector.data_collector import DataCollector


def init_all_data(exchange, symbols, timeframe):
    for symbol in symbols:
        data_collector = DataCollector(exchange, symbol, timeframe)
        data_collector.collect_until_today()
