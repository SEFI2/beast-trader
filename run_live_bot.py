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
from strategy.ema import strategy_ema
from strategy.rsi_ma import strategy_rsi_ma

warnings.filterwarnings("ignore")
#warnings.simplefilter(action='ignore', category=FutureWarning)


accounts = {
    "matic": {
        "account_id": "2202563",
        "apiKey": "B5WFVS4A1lP_zfd_pcBZuagD",
        "secret": "t0G9h9qwcKpApTXowbjuz9O7IsinHjQcBcr5dP0a9VTxmkK8"
    },
    "ether": {
        "account_id": "2202564",
        "apiKey": "7mT68GGufNsN2oAXkYrJ15_d",
        "secret": "VCyljkhsfVK01LmhCowKMmy9lmJXViq8pBxox2CEmPL4tN1t"
    }

}

#exchange.set_sandbox_mode(True)

from data_collector.data_collector import DataCollector
from strategy_finder.stategy_sorter import find_best_strategy
from strategy.supertrend import strategy_supertrend


buy_count_leverage_params = {
    6: 50,
    5: 20,
    4: 10,
    3: 5,
    2: 2,
    1: 1,
}


def try_long(exchange, buy_count, symbol, budget, price):
    if buy_count == 0:
        print(f"Buy count is zero for {symbol}")
        return
    
    amount = (int(round(budget / price)) // 10) * 10
    print(f"Trying to buy {symbol}. Buy count {buy_count}. Price: {price}. Budget: {budget}. Amount: {amount}")
    amount = (amount//10) * 1000
    if amount == 0:
        return
    print(amount)
    
    params = {
        "leverage": 1,
        "takeProfitPrice": None,
        "takeProfitPrice": None,
    }

    try:
        params = {
            "leverage": buy_count_leverage_params[buy_count]
        }
        order = exchange.create_market_buy_order(symbol, amount, params)
        price = order["price"]
        buy_amount = order["filled"]
        spend_amount = order['cost']
        print(f"BUY!! {symbol} - {buy_amount} - {price} - {spend_amount}", order)
        return (
            buy_amount,
            price,
            spend_amount
        )
    except Exception as e:
        print(f"Cannot buy for {symbol}")
        print("error:", e)
        return None
    return budget

def try_short(exchange, sell_count, symbol, budget, price):
    if sell_count == 0:
        print(f"Sell count is zero for {symbol}")
        return False

    amount = (int(round(budget / price)) // 10) * 10
    print(f"Trying to sell {symbol}. Sell count {sell_count}. Price: {price}. Budget: {budget}. Amount: {amount}")
    amount = (amount//10) * 1000
    if amount == 0:
        return
    print(amount)

    try:
        params = {
            "leverage": buy_count_leverage_params[sell_count]
        }
        order = exchange.create_market_sell_order(symbol, amount, params)

        price = order["price"]
        sell_amount = order["filled"]
        spend_amount = order['cost']
        print(f"SELL!! {symbol} - {sell_amount} - {price} - {spend_amount}", order)
        return (
            sell_amount,
            price,
            spend_amount
        )
    except Exception as e:
        print(f"Cannot sell for {symbol}")
        print("error:", e)
        return None
    return budget


def run_live_strategy(exchange, budget, df, symbol, timeframe, strategy_func1, strategy_func2, strategy_func3):
    print(f"Running live strategy for {symbol}")
    (buy1, sell1) = strategy_func1(df)
    (buy2, sell2) = strategy_func2(df)
    (buy3, sell3) = strategy_func3(df)
    print(buy1[-1])
    print(buy2[-1])
    print(buy3[-1])
    
    buy_count = (buy1[-1] is True) * 3 + (buy2[-1] is True) * 2 + (buy3[-1] is True) * 1
    sell_count = (sell1[-1] is True) * 3 + (sell2[-1] is True) * 2 + (sell3[-1] is True) * 1

    price = df["close"][-1]
    buy_order = try_long(exchange, buy_count, symbol, budget, price)
    if buy_order:
        return buy_order

    sell_order = try_short(exchange, sell_count, symbol, budget, price)
    if sell_order:
        return -sell_order
    return 0


def run_bot(config):
    account_name = config["account_name"]
    exchange = ccxt.bitmex({
        'apiKey': accounts[account_name]["apiKey"],
        'secret': accounts[account_name]["secret"],
        #'apiKey': '0y7QTbMmps5eWg-fmGS3uOC0',
        #'secret': 'YWZOQMzCFchD4t05CxE0ptuIgcAblctmdxpH4GVlNKC1Yaxl',
    })
    exchange.create_market_buy_order

    balance = exchange.fetch_balance()
    print(balance)
    timeframe = "1m"
    last_timestamp = config["timestamp"]
    symbol = config["symbol"]
    strategy_func1 = config["strategy_func1"]
    strategy_func2 = config["strategy_func2"]
    strategy_func3 = config["strategy_func3"]

    usdt_balance = balance['USDT']['free']
    print(f"Current balance for {symbol} and {account_name} is {usdt_balance}")
    total_bot_budget = usdt_balance


    try:
        data_collector = DataCollector(exchange, symbol, timeframe)
        df = data_collector.get_last_15_hours_data()
    except Exception as e:
        print(f"Error while retrieveing data for {symbol}:", e)
        return

    if last_timestamp is not None and df.index[-1] == last_timestamp:
        print(f"Timestamp {symbol} already checked")
        return
    else:
        last_timestamp = df.index[-1]

    print(f"Timestamp {symbol}", last_timestamp)
    out = run_live_strategy(exchange, total_bot_budget, df, symbol, timeframe, strategy_func1, strategy_func2, strategy_func3)

    #config["budget"] += out
    config["timestamp"] = last_timestamp
    print()


def run_all_bots():
    timeframe = "1m"

    configurations = [
        {
            "account_name": "matic",
            "timestamp": None,
            "symbol": "MATICUSDT",
            "strategy_func1": strategy_rsi_ma,
            "strategy_func2": strategy_ema,
            "strategy_func3": strategy_supertrend
        },
        {
            "account_name": "ether",
            "timestamp": None,
            "symbol": "ETHUSDT",
            "strategy_func1": strategy_rsi_ma,
            "strategy_func2": strategy_ema,
            "strategy_func3": strategy_supertrend
        },

        # {
        #     "timestamp": None,
        #     "budget": 10,
        #     "symbol": "LINK/USDT",
        #     "strategy_func": strategy_rsi_ma
        # },
        # {
        #     "timestamp": None,
        #     "budget": 10,
        #     "symbol": "GMT/USDT:USDT",
        #     "strategy_func": strategy_rsi_ma
        # }
    ]
    for config in configurations:
        run_bot(config)
        schedule.every(10).seconds.do(run_bot, config)
        time.sleep(1)

    while True:
        schedule.run_pending()
        time.sleep(1)
        
run_all_bots()
