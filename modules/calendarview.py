# modules/calendarview.py

import streamlit as st
import pandas as pd
from database import db
from modules.stock_data import get_dividends
from config import MONTH_LABELS

def show_xd_calendar():
    st.title("📆 XD Calendar - หุ้นในพอร์ต")

    raw_data = db.get_portfolio()
    if not raw_data:
        st.warning("ยังไม่มีหุ้นในพอร์ต")
        return

    df = pd.DataFrame(raw_data, columns=["symbol", "group", "sector", "avg_price", "quantity", "total_cost"])
    year = st.selectbox("เลือกปี", options=range(2020, 2026), index=5)  # default: 2025

    # เตรียมข้อมูล
    calendar = {month: [] for month in range(1, 13)}

    for symbol in df["symbol"]:
        div_df = get_dividends(symbol)
        if not div_df.empty:
            filtered = div_df[div_df["Year"] == year]
            for _, row in filtered.iterrows():
                month = row["Month"]
                calendar[month].append(f"{symbol} ({row['Dividend']:.2f})")

    # แสดงเป็นตาราง 3x4 (12 เดือน)
    cols = st.columns(4)
    for i in range(12):
        with cols[i % 4]:
            st.markdown(f"#### {MONTH_LABELS[i]}")
            if calendar[i + 1]:
                for stock in calendar[i + 1]:
                    st.markdown(f"- {stock}")
            else:
                st.markdown("_ไม่มีข้อมูล_")
