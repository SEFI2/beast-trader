
import vectorbt as vbt
import pandas as pd
from test_strategy.test_strategy import test_strategy
from symbols.symbols import main_symbols
# -*- coding: utf-8 -*-

import ccxt
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt
import time
import ccxt
from data_collector.data_collector import DataCollector
import vectorbt as vbt
import warnings
import plotly.express as px

warnings.filterwarnings("ignore")
#warnings.simplefilter(action='ignore', category=FutureWarning)

exchange = ccxt.bitmex({
    'apiKey': "nQEbL79NBi7cN65VQXSCvmSo",
    'secret': "R74OKyy8W-xJHmTL3DsGIno32EqLwhA9hRmXvYvLWZ8-I4Zc",
    #'apiKey': '0y7QTbMmps5eWg-fmGS3uOC0',
    #'secret': 'YWZOQMzCFchD4t05CxE0ptuIgcAblctmdxpH4GVlNKC1Yaxl',
})

from strategy.rsi_ma import strategy_rsi_ma
from strategy.supertrend import strategy_supertrend
from strategy.ema_price_crossover import strategy_ema_price_crossover

def run():
    timeframe = "1m"
    all_symbols = []
    for symbol in main_symbols:
        data_collector = DataCollector(exchange, symbol, timeframe)
        df = data_collector.get_all_data()
        if df.empty:
            continue

        test_data = test_strategy(df, strategy_ema_price_crossover)
        print(test_data)
        test_data = test_data.reset_index()
        #test_data.columns = ['timestamp', 'profits', "1", "2", "3"]
        test_data.columns = ['timestamp', 'profits']
        test_data['symbol'] = symbol
        test_data['profits'] = test_data['profits']

        all_symbols.append(test_data)
        print(f"Data for {symbol}")
        print(test_data)

    df = pd.concat(all_symbols)
    fig = px.line(df, x="timestamp", y="profits", color="symbol", facet_col_wrap=3)
    fig.add_hline(y=0, line_dash="dash", line_color="red")  # Customize line properties as needed
    fig.update_layout(autosize=False, width=3000, height=1000)

    fig.show()
    return
    



run()