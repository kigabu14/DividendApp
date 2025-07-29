# modules/stock_data.py

import yfinance as yf
import pandas as pd

def get_price(symbol: str) -> float:
    try:
        ticker = yf.Ticker(symbol + ".BK")
        todays_data = ticker.history(period='1d')
        return todays_data['Close'].iloc[-1]
    except Exception as e:
        print(f"Error getting price for {symbol}: {e}")
        return 0.0

def get_dividends(symbol: str) -> pd.DataFrame:
    try:
        stock = yf.Ticker(symbol + ".BK")
        dividends = stock.dividends
        if dividends.empty:
            return pd.DataFrame()
        df = dividends.reset_index()
        df.columns = ["Date", "Dividend"]
        df["Date"] = pd.to_datetime(df["Date"])
        df["Year"] = df["Date"].dt.year
        df["Month"] = df["Date"].dt.month
        return df
    except Exception as e:
        print(f"Error getting dividends for {symbol}: {e}")
        return pd.DataFrame()
