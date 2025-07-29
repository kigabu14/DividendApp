import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
from modules.db import get_all_stocks

def get_dividends(symbol: str) -> pd.DataFrame:
    try:
        stock = yf.Ticker(symbol + ".BK")  # ต่อ .BK สำหรับหุ้นไทย
        dividends = stock.dividends
        if dividends.empty:
            return pd.DataFrame()
        df = dividends.reset_index()
        df.columns = ["Date", "Dividend"]
        df["Date"] = pd.to_datetime(df["Date"])
        df["Month"] = df["Date"].dt.month
        df["Year"] = df["Date"].dt.year
        df["Symbol"] = symbol
        return df[df["Year"] >= datetime.now().year - 5]  # 5 ปีล่าสุด
    except Exception as e:
        st.warning(f"⚠️ ดึงข้อมูลไม่ได้สำหรับ {symbol}: {e}")
        return pd.DataFrame()

def show_calendar():
    st.subheader("📅 ปฏิทินปันผล (เฉพาะหุ้นที่คุณมีในพอร์ต)")

    # ดึงหุ้นจาก database
    df_port = get_all_stocks()
    if df_port.empty:
        st.info("❌ ยังไม่มีข้อมูลหุ้นในพอร์ต")
        return

    stock_list = df_port["symbol"].unique()

    # สร้าง dict เก็บหุ้นที่ปันผลในแต่ละเดือน
    calendar = {i: [] for i in range(1, 13)}  # 1-12 = Jan to Dec

    with st.spinner("🔄 กำลังโหลดข้อมูลปันผลย้อนหลัง..."):
        for symbol in stock_list:
            df_div = get_dividends(symbol)
            for month in df_div["Month"].unique():
                calendar[month].append(symbol)

    months_th = [
        "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
        "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."
    ]

    st.markdown("### 🗓 หุ้นที่คุณถือ จ่ายปันผลเดือนไหนบ้าง (ย้อนหลัง 5 ปี)")

    cols = st.columns(6)

    for i in range(12):
        with cols[i % 6]:
            st.markdown(f"#### {months_th[i]}")
            stocks = sorted(set(calendar[i + 1]))
            if stocks:
                for stock in stocks:
                    st.markdown(f"- {stock}")
            else:
                st.markdown("ไม่มี")
