import streamlit as st
import pandas as pd
from datetime import datetime
from config import DEFAULT_ANNUAL_GOAL
from modules.stock_data import get_dividends  # ฟังก์ชันดึงปันผลจาก yfinance
from visualization import plot_dividend_progress  # ใช้ gauge ที่มีอยู่แล้ว

# -------------------------------------------------
# Utility / Cache Layer
# -------------------------------------------------
@st.cache_data(show_spinner=False, ttl=60 * 30)  # cache 30 นาที
def load_dividend_history(symbol: str) -> pd.DataFrame:
    """
    ดึงข้อมูลปันผลของหุ้นหนึ่งตัว (ใช้ cache)
    คืน DataFrame คอลัมน์: Date, Dividend, Year, Month
    """
    df = get_dividends(symbol)
    if df is None or df.empty:
        return pd.DataFrame(columns=["Date", "Dividend", "Year", "Month"])
    return df

def format_money(v):
    try:
        return f"{v:,.2f}"
    except Exception:
        return "-"

# -------------------------------------------------
# Dashboard Dividend Summary
# -------------------------------------------------
def summary_dividend_chart(portfolio_df: pd.DataFrame, goal_amount: float = DEFAULT_ANNUAL_GOAL):
    st.subheader("📈 ความคืบหน้าของเป้าหมายปันผลรายปี")

    # กรณีไม่มีพอร์ต
    if portfolio_df is None or portfolio_df.empty:
        st.info("ยังไม่มีหุ้นในพอร์ต หรือยังไม่ได้เพิ่มข้อมูล")
        return

    required_cols = {"symbol", "quantity", "avg_price"}
    if not required_cols.issubset(portfolio_df.columns):
        st.error(f"ข้อมูลพอร์ตขาดคอลัมน์: {required_cols - set(portfolio_df.columns)}")
        return

    dividend_rows = []
    total_dividend_baht = 0.0

    with st.spinner("กำลังดึงข้อมูลปันผล..."):
        for _, row in portfolio_df.iterrows():
            symbol = str(row["symbol"]).strip()
            quantity = float(row.get("quantity", 0) or 0)
            avg_price = float(row.get("avg_price", 0) or 0)

            if not symbol:
                continue

            div_df = load_dividend_history(symbol)

            if div_df.empty:
                # แสดงแถวแจ้งว่าไม่มีปันผล (ถ้าต้องการข้ามก็เปลี่ยน continue)
                dividend_rows.append({
                    "หุ้น": symbol,
                    "จำนวน": quantity,
                    "ราคาซื้อเฉลี่ย": avg_price,
                    "เงินปันผล/หุ้น (ปีล่าสุด)": 0.0,
                    "รวมปันผล (ประเมิน)": 0.0,
                    "ผลตอบแทนต่อปี (%)": 0.0,
                    "รายการ (ปีล่าสุด)": "-"
                })
                continue

            # คำนวณเฉพาะ "ปีล่าสุดที่มีข้อมูล"
            latest_year = div_df["Year"].max()
            latest_year_df = div_df[div_df["Year"] == latest_year]

            annual_div_per_share = latest_year_df["Dividend"].sum()
            est_total = annual_div_per_share * quantity
            yield_percent = (annual_div_per_share / avg_price * 100) if avg_price > 0 else 0.0

            total_dividend_baht += est_total

            # อธิบายรายการของปีล่าสุด (วันที่ + จำนวน)
            items_desc = ", ".join(
                latest_year_df.sort_values("Date")["Dividend"].apply(lambda x: f"{x:.2f}").tolist()
            )

            dividend_rows.append({
                "หุ้น": symbol,
                "จำนวน": quantity,
                "ราคาซื้อเฉลี่ย": round(avg_price, 2),
                "เงินปันผล/หุ้น (ปีล่าสุด)": round(annual_div_per_share, 3),
                "รวมปันผล (ประเมิน)": round(est_total, 2),
                "ผลตอบแทนต่อปี (%)": round(yield_percent, 2),
                "รายการ (ปีล่าสุด)": items_desc if items_desc else "-"
            })

    if dividend_rows:
        df_show = pd.DataFrame(dividend_rows)
        st.dataframe(df_show, use_container_width=True)
    else:
        st.warning("ไม่พบข้อมูลปันผลของหุ้นในพอร์ตเลย")

    fig = plot_dividend_progress(total_dividend_baht, goal=goal_amount)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        f"💰 รวมปันผลที่ประเมิน (ปีล่าสุดของแต่ละหุ้น): "
        f"**{format_money(total_dividend_baht)} บาท**  | 🎯 เป้าหมาย: {format_money(goal_amount)}"
    )

    # เพิ่มส่วนสรุปย่อย
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("จำนวนหุ้นในพอร์ต", len(portfolio_df))
    with col2:
        st.metric("หุ้นที่มีปันผล", sum(1 for r in dividend_rows if r['เงินปันผล/หุ้น (ปีล่าสุด)'] > 0))
    with col3:
        progress_pct = (total_dividend_baht / goal_amount * 100) if goal_amount > 0 else 0
        st.metric("ความคืบหน้าเป้าหมาย (%)", f"{progress_pct:.2f}%")

