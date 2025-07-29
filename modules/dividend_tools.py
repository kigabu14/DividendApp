# modules/dividend_tools.py

import streamlit as st
from modules.stock_data import get_price, get_dividends
from config import DEFAULT_ANNUAL_GOAL
from visualization import plot_dividend_progress
import pandas as pd

def dca_calculator():
    st.subheader("🧮 เครื่องคำนวณถัวเฉลี่ย (DCA)")

    symbol = st.text_input("ชื่อหุ้น (เช่น PTT, SCB)", value="PTT").upper()
    old_price = st.number_input("ราคาซื้อเดิม", min_value=0.0)
    old_qty = st.number_input("จำนวนหุ้นเดิม", min_value=0)
    new_qty = st.number_input("จำนวนที่จะซื้อเพิ่ม", min_value=0)

    if st.button("คำนวณ"):
        current_price = get_price(symbol)
        total_cost = (old_price * old_qty) + (current_price * new_qty)
        total_qty = old_qty + new_qty

        if total_qty == 0:
            st.warning("❗ ต้องมีจำนวนหุ้นรวมมากกว่า 0")
            return

        avg_price = total_cost / total_qty
        st.success(f"📌 ราคาถัวเฉลี่ยใหม่: {avg_price:.2f} บาท")
        st.caption(f"(ราคาปัจจุบัน: {current_price:.2f} บาท)")

def summary_dividend_chart(portfolio_df, goal_amount=DEFAULT_ANNUAL_GOAL):
    st.subheader("📈 ความคืบหน้าของเป้าหมายปันผลรายปี")
    total_div = 0.0

    for symbol in portfolio_df["symbol"].unique():
        div = get_dividends(symbol)
        if not div.empty:
            total_div += div["Dividend"].sum() * \
                         portfolio_df[portfolio_df["symbol"] == symbol]["quantity"].iloc[0]

    fig = plot_dividend_progress(total_div, goal_amount)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"💰 รวมปันผลจากหุ้นทั้งหมด: **{total_div:,.2f} บาท**")
