# modules/calendarview.py

import streamlit as st
import pandas as pd
import yfinance as yf
from database import db
from datetime import datetime

def get_dividend_history(symbol: str) -> pd.DataFrame:
    """
    Fetch dividend history for a SET symbol (Thai market) via yfinance.
    Returns a DataFrame with columns: date, dividend, symbol
    """
    try:
        stock = yf.Ticker(symbol + ".BK")
        div_series = stock.dividends  # This is a (possibly empty) Series indexed by date
        if div_series is None or div_series.empty:
            return pd.DataFrame(columns=["date", "dividend", "symbol"])
        df = div_series.reset_index()
        # After reset_index, columns are usually ['Date', 'Dividends'] but we standardize:
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

    symbols = [row[0] for row in portfolio]

    all_dividends: list[pd.DataFrame] = []
    for symbol in symbols:
        df_symbol = get_dividend_history(symbol)
        # Skip empty results so we don't end up with non-datetimelike dtypes later
        if not df_symbol.empty:
            all_dividends.append(df_symbol)

    if not all_dividends:
        st.warning("ไม่พบข้อมูลปันผล")
        return

    df = pd.concat(all_dividends, ignore_index=True)

    # Ensure date column is proper datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    if df.empty:
        st.warning("ไม่พบข้อมูลวันที่ปันผลที่ใช้งานได้")
        return

    # Derive calendar fields
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%B")

    # Aggregate dividend per symbol per month
    calendar = (
        df.groupby(["year", "month", "month_name", "symbol"], as_index=False)
          .agg(dividend=("dividend", "sum"))
    )

    # Sort chronologically (month_name alone would sort alphabetically)
    calendar = calendar.sort_values(["year", "month", "symbol"])

    st.subheader("สรุปปันผลรายเดือน")
    st.dataframe(calendar, use_container_width=True)

    # Optional: Pivot view (symbols as columns, months as rows)
    with st.expander("Pivot ดูแบบปฏิทิน (ทดลอง)"):
        pivot = (
            calendar
            .pivot_table(
                index=["year", "month", "month_name"],
                columns="symbol",
                values="dividend",
                aggfunc="sum",
                fill_value=0.0
            )
            .reset_index()
            .sort_values(["year", "month"])
        )
        # Combine year-month for display
        pivot["Year-Month"] = pivot["year"].astype(str) + "-" + pivot["month"].astype(str).str.zfill(2)
        display_cols = ["Year-Month", "month_name"] + [c for c in pivot.columns if c not in {"year", "month", "month_name", "Year-Month"}]
        st.dataframe(pivot[display_cols], use_container_width=True)
