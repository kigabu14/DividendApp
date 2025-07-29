# modules/portfolio.py
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from modules.stock_data import get_price
from modules.config import SET100

def portfolio_page():
    st.header("📁 พอร์ตหุ้นปันผล")

    conn = sqlite3.connect("data/dividend_data.db", check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS portfolio
                 (symbol TEXT, price REAL, quantity INTEGER, date TEXT)''')

    with st.expander("➕ เพิ่มหุ้นเข้าพอร์ต"):
        symbol = st.selectbox("เลือกหุ้นจาก SET100", SET100)
        price = st.number_input("ราคาซื้อ (บาท)", min_value=0.0)
        qty = st.number_input("จำนวนหุ้น", min_value=1, step=1)
        add = st.button("บันทึก")
        if add:
            c.execute("INSERT INTO portfolio VALUES (?, ?, ?, ?)",
                      (symbol, price, qty, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            st.success("✅ บันทึกเรียบร้อย")

    df = pd.read_sql("SELECT * FROM portfolio", conn)
    if not df.empty:
        df['current'] = df['symbol'].apply(get_price)
        df['total_cost'] = df['price'] * df['quantity']
        df['market_value'] = df['current'] * df['quantity']
        df['pnl'] = df['market_value'] - df['total_cost']
        st.dataframe(df)
    else:
        st.info("ยังไม่มีหุ้นในพอร์ต")
