from new_bot_base import BotBase
from volatility.volatility import if_market_volatile
import numpy as np
from datetime import datetime
from dateutil import parser
import pytz
import time

class Bot(BotBase):
    def __init__(self, account_name, symbol, timeframe, strategy_func, leverage, precision, minAmount):
        super(Bot, self).__init__(account_name, symbol, timeframe, strategy_func, leverage, precision)
        self._init_leverage()
        self.minAmount = minAmount

    def _make_stop_loss(self, side, price, amount):
        if side == "sell":
            stop_loss = price + price * 0.01
        else:
            stop_loss = price - price * 0.01

        print(f"stop_loss_order @{self.symbol} {stop_loss} {amount}")
        stop_loss_order = self._make_order(
            'Stop', 
            "buy" if side == "sell" else "sell",
            amount,
            None, 
            {
                "stopPrice": stop_loss
            }
        )
        if stop_loss_order:
            return True
        return False

    def _make_take_profit(self, side, price, amount):
        if side == "sell":
            take_profit = price - price * 0.003
        else:
            take_profit = price + price * 0.003

        print(f"take_profit_order @{self.symbol} {take_profit} {amount}")
        take_profit_order = self._make_order(
            'MarketIfTouched', 
            "buy" if side == "sell" else "sell",
            amount,
            None, 
            {
                "stopPrice": take_profit
            }
        )
        if take_profit_order:
            return True
        return False

    def _risk_manager(self, side, price, amount):
        #return self._make_stop_loss(side, price, amount) and self._make_take_profit(side, price, amount)            
        return True

    def _try_long(self, amount):
        print(f"Trying to buy for {self.symbol}.")
        order = self._make_market_buy_order(amount, {
            "leverage": self._get_leverage()
        })
        print("long order", order)
        if order is not None:
            return True
        return False

    def _try_short(self, amount):
        print(f"Trying to sell for {self.symbol}.")
        order = self._make_market_sell_order(amount, {
            "leverage": self._get_leverage()
        })
        print("short order", order)
        if order is not None:
            return True
        return False

    def _init_leverage(self):
        try:
            self.exchange.private_post_position_leverage(
                {
                    "symbol": self.symbol, 
                    "leverage": self._get_leverage()
                }
            )
            time.sleep(0.1)
        except Exception as e:
            print("cannot init leverage", e)
 

    def _try_short_long(self, buy, sell):
        price = self._get_price() * self.minAmount
        leverage = self._get_leverage()
        balance = self._get_leveraged_balance()
        portions = [5, 3, 2, 1]
        for portion in portions: 
            budget = balance / portion
            if (budget / price) * self.precision >= self.precision:
                print(f"@{self.symbol} found precision at portion {portion}")
                break
            
        amount = budget / price

        print(f"Current leverage balance {balance} at leverage {leverage} and budget {budget}")
        print(f"Trying short or long @{self.symbol} at price {price} with amount {amount}.")
        print(f"Mint amount {self.minAmount}")

        amount *= self.precision
        if buy:
            if self._try_long(amount):
                #return True
                return self._risk_manager("buy", price, amount)
            return False
        elif sell:
            if self._try_short(amount):
                #return True
                return self._risk_manager("sell", price, amount)
        return False

    def _data_last_time(self):
        return self.data.index[-1]

    def analyze_positions(self):
        try:
            markets = self.exchange.load_markets()
            positions = self.exchange.fetch_positions()
            for position in positions:
                info = position["info"]
                if info["symbol"] != self.symbol:
                    continue
                is_open = info["isOpen"]
                if is_open is None or is_open is False:
                    continue
                roe = info['unrealisedRoePcnt']

                if "unrealisedRoePcnt" in info:
                    roe = float(info['unrealisedRoePcnt'])
                else:
                    roe = 0.0

                time = position["timestamp"]
                amount = float(info["currentQty"])
                side = position['side']
                print("found")
                print(amount, time, side, roe)

                if roe <= -0.03:
                    print("need to cancel")
                    if side == "long":
                        self._make_market_sell_order(amount, params={"reduceOnly": True})
                    else:
                        self._make_market_buy_order(amount, params={"reduceOnly": True})
                    continue
                if roe >= 0.01:
                    print("need to take profit")
                    if side == "long":
                        self._make_market_sell_order(amount, params={"reduceOnly": True})
                    else:
                        self._make_market_buy_order(amount, params={"reduceOnly": True})
                    continue

        except Exception as e:
            print("Cannot analyze markets", e)

    def _run_strategy(self):
        (buy, sell) = self._strategy_signal()
        if buy is np.True_ or buy is np.True_:
            return self._try_short_long(buy, sell)
        print(f"No signals at all for {self.symbol}")
        return False

    def _strategy_signal(self):
        (buy, sell) = self.strategy_func(self.data)
        return (buy[-1], sell[-1]) 

    def _check_if_market_volatile(self):
        try:
            return if_market_volatile(self.data)
        except Exception as e:
            print("Error checking volatility", e)
            return False    

    def _start(self):
        
        self.analyze_positions()

        balance = self._get_balance()
        if balance == 0:
            print("ERR! {self.symbol} - No user balance")
            return False

        self._get_data()

        if self.data is None:
            print(f"ERR! {self.symbol} - No data")
            return False
        if self._check_if_market_volatile():
            print(f"ERR! {self.symbol} - Market too volatile now")
            return False
        if self._already_checked():
            print(f"ERR! {self.symbol} - Timestamp already checked")
            return False

        self._run_strategy()

    def run(self):
        self._start()


