# -*- coding: utf-8 -*-

import os
import sys
import time

import ccxt
import config
import schedule
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt
import time
pd.set_option('display.max_rows', None)
import numpy as np
from datetime import datetime
import time
import ccxt
from data_collector.data_collector import DataCollector
import vectorbt as vbt
import warnings
import warnings
from plot_strategy import plot_strategies

warnings.filterwarnings("ignore")
#warnings.simplefilter(action='ignore', category=FutureWarning)

exchange = ccxt.bitmex({
    'apiKey': "nQEbL79NBi7cN65VQXSCvmSo",
    'secret': "R74OKyy8W-xJHmTL3DsGIno32EqLwhA9hRmXvYvLWZ8-I4Zc",
    #'apiKey': '0y7QTbMmps5eWg-fmGS3uOC0',
    #'secret': 'YWZOQMzCFchD4t05CxE0ptuIgcAblctmdxpH4GVlNKC1Yaxl',
})
#exchange.set_sandbox_mode(True)

balance = exchange.fetch_balance()
usdt_balance = balance['USDT']['total']
print("current balance", usdt_balance)

from init_data import init_all_data
from init_strategy import init_all_strategy
from symbols.symbols import acceptable_symbols

def init():
    # markets = exchange.load_markets()
    # filtered_symbols = [x for x in symbols if "USDT" in x]
    
    symbols = acceptable_symbols
    timeframe = "1m"
    #init_all_data(exchange, filtered_symbols, timeframe)
    #init_all_strategy(exchange, filtered_symbols, timeframe)
    #plot_strategies(symbols, timeframe)

init()
