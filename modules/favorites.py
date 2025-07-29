# modules/favorites.py

import streamlit as st
from database import db
from datetime import datetime
import yfinance as yf

def show_favorites():
    st.title("❤️ หุ้นที่ติดตาม")

    favorites = db.get_favorites()
    if not favorites:
        st.info("ยังไม่มีรายการโปรด")

    for symbol, note, added_at in favorites:
        col1, col2 = st.columns([5, 1])
        with col1:
            try:
                ticker = yf.Ticker(symbol + ".BK")
                info = ticker.info

                pe = info.get("trailingPE", "-")
                pbv = info.get("priceToBook", "-")
                dy = info.get("dividendYield", 0.0)
                if dy:
                    dy = round(dy * 100, 2)

                st.markdown(f"""
                **{symbol}**  
                📌 Note: {note}  
                📅 เพิ่มเมื่อ: {added_at}  
                - P/E: `{pe}`  
                - P/BV: `{pbv}`  
                - Dividend Yield: `{dy}%`
                """)
            except Exception as e:
                st.warning(f"ไม่สามารถโหลดข้อมูล {symbol}: {e}")
        with col2:
            if st.button("🗑️ ลบ", key=f"fav_delete_{symbol}"):
                db.delete_favorite(symbol)
                st.experimental_rerun()

    st.markdown("---")
    st.subheader("➕ เพิ่มหุ้นที่สนใจ")
    new_symbol = st.text_input("ชื่อหุ้น (เช่น PTT, CPALL)").upper()
    note = st.text_input("หมายเหตุ (เช่น ติดตามเพื่อซื้อ, ปันผลดี ฯลฯ)")

    if st.button("เพิ่มเข้ารายการโปรด"):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        db.add_favorite(new_symbol, note, now)
        st.success(f"เพิ่ม {new_symbol} แล้ว")
        st.experimental_rerun()
