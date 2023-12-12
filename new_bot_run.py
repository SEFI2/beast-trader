# -*- coding: utf-8 -*-

import time
import schedule
import pandas as pd
pd.set_option('display.max_rows', None)

import time
import time
import warnings
warnings.filterwarnings("ignore")

# strategies
from strategy.supertrend import strategy_supertrend
from strategy.ema_price_crossover import strategy_ema_price_crossover
from strategy.sma import strategy_sma
from strategy.ema import strategy_ema
from strategy.rsi_ma import strategy_rsi_ma
from strategy.macd import strategy_macd


from strategy.supertrend import strategy_supertrend
from new_bot import Bot

def run_all_bots():
    configurations = [
        {
            "account_name": "ltc",
            "symbol": "LTCUSDT",
            "timeframe": "1m",
            "strategy_func": strategy_supertrend,
            "leverage": 2,
            "precision": 1000
        },
        {
            "account_name": "link",
            "symbol": "LINKUSDT",
            "timeframe": "1m",
            "strategy_func": strategy_rsi_ma,
            "leverage": 3,
            "precision": 1000
        },
        {
            "account_name": "sol",
            "symbol": "SOLUSDT",
            "timeframe": "1m",
            "strategy_func": strategy_ema_price_crossover,
            "leverage": 2,
            "precision": 10000
        },
        {
            "account_name": "doge",
            "symbol": "DOGEUSDT",
            "timeframe": "1m",
            "strategy_func": strategy_ema_price_crossover,
            "leverage": 3,
            "precision": 1000
        },
        {
            "account_name": "ether",
            "symbol": "ETHUSDT",
            "timeframe": "1m",
            "strategy_func": strategy_rsi_ma,
            "leverage": 2,
            "precision": 100000
        },
        {
            "account_name": "kadirpili",
            "symbol": "ADAUSDT",
            "timeframe": "1m",
            "strategy_func": strategy_macd,
            "leverage": 2,
            "precision": 100000
        },
    ]
    timeframe = "1m"

    bots = []
    for config in configurations:
        bot = Bot(
            config["account_name"],
            config["symbol"],
            timeframe,
            config["strategy_func"],
            config["leverage"],
            config["precision"],
        )
        bots.append(bot)

    def execute_bots():
        for bot in bots:
            bot.run()
            time.sleep(1)

    execute_bots()
    schedule.every(2).minutes.do(execute_bots)

    while True:
        schedule.run_pending()
        time.sleep(1)
        
run_all_bots()
