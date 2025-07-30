# modules/calendarview.py

import streamlit as st
import pandas as pd
import yfinance as yf
from database import db
from datetime import datetime

def get_dividend_history(symbol):
    try:
        stock = yf.Ticker(symbol + '.BK')
        df = stock.dividends
        df = df.reset_index()
        df.columns = ["date", "dividend"]
        df["symbol"] = symbol
        return df
    except Exception as e:
        st.warning(f"ดึงข้อมูล {symbol} ไม่สำเร็จ: {e}")
        return pd.DataFrame(columns=["date", "dividend", "symbol"])

def show_xd_calendar():
    st.title("📅 XD Calendar")

    portfolio = db.get_portfolio()
    if not portfolio:
        st.info("ยังไม่มีหุ้นในพอร์ต กรุณาเพิ่มหุ้นก่อน")
        return

    # เอา symbol จากพอร์ต
    symbols = [row[0] for row in portfolio]

    all_dividends = []
    for symbol in symbols:
        df = get_dividend_history(symbol)
        all_dividends.append(df)

    if not all_dividends:
        st.warning("ไม่พบข้อมูลปันผล")
        return

    df = pd.concat(all_dividends)
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    df["month_name"] = df["date"].dt.strftime("%B")

    # group by calendar
    calendar = df.groupby(["year", "month_name", "symbol"]).agg({"dividend": "sum"}).reset_index()

    st.dataframe(calendar.sort_values(by=["year", "month_name"]))