# -------------------------------------------------
# DCA Calculator (พื้นฐาน)
# -------------------------------------------------
def dca_calculator():
    st.title("🧮 DCA Calculator")

    st.markdown("คำนวณการถัวเฉลี่ยต้นทุน (Dollar-Cost Averaging) และประเมินปันผลที่อาจได้รับ")

    symbol = st.text_input("หุ้น (เช่น PTT, ADVANC)").strip().upper()
    current_price = st.number_input("ราคาปัจจุบัน (บาท)", min_value=0.0, value=0.0, step=0.01)
    invest_per_period = st.number_input("จำนวนเงินต่อรอบ (บาท)", min_value=0.0, value=1000.0, step=100.0)
    freq_label = st.selectbox("ความถี่", ["รายเดือน (12x)", "รายสัปดาห์ (52x)", "รายไตรมาส (4x)", "ปีละครั้ง (1x)"])
    freq_map = {
        "รายเดือน (12x)": 12,
        "รายสัปดาห์ (52x)": 52,
        "รายไตรมาส (4x)": 4,
        "ปีละครั้ง (1x)": 1
    }
    periods = freq_map[freq_label]

    use_latest_div = st.checkbox("ใช้ปันผล/หุ้น จากปีล่าสุด (ถ้ามี)", value=True)
    manual_div = st.number_input("หรือระบุปันผลต่อหุ้นต่อปีเอง (บาท)", min_value=0.0, value=0.0, step=0.01)

    if st.button("คำนวณ"):
        if not symbol:
            st.warning("กรุณากรอกชื่อหุ้น")
            return
        if current_price <= 0:
            st.warning("กรุณาระบุราคาปัจจุบัน > 0")
            return
        if invest_per_period <= 0:
            st.warning("กรุณาระบุจำนวนเงินลงทุน > 0")
            return

        shares_per_period = invest_per_period / current_price
        total_shares_1y = shares_per_period * periods
        total_cost_1y = invest_per_period * periods

        annual_div_per_share = 0.0
        if use_latest_div:
            div_df = load_dividend_history(symbol)
            if not div_df.empty:
                latest_year = div_df["Year"].max()
                annual_div_per_share = div_df[div_df["Year"] == latest_year]["Dividend"].sum()
        if annual_div_per_share == 0 and manual_div > 0:
            annual_div_per_share = manual_div

        est_div_income_after_1y = total_shares_1y * annual_div_per_share
        forward_yield = (annual_div_per_share / current_price * 100) if current_price > 0 and annual_div_per_share > 0 else 0
        effective_yield_on_cost = (est_div_income_after_1y / total_cost_1y * 100) if total_cost_1y > 0 and est_div_income_after_1y > 0 else 0

        st.markdown("### ผลลัพธ์")
        st.write(f"- หุ้นต่อรอบ (ประมาณ): **{shares_per_period:.4f} หุ้น**")
        st.write(f"- หุ้นสะสมหลัง 1 ปี: **{total_shares_1y:.4f} หุ้น**")
        st.write(f"- เงินลงทุนรวม 1 ปี: **{format_money(total_cost_1y)} บาท**")
        st.write(f"- ปันผลต่อหุ้น (ปี): **{annual_div_per_share:.3f} บาท**")
        st.write(f"- ประเมินปันผลหลัง 1 ปี: **{format_money(est_div_income_after_1y)} บาท**")
        st.write(f"- Forward Yield (ต่อหุ้น): **{forward_yield:.2f}%**")
        st.write(f"- ผลตอบแทนปันผลเทียบเงินลงทุนปีแรก: **{effective_yield_on_cost:.2f}%**")

        st.info("หมายเหตุ: การคำนวณนี้เป็นการประเมินจากข้อมูลย้อนหลัง อาจไม่สะท้อนอนาคต")

# -------------------------------------------------
# (ออปชัน) ฟังก์ชันเสริม debug
# -------------------------------------------------
def debug_dividend(symbol: str):
    st.write(f"DEBUG: {symbol}")
    df = load_dividend_history(symbol)
    st.write(df.head())
