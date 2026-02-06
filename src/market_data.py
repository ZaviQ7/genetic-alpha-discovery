import yfinance as yf
import pandas as pd
import pandas_ta as ta
import numpy as np
import os

def download_data(ticker="BTC-USD", start="2018-01-01", end="2026-02-01"):
    os.makedirs("data", exist_ok=True)
    file_path = f"data/{ticker}.csv"
    
    if os.path.exists(file_path):
        print(f"Loading {ticker} from cache...")
        df = pd.read_csv(file_path, index_col=0, parse_dates=True)
    else:
        print(f"Downloading {ticker} from Yahoo Finance...")
        df = yf.download(ticker, start=start, end=end)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.to_csv(file_path)
    
    cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    
    return df

def prepare_features(df):
    data = df.copy()
    data = data.dropna()

    data.ta.adx(length=14, append=True)
    data.ta.macd(fast=12, slow=26, signal=9, append=True)
    data.ta.aroon(length=14, append=True)

    data.ta.rsi(length=14, append=True)
    data.ta.stoch(length=14, append=True)
    data.ta.cci(length=20, append=True)

    data['ATR_Norm'] = data.ta.atr(length=14) / data['Close']
    
    bb = data.ta.bbands(length=20, std=2)
    data['BB_Width'] = (bb.iloc[:, 2] - bb.iloc[:, 0]) / data['Close']

    data['OBV'] = data.ta.obv()
    data['OBV_Slope'] = data['OBV'].pct_change(5)
    data.ta.mfi(length=14, append=True)

    data['Close_vs_EMA50'] = data['Close'] / data.ta.ema(length=50)
    data['High_vs_Low'] = (data['High'] - data['Low']) / data['Close']
    
    data['Log_Returns'] = np.log(data['Close'] / data['Close'].shift(1))
    data['Target_NextDay'] = data['Log_Returns'].shift(-1)

    data = data.dropna()
    
    exclude = ['Open', 'High', 'Low', 'Close', 'Volume', 'Target_NextDay', 'Adj Close']
    feature_cols = [c for c in data.columns if c not in exclude]
    
    print(f"Features Generated ({len(feature_cols)}): {feature_cols}")
    
    return data[feature_cols], data['Target_NextDay']