import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
from modules.db import get_all_stocks

def get_dividends(symbol):
    try:
        stock = yf.Ticker(symbol + ".BK")  # สำหรับหุ้นไทย
        dividends = stock.dividends
        if dividends.empty:
            return pd.DataFrame()
        df = dividends.reset_index()
        df.columns = ["Date", "Dividend"]
        df = df[df["Date"].dt.year >= datetime.now().year - 5]  # 5 ปีล่าสุด
        df["Month"] = df["Date"].dt.month
        df["Year"] = df["Date"].dt.year
        df["Symbol"] = symbol
        return df
    except:
        return pd.DataFrame()

def show_calendar():
    st.subheader("📅 ปฏิทินปันผล (เฉพาะหุ้นที่คุณมี)")

    # ดึงรายการหุ้นจากพอร์ต
    df_port = get_all_stocks()
    if df_port.empty:
        st.info("⛔️ คุณยังไม่มีหุ้นในพอร์ต")
        return

    stock_list = df_port["symbol"].unique()

    # เตรียมโครงสร้างปฏิทิน
    calendar = {i: [] for i in range(1, 13)}  # 1-12 = Jan to Dec

    with st.spinner("🔄 กำลังดึงข้อมูลปันผล..."):
        for symbol in stock_list:
            div = get_dividends(symbol)
            for month in div["Month"].unique():
                calendar[month].append(symbol)

    # ชื่อเดือน
    months_th = [
        "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
        "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."
    ]
    cols = st.columns(6)

    for i in range(12):
        with cols[i % 6]:
            st.markdown(f"#### {months_th[i]}")
            unique_stocks = sorted(set(calendar[i + 1]))
            if unique_stocks:
                for stock in unique_stocks:
                    st.markdown(f"- {stock}")
            else:
                st.markdown("ไม่มี")
