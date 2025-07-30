import streamlit as st
import pandas as pd

from database.db import init_db
from database import db  # ✅ เพิ่มตรงนี้
from modules import portfolio, calendarview, dividend_tools, favorites

init_db()

# Layout & Theme
st.set_page_config(
    page_title="SET Dividend Tracker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.title("📌 เมนู")
page = st.sidebar.radio("ไปยังหน้า", [
    "🏠 Dashboard",
    "📊 Portfolio",
    "📅 XD Calendar",
    "🧮 DCA Calculator",
    "❤️ Favorites"
])

# ส่วนหลัก
if page == "🏠 Dashboard":
    portfolio.show_portfolio()
    
    data = [(s, g, se, ap, q, ap * q) for s, g, se, ap, q in db.get_portfolio()]
    portfolio_df = pd.DataFrame(
        data,
        columns=["symbol", "group", "sector", "avg_price", "quantity", "total_cost"]
    )

    dividend_tools.summary_dividend_chart(portfolio_df)  # ✅ เรียกฟังก์ชันให้ถูก

elif page == "📊 Portfolio":
    portfolio.show_portfolio()

elif page == "📅 XD Calendar":
    calendarview.show_xd_calendar()

elif page == "🧮 DCA Calculator":
    dividend_tools.dca_calculator()

elif page == "❤️ Favorites":
    favorites.show_favorites()
