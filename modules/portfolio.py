# modules/portfolio.py

import streamlit as st
import pandas as pd
from database import db
from modules.stock_data import get_price, get_dividends
from visualization import plot_portfolio_pie
from config import MONTH_LABELS

def show_portfolio():
    st.title("📊 พอร์ตหุ้นของฉัน")

    # 🔹 แสดงตารางพอร์ต
    raw_data = db.get_portfolio()
    if not raw_data:
        st.info("ยังไม่มีหุ้นในพอร์ต กรุณาเพิ่มหุ้นก่อน")
        return

    df = pd.DataFrame(raw_data, columns=[
        "symbol", "group", "sector", "avg_price", "quantity", "total_cost"
    ])
    df["latest_price"] = df["symbol"].apply(get_price)
    df["market_value"] = df["latest_price"] * df["quantity"]
    df["gain_loss"] = df["market_value"] - df["total_cost"]

    # แสดง Pie Chart
    st.plotly_chart(plot_portfolio_pie(df), use_container_width=True)

    # ปุ่มลบหุ้น
    for idx, row in df.iterrows():
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"**{row['symbol']}** | {row['quantity']} หุ้น | ราคาซื้อเฉลี่ย: {row['avg_price']:.2f} บาท | กำไร/ขาดทุน: {row['gain_loss']:.2f}")
        with col2:
            if st.button("🗑️ ลบ", key=f"delete_{row['symbol']}"):
                db.delete_stock(row['symbol'])
                st.experimental_rerun()

    # ตารางสรุป
    st.markdown("### 📋 สรุปพอร์ต")
    st.dataframe(df[[
        "symbol", "avg_price", "latest_price", "quantity", "market_value", "gain_loss"
    ]].style.format({"avg_price": ".2f", "latest_price": ".2f", "market_value": ".2f", "gain_loss": ".2f"}))

    # 🔹 ปันผลย้อนหลังของหุ้นในพอร์ต
    st.subheader("📅 ปันผลย้อนหลังจากหุ้นในพอร์ต")
    all_div = []
    for symbol in df["symbol"]:
        div = get_dividends(symbol)
        if not div.empty:
            div["symbol"] = symbol
            all_div.append(div)

    if all_div:
        div_df = pd.concat(all_div)
        div_df = div_df[["symbol", "Date", "Dividend"]].sort_values(by="Date", ascending=False)
        st.dataframe(div_df)
    else:
        st.warning("ยังไม่มีข้อมูลปันผลย้อนหลังจากหุ้นในพอร์ต")
