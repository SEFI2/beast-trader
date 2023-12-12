import pandas as pd

def if_market_volatile(df, threshold=0.01):    
    returns = df['close'].pct_change()
    volatility = returns.std()
    if volatility > threshold:
        return True
    else:
        return False
