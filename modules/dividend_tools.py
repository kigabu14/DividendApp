# modules/dividend_tools.py (ต่อจาก DCA)
import pandas as pd
from modules.stock_data import get_dividends

    st.subheader("📆 ปันผลย้อนหลัง (จาก Yahoo Finance)")
    symbol = st.text_input("ใส่ชื่อหุ้น เช่น PTT.BK", "PTT.BK")
    if st.button("แสดงปันผลย้อนหลัง"):
        df = get_dividends(symbol)
        if df.empty:
            st.warning("ไม่พบข้อมูลปันผล")
        else:
            st.dataframe(df)
