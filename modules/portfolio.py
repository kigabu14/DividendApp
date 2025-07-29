import streamlit as st
import pandas as pd
from datetime import datetime
from modules.db import get_conn
from modules.stock_data import get_price, get_dividends

SET100 = ["AOT", "PTT", "SCB", "BBL", "KBANK", "CPALL", "GULF", "ADVANC"]  # เพิ่มเติมได้

def portfolio_page(show_dividend=False):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
      CREATE TABLE IF NOT EXISTS portfolio (
        symbol TEXT,
        buy_price REAL,
        quantity INTEGER,
        buy_date TEXT
      )
    """)
    conn.commit()

    with st.expander("➕ เพิ่มหุ้นในพอร์ต"):
        symbol = st.selectbox("เลือกหุ้นจาก SET100", SET100)
        price = st.number_input("ราคาซื้อ (บาท)", min_value=0.0)
        qty = st.number_input("จำนวนหุ้น", min_value=1, step=1)
        if st.button("บันทึก"):
            c.execute("INSERT INTO portfolio VALUES (?, ?, ?, ?)",
                      (symbol, price, qty, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            st.success("✅ บันทึกเรียบร้อย")

    df = pd.read_sql("SELECT * FROM portfolio", conn)
    if df.empty:
        st.info("ยังไม่มีหุ้นในพอร์ต")
        return

    df["current_price"] = df["symbol"].apply(get_price)
    df["market_value"] = df["current_price"] * df["quantity"]
    df["cost"] = df["buy_price"] * df["quantity"]
    df["profit_loss"] = df["market_value"] - df["cost"]

    st.dataframe(df[["symbol", "buy_price", "quantity", "current_price", "market_value", "profit_loss"]])

    if show_dividend:
        total_div = 0
        st.subheader("📈 ปันผลย้อนหลังจากหุ้นในพอร์ต")
        for sym in df["symbol"].unique():
            div = get_dividends(sym)
            if not div.empty:
                st.markdown(f"## {sym}")
                st.dataframe(div[["Date", "Dividend"]])
                total_div += div["Dividend"].sum()
                st.write(f"รวมปันผลของ {sym}: {div['Dividend'].sum():.2f} บาท")
        st.success(f"💰 รวมปันผลย้อนหลังทั้งหมด: {total_div:.2f} บาท")
