# modules/stock_data.py
import yfinance as yf
import pandas as pd

def get_price(symbol: str) -> float:
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d")
        return round(hist["Close"].iloc[-1], 2)
    except:
        return 0.0

def get_dividends(symbol: str) -> pd.DataFrame:
    try:
        stock = yf.Ticker(symbol)
        divs = stock.dividends
        if divs.empty:
            return pd.DataFrame(columns=["Date", "Dividend"])
        df = divs.reset_index()
        df.columns = ["Date", "Dividend"]
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date", ascending=False)
        return df
    except Exception as e:
        return pd.DataFrame(columns=["Date", "Dividend"])
