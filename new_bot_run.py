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
            "strategy_func": strategy_rsi_ma,
            "leverage": 10,
            "precision": 10000,
            "minAmount": 1,
        },
        {
            "account_name": "doge",
            "symbol": "SUIUSDT",
            "timeframe": "1m",
            "strategy_func": strategy_rsi_ma,
            "leverage": 3,
            "precision": 1000,
            "minAmount": 1
        },
        {
            "account_name": "link",
            "symbol": "LINKUSDT",
            "timeframe": "1m",
            "strategy_func": strategy_rsi_ma,
            "leverage": 4,
            "precision": 1000,
            "minAmount": 1

        },
        {
            "account_name": "sol",
            "symbol": "SOLUSDT",
            "timeframe": "1m",
            "strategy_func": strategy_supertrend,
            "leverage": 5,
            "precision": 10000,
            "minAmount": 1
        },
        {
            "account_name": "doge",
            "symbol": "XRPUSDT",
            "timeframe": "1m",
            "strategy_func": strategy_macd,
            "leverage": 5,
            "precision": 1000,
            "minAmount": 10
        },
        {
            "account_name": "sol",
            "symbol": "ETHUSDT",
            "timeframe": "1m",
            "strategy_func": strategy_rsi_ma,
            "leverage": 3,
            "precision": 100000,
            "minAmount": 1,

        },
        {
            "account_name": "ether",
            "symbol": "XBTUSDT",
            "timeframe": "1m",
            "strategy_func": strategy_rsi_ma,
            "leverage": 5,
            "precision": 1000,
            "minAmount": 10,
        },
        {
            "account_name": "kadirpili",
            "symbol": "ADAUSDT",
            "timeframe": "1m",
            "strategy_func": strategy_macd,
            "leverage": 5,
            "precision": 1000,
            "minAmount": 10,
        },
        {
            "account_name": "ether",
            "symbol": "APEUSDT",
            "timeframe": "1m",
            "strategy_func": strategy_rsi_ma,
            "leverage": 7,
            "precision": 10,
            "minAmount": 1,
        },

        {
            "account_name": "kadirpili",
            "symbol": "MATICUSDT",
            "timeframe": "1m",
            "strategy_func": strategy_rsi_ma,
            "leverage": 9,
            "precision": 1000,
            "minAmount": 10,
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
            config["minAmount"],
            
        )
        bots.append(bot)

    def execute_bots():
        for bot in bots:
            bot.run()
            time.sleep(1)

    execute_bots()
    schedule.every(10).seconds.do(execute_bots)

    while True:
        schedule.run_pending()
        time.sleep(1)
        
run_all_bots()
