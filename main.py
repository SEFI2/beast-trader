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
from data_collector import DataCollector
import vectorbt as vbt
import warnings
import warnings
warnings.filterwarnings("ignore")
#warnings.simplefilter(action='ignore', category=FutureWarning)

exchange = ccxt.bitmex({
    #'apiKey': "nQEbL79NBi7cN65VQXSCvmSo",
    #'secret': "R74OKyy8W-xJHmTL3DsGIno32EqLwhA9hRmXvYvLWZ8-I4Zc",
    'apiKey': '0y7QTbMmps5eWg-fmGS3uOC0',
    'secret': 'YWZOQMzCFchD4t05CxE0ptuIgcAblctmdxpH4GVlNKC1Yaxl',
})
exchange.set_sandbox_mode(True)

from init_data import init_data

markets = exchange.load_markets()
symbols = list(markets.keys())
filtered_symbols = [x for x in symbols if "USD" in x]

init_data(exchange, symbols)