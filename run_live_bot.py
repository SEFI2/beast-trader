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
from strategy.macd import strategy_macd

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
    },
    "ava": {
        "account_id": "2202647",
        "apiKey": "kA2Wr6dTL1u7pwpdmUObTvAG",
        "secret": "vGeDVoBiYzkXZsz5cCYMitAUsxFtKUUm4P6wCoJWr10_SSfy"
    },
    "sol": {
        "account_id": "2202650",
        "apiKey": "zqxAniO4W_NwNjwzvkWaOx0W",
        "secret": "hFhihTPXq4Hnhz6nTy1snKMYh79fjThcQfFBNMX7nFd11eT7"
    },
    "link": {
        "account_id": "2202569",
        "apiKey": "AbnJbnyepEZrdjZazhEI1AYZ",
        "secret": "rhxBs1BRArblqwj6xDkgNQxXgYf_rD3trw-OUKnlIG7bTW72"
    }
}

#exchange.set_sandbox_mode(True)

from data_collector.data_collector import DataCollector
from strategy_finder.stategy_sorter import find_best_strategy
from strategy.supertrend import strategy_supertrend


buy_count_leverage_params = {
    6: 10,
    5: 5,
    4: 3,
    3: 2,
    2: 1,
    1: 1,
}

def risk_management(exchange, symbol, side, amount, stop_loss, take_profit):
    # Stop loss
    stop_loss_order = exchange.create_order(
        symbol,
        type='limit',
        side='sell' if side == 'buy' else 'buy',
        amount=amount,
        price=None,
        params ={
            "stopProce": stop_loss
        }
        
    )
    print(f"Stop-Loss: {symbol} {side} {stop_loss}")

    # Create the take-profit order
    take_profit_order = exchange.create_order(
        symbol,
        type='limit',
        side='sell' if side == 'buy' else 'buy',
        amount=amount,
        price=None,
        params={
            "stopPrice": take_profit
        }
    )
    print(f"Take-profit: {symbol} {side} {take_profit}")

    return stop_loss_order, take_profit_order

def try_long(exchange, buy_count, symbol, budget, price, precision):
    if buy_count < 3:
        print(f"Buy count is less than 3 for {symbol}")
        return

    amount = budget / price     
    print(f"Trying to buy {symbol}. Buy count {buy_count}. Price: {price}. Budget: {budget}. Amount: {amount}")
    if precision:
        amount *= precision
        print(f"Add precision {precision} {amount}")

    if amount == 0:
        print("Amount is zero")
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
        stop_loss = price - price * 0.04
        take_profit = price + price * 0.02
        risk_management(exchange, symbol, "buy", amount, stop_loss, take_profit)
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

def try_short(exchange, sell_count, symbol, budget, price, precision):
    if sell_count < 3:
        print(f"Sell count is less than 3 for {symbol}")
        return False

    amount = budget / price     
    print(f"Trying to sell {symbol}. Sell count {sell_count}. Price: {price}. Budget: {budget}. Amount: {amount}")
    if precision:
        amount *= precision
        print(f"Add precision {precision} {amount}")
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
        stop_loss = price + price * 0.04
        take_profit = price - price * 0.02
        risk_management(exchange, symbol, "sell", amount, stop_loss, take_profit)
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


def run_live_strategy(exchange, budget, df, symbol, timeframe, precision, strategy_funcs):
    print(f"Running live strategy for {symbol}")

    for strategy_func1 in strategy_funcs:
        (buy, sell) = strategy_func1(df)

    print(f"Buy count {buy_count}")
    print(f"Sell count {sell_count}")

    price = df["close"][-1]
    if buy_count >= sell_count:
        buy_order = try_long(exchange, buy_count, symbol, budget, price, precision)
        if buy_order:
            return buy_order
    elif sell_count > buy_count:
        sell_order = try_short(exchange, sell_count, symbol, budget, price, precision)
        if sell_order:
            return sell_order
    print(f"No strategy is used for {symbol} for now..")
    return 0


def run_bot(config):
    account_name = config["account_name"]
    precision = config["precision"]
    symbol = config["symbol"]
    exchange = ccxt.bitmex({
        'apiKey': accounts[account_name]["apiKey"],
        'secret': accounts[account_name]["secret"],
    })

    try:
        balance = exchange.fetch_balance()
    except Exception as e:
        print(f"Cannot fetch the balance for {symbol} and {account_name}")
        print(e)
        return
    timeframe = "1m"
    last_timestamp = config["timestamp"]
    strategy_funcs = config["strategy_funcs"]

    usdt_balance = balance['USDT']['free']
    print(f"Current balance for {symbol} and {account_name} is {usdt_balance}")
    if usdt_balance > 10:
        total_bot_budget = usdt_balance / 2
    else:
        total_bot_budget = usdt_balance

    try:
        data_collector = DataCollector(exchange, symbol, timeframe)
        df = data_collector.get_live_data()
    except Exception as e:
        print(f"Error while retrieveing data for {symbol}:", e)
        return

    if last_timestamp is not None and df.index[-1] == last_timestamp:
        print(f"Timestamp {symbol} already checked")
        return
    else:
        last_timestamp = df.index[-1]

    print(f"Timestamp {symbol}", last_timestamp)
    out = run_live_strategy(exchange, total_bot_budget, df, symbol, timeframe, precision, strategy_funcs)

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
            "strategy_funcs": [strategy_macd, strategy_ema, strategy_rsi_ma] ,
            "precision": 10000,
        },
        {
            "account_name": "sol",
            "timestamp": None,
            "symbol": "SOLUSDT",
            "strategy_funcs": [strategy_macd, strategy_ema, strategy_rsi_ma] ,
            "precision": 10000
        },
        {
            "account_name": "ava",
            "timestamp": None,
            "symbol": "AVAXUSDT",
            "strategy_funcs": [strategy_macd, strategy_ema, strategy_rsi_ma] ,
            "precision": 10000
        },
        {
            "account_name": "ether",
            "timestamp": None,
            "symbol": "ETHUSDT",
            "strategy_funcs": [strategy_macd, strategy_ema, strategy_rsi_ma] ,
            "precision": 10000
        },
        {
            "account_name": "link",
            "timestamp": None,
            "symbol": "LINKUSDT",
            "strategy_funcs": [strategy_macd, strategy_ema, strategy_rsi_ma] ,
            "precision": 10000
        },
    ]
    for config in configurations:
        run_bot(config)
        schedule.every(20).seconds.do(run_bot, config)
        time.sleep(1)

    while True:
        schedule.run_pending()
        time.sleep(1)
        
run_all_bots()
