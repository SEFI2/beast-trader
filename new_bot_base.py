

import ccxt
from accounts import accounts
from data_collector.data_collector import DataCollector
import time

class BotBase:
    def __init__(self, account_name, symbol, timeframe, strategy_func, leverage, precision) -> None:
        self.symbol = symbol
        self.timeframe = timeframe
        self.strategy_func = strategy_func
        self.account_name = account_name
        self.leverage = leverage
        self.precision = precision
        self.exchange = ccxt.bitmex({
            'apiKey': accounts[account_name]["apiKey"],
            'secret': accounts[account_name]["secret"],
        })
        self.data_collector = DataCollector(self.exchange, self.symbol, self.timeframe)
        self.data = None
        self.last_timestamp = None
        self.balance = None

    def _get_data(self):
        try:
            self.data = self.data_collector.get_live_data()
            return self.data
        except Exception as e:
            print(f"Error while retrieveing data", e)
            return None

    def _get_leveraged_balance(self):
        return self._get_balance() * self._get_leverage()
    def _get_balance(self):
        try:
            all_balances = self.exchange.fetch_balance()
            self.balance = all_balances['USDT']['free']
            print(f'Balance: {self.symbol} {self.balance}')
            time.sleep(0.3)
            return self.balance
        except Exception as e:
            print(f"Fetch balance error:", e)
            return 0

    def _already_checked(self):
        current_timestamp = self.data.index[-1]
        if self.last_timestamp is None:
            self.last_timestamp = current_timestamp
            return False
        return self.last_timestamp == current_timestamp

    def _get_price(self):
        price = self.data.close[-1]
        return price
    
    def _make_order(self, ordType, side, amount, price, params):
        try:
            order = self.exchange.create_order(self.symbol, ordType, side, amount, price, params)
            time.sleep(0.4)
            return order
        except Exception as e:
            print("ERR! Cannot make an order: ", e)
            time.sleep(0.4)
            return None

    def _make_stop_market_order(self, side, amount, stopPrice):
        return self._make_order('MarketIfTouched', side, amount, None, {
            "stopPrice": stopPrice,            
        })

    def _make_limit_order(self, side, amount, price, params={}):
        return self._make_order('limit', side, amount, price, params)

    def _make_market_order(self, side, amount, params={}):
        return self._make_order('market', side, amount, None, params)

    def _make_market_buy_order(self, amount, params={}):
        return self._make_market_order("buy", amount, params)

    def _make_market_sell_order(self, amount, params={}):
        return self._make_market_order("sell", amount, params)

    def _make_buy_order_with_leverage(self, amount, leverage):
        return self._make_market_buy_order(amount, {
            "leverage": leverage
        })

    def _make_sell_order_with_leverage(self, amount, leverage):
        return self._make_market_sell_order(amount, {
            "leverage": leverage
        })

    def _make_sell_order(self, amount, params):
        return self._make_order("buy", amount, params)

    def _get_leverage(self):
        return self.leverage

