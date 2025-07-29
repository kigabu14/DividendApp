import yfinance as yf
import pandas as pd
from datetime import datetime

def get_price(symbol: str) -> float:
    try:
        ticker = yf.Ticker(symbol if symbol.endswith(".BK") else symbol + ".BK")
        hist = ticker.history(period="1d")
        return round(hist["Close"].iloc[-1], 2)
    except:
        return 0.0

def get_dividends(symbol: str) -> pd.DataFrame:
    try:
        ticker = yf.Ticker(symbol if symbol.endswith(".BK") else symbol + ".BK")
        divs = ticker.dividends
        if divs.empty:
            return pd.DataFrame()
        df = divs.reset_index()
        df.columns = ["Date", "Dividend"]
        df["Date"] = pd.to_datetime(df["Date"])
        df["Year"] = df["Date"].dt.year
        df["Month"] = df["Date"].dt.month
        df["Symbol"] = symbol
        five_years = datetime.now().year - 5
        return df[df["Year"] >= five_years]
    except:
        return pd.DataFrame()
