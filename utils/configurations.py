# strategies
from strategy.supertrend import strategy_supertrend
from strategy.ema_price_crossover import strategy_ema_price_crossover
from strategy.sma import strategy_sma
from strategy.ema import strategy_ema
from strategy.rsi_ma import strategy_rsi_ma
from strategy.macd import strategy_macd
from strategy.supertrend import strategy_supertrend

configurations = [
    {
        "account_name": "ltc",
        "symbol": "LTCUSDT",
        "timeframe": "1m",
        "strategy_func": strategy_rsi_ma,
        "leverage": 10,
        "precision": 1000,
        "minAmount": 0.1,
    },
    {
        "account_name": "doge",
        "symbol": "SUIUSDT",
        "timeframe": "1m",
        "strategy_func": strategy_rsi_ma,
        "leverage": 10,
        "precision": 1000,
        "minAmount": 1
    },
    {
        "account_name": "link",
        "symbol": "LINKUSDT",
        "timeframe": "1m",
        "strategy_func": strategy_rsi_ma,
        "leverage": 10,
        "precision": 1000,
        "minAmount": 1

    },
    {
        "account_name": "sol",
        "symbol": "SOLUSDT",
        "timeframe": "1m",
        "strategy_func": strategy_supertrend,
        "leverage": 10,
        "precision": 10000,
        "minAmount": 1
    },
    {
        "account_name": "doge",
        "symbol": "XRPUSDT",
        "timeframe": "1m",
        "strategy_func": strategy_macd,
        "leverage": 10,
        "precision": 1000,
        "minAmount": 10
    },
    {
        "account_name": "sol",
        "symbol": "ETHUSDT",
        "timeframe": "1m",
        "strategy_func": strategy_rsi_ma,
        "leverage": 10,
        "precision": 100000,
        "minAmount": 1,

    },
    {
        "account_name": "ether",
        "symbol": "XBTUSDT",
        "timeframe": "1m",
        "strategy_func": strategy_rsi_ma,
        "leverage": 10,
        "precision": 1000,
        "minAmount": 1,
    },
    {
        "account_name": "kadirpili",
        "symbol": "ADAUSDT",
        "timeframe": "1m",
        "strategy_func": strategy_macd,
        "leverage": 10,
        "precision": 1000,
        "minAmount": 10,
    },
    {
        "account_name": "ether",
        "symbol": "APEUSDT",
        "timeframe": "1m",
        "strategy_func": strategy_rsi_ma,
        "leverage": 10,
        "precision": 10,
        "minAmount": 1,
    },

    {
        "account_name": "kadirpili",
        "symbol": "MATICUSDT",
        "timeframe": "1m",
        "strategy_func": strategy_rsi_ma,
        "leverage": 10,
        "precision": 1000,
        "minAmount": 10,
    },
]
