import ccxt
import pandas as pd
import backtrader as bt
import pandas_ta as ta
from datetime import datetime, timedelta
import time
import os

# Define the symbol and timeframe
symbol = 'ETHUSDT'  # Example symbol
timeframe = '1m'     # Example timeframe

# Initialize the exchange
exchange = ccxt.bitmex({
    #'apiKey': "nQEbL79NBi7cN65VQXSCvmSo",
    #'secret': "R74OKyy8W-xJHmTL3DsGIno32EqLwhA9hRmXvYvLWZ8-I4Zc",
    'apiKey': '0y7QTbMmps5eWg-fmGS3uOC0',
    'secret': 'YWZOQMzCFchD4t05CxE0ptuIgcAblctmdxpH4GVlNKC1Yaxl',
})
exchange.set_sandbox_mode(True)


class DataCollector:
    def __init__(self, exchange, symbol, timeframe):
        self.symbol = symbol
        self.timeframe = timeframe
        self.exchange = exchange
        folder = 'data/'
        temp_name = f'{self.symbol}_{self.timeframe}.csv'
        temp_name = temp_name.replace("/", "_")
        self.file_name = f'{folder}{temp_name}'

    def _save_file(self, new_data):
        if not os.path.isfile(self.file_name):
            print(f'{self.file_name} create new file.')
            new_data.to_csv(self.file_name)
            return

        print(f'{self.file_name} already exists. Join.')
        existing_data = pd.read_csv(self.file_name, index_col='timestamp')
        new_rows = new_data[~new_data.index.isin(existing_data.index)]
        if new_rows.empty:
            print("INF! No new data.")
            return

        print(f"INF! Concatenate {self.file_name}.")
        result = pd.concat([existing_data, new_rows])
        result.to_csv(self.file_name)

    def continue_collect(self, end):
        existing_data = pd.read_csv(self.file_name, index_col='timestamp')
        start = pd.to_datetime(existing_data.index[-1]).timestamp() * 1000 + 60000
        return self.collect(start, end)

    def get_last_15_hours_data(self):
        bars = self.exchange.fetch_ohlcv(self.symbol, since=None, timeframe=self.timeframe, limit=900) # 15 hours
        contains_none = any(item is None for item in bars[-1])
        if contains_none:
            print("WRN! CONTAINS NONE")
            bars = bars[:-1]

        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        if not df["close"][-1]:
            df.drop(df.index[-1], inplace=True)
        return df

    def get_last_5_hours_data(self):
        bars = self.exchange.fetch_ohlcv(self.symbol, timeframe=self.timeframe, limit=300) # 5 hours
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df

    def get_live_data(self):
        end = datetime.now()
        start = (end - timedelta(days=1))  # Two days ago
        end = int(end.timestamp()) * 1000
        start = int(start.timestamp()) * 1000
        print(start, end)
        df = self._get_data(start, end, True)
        #self._save_file(df)
        return df
        
    def get_all_data(self):
        data = pd.read_csv(self.file_name, index_col='timestamp')
        data.index = pd.to_datetime(data.index)
        return data

    def _get_data(self, start, end, non_stop = False):
        data = []
        while True:
            if non_stop is False and start >= end:
                break
            bars = self.exchange.fetch_ohlcv(self.symbol, timeframe=self.timeframe, since=start, limit=900) # 15 hours
            if len(bars) == 0:
                break
            start = bars[-1][0] + 60000
            data += bars

            time.sleep(1)

        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df

    def collect_until_today(self):
        if os.path.isfile(self.file_name):
            return
        if os.path.isfile(self.file_name):
            existing_data = pd.read_csv(self.file_name, index_col='timestamp')
            start = pd.to_datetime(existing_data.index[-1]).timestamp() * 1000 + 60000
            df = self._get_data(start, end, True)
            self._save_file(df)
            return

        end = datetime.now()
        start = (end - timedelta(days=120))  # since 120 days ago
        end = int(end.timestamp()) * 1000
        start = int(start.timestamp()) * 1000
        df = self._get_data(start, end, True)
        self._save_file(df)
        return df

    def collect(self, start, end):
        df = self._get_data(start, end)
        self._save_file(df)
        return df


