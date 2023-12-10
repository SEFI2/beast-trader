import ccxt
import pandas as pd
import backtrader as bt
import pandas_ta as ta

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

exchange.load_markets()

# Fetch historical data
data = exchange.fetch_ohlcv(symbol, timeframe, limit=900)
df = pd.DataFrame(data[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)

# Calculate breakout conditions and additional indicators
df['breakout'] = ta.vwap(df['high'], df['low'], df['close'], df['volume'], length=20)
df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
df['rsi'] = ta.rsi(df['close'], length=14)
df['confidence'] = ((df['close'] - df['breakout']) / df['atr']).abs()
df['buy_signal'] = df['close'] > 10#(df['close'] > df['breakout']) & (df['confidence'] > 1.5) & (df['rsi'] > 70)
df['sell_signal'] = (df['close'] < df['breakout']) & (df['confidence'] > 1.2) & (df['rsi'] < 30)

class BreakoutStrategy(bt.Strategy):
    params = (
        ('buy_threshold', 1.5),
        ('sell_threshold', 1.2),
        ('rsi_threshold', 70),
        ('risk_percentage', 0.02),
        ('symbol', symbol),
        ('timeframe', bt.TimeFrame.Minutes),
        ('printlog', False),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buy_sig = df['buy_signal']
        self.sell_sig = df['sell_signal']

    def next(self):
        if self.buy_sig[] and not self.position:
            self.order = self.buy()
        elif self.sell_sig and self.position:
            self.order = self.sell()

        self.log('Close, %.2f' % self.dataclose[0])

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.buy_sig = None
            elif order.issell():
                self.sell_sig = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(f'OPERATION PROFIT, GROSS {trade.pnl}, NET {trade.pnlcomm}')

    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()}, {txt}')
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))


cerebro = bt.Cerebro()
#print(df)

data = bt.feeds.PandasData(dataname=df)
cerebro.adddata(data)
cerebro.addstrategy(BreakoutStrategy)
cerebro.broker.setcash(10000.0)

cerebro.run()

#cerebro.plot()
