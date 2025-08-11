import streamlit as st
import pandas as pd

from config import DEFAULT_ANNUAL_GOAL
from modules.stock_data import get_dividends
from visualization import plot_dividend_progress


def summary_dividend_chart(portfolio_df: pd.DataFrame, goal_amount: float | None = None):
    """
    สรุปความคืบหน้าปันผลเทียบเป้าหมายประจำปี พร้อมตารางรายละเอียดรายหุ้น
    :param portfolio_df: DataFrame ต้องมีคอลัมน์ symbol, quantity, avg_price
    :param goal_amount: เป้าหมายปันผลทั้งปี (บาท). ถ้าไม่ส่งมาใช้ DEFAULT_ANNUAL_GOAL
    """
    if goal_amount is None:
        goal_amount = DEFAULT_ANNUAL_GOAL

    st.subheader("📈 ความคืบหน้าของเป้าหมายปันผลรายปี")

    required_cols = {"symbol", "quantity", "avg_price"}
    missing = required_cols - set(portfolio_df.columns)
    if missing:
        st.error(f"ขาดคอลัมน์ที่จำเป็น: {', '.join(missing)}")
        return

    dividend_data = []
    total_div = 0.0

    for _, row in portfolio_df.iterrows():
        symbol = row["symbol"]
        quantity = row["quantity"]
        avg_price = row["avg_price"]

        dividends_df = get_dividends(symbol)
        if dividends_df.empty:
            continue

        # รวมเงินปันผลทั้งปีต่อ 1 หุ้น
        annual_div = dividends_df["Dividend"].sum()

        total_for_symbol = annual_div * quantity
        yield_percent = (annual_div / avg_price) * 100 if avg_price > 0 else 0

        dividend_data.append({
            "หุ้น": symbol,
            "จำนวน": quantity,
            "ราคาซื้อเฉลี่ย": round(float(avg_price), 2),
            "เงินปันผล/หุ้น": round(float(annual_div), 2),
            "รวมปันผล": round(float(total_for_symbol), 2),
            "ผลตอบแทนต่อปี (%)": round(float(yield_percent), 2),
        })

        total_div += total_for_symbol

    # แสดงตาราง
    if dividend_data:
        df = pd.DataFrame(dividend_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("ยังไม่มีข้อมูลปันผลที่ดึงมาได้")

    # แสดงกราฟและสรุป
    fig = plot_dividend_progress(total_div, goal_amount)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"💰 รวมปันผลจากหุ้นทั้งหมด: **{total_div:,.2f} บาท** / เป้าหมาย {goal_amount:,.0f} บาท "
                f"({(total_div/goal_amount*100 if goal_amount else 0):.2f}%)")
