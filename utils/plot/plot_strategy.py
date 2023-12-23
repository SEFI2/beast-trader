from ..strategy_finder.strategy_finder import StrategyFinder
from data_collector.data_collector import DataCollector
from strategy_finder.stategy_sorter import find_best_strategy

import pandas as pd
import os
import plotly.express as px

strategies_list = [
        {
            "name": "supertrend",
        },
        {
            "name": "EMA",
        },
        {
            "name": "SMA",
        },
        {
            "name": "RSI_MA",
        },
        {
            "name": "Scalping",
        }
    ]

def plot_strategies(symbols, timeframe):
    profit_list = []
    for strategy in strategies_list:
        for symbol in symbols:
            temp_name = f'profits_{strategy["name"]}_{symbol}_{timeframe}.csv'
            temp_name = temp_name.replace("/", "_")
            profits_file = f'data_profits/{temp_name}'
            if not os.path.isfile(profits_file):
                continue

            data = pd.read_csv(profits_file)
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            data.columns = ['timestamp', 'profits']
            data['strategy'] = strategy["name"]
            data['symbol'] = symbol

            data_mean = data.copy()
            data_mean['strategy'] = data_mean['strategy'] + '_mean'
            data_mean['profits'] = data_mean['profits'].mean()
            profit_list.append(data)
            profit_list.append(data_mean)
    df = pd.concat(profit_list)
    fig = px.line(df, x="timestamp", y="profits", color="strategy", facet_col="symbol")
    #fig.update_layout(autosize=False, width=2000, height=6000)
    fig.show()