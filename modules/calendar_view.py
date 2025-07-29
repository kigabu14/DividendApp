# modules/calendar_view.py
import streamlit as st
import pandas as pd

def xd_calendar():
    st.header("📅 XD Calendar")
    st.write("📌 *ข้อมูลนี้จำลองไว้ สามารถเชื่อมจริงได้ในเวอร์ชันถัดไป*")
    data = {
        "symbol": ["PTT.BK", "AOT.BK", "SCB.BK"],
        "xd_date": ["2025-08-15", "2025-09-01", "2025-09-20"],
        "dividend": [1.5, 2.0, 2.25],
    }
    df = pd.DataFrame(data)
    df["xd_date"] = pd.to_datetime(df["xd_date"])
    df = df.sort_values("xd_date")
    st.dataframe(df)
