from strategy_finder.strategy_finder import StrategyFinder
from data_collector.data_collector import DataCollector
from strategy_finder.stategy_sorter import find_best_strategy
import pandas as pd
import os
import plotly.express as px

def init_all_strategy(exchange, symbols, timeframe):
    for symbol in symbols:
        data_collector = DataCollector(exchange, symbol, timeframe)
        df = data_collector.get_all_data()
        if df.empty:
            print("WRN! Skip init bot for {symbol}. Data is empty")
            continue
        contains_none = df.isna().any().any()
        contains_zeros = (df['close'] == 0).any()
        if contains_none or contains_zeros:
            print("WRN! Skip init bot for {symbol}. Contains none or zeros")
            continue

        find_best_strategy(df, symbol, timeframe)

