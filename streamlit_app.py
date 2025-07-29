import streamlit as st
from modules.portfolio import portfolio_page
from modules.calendarview import show_calendar
from modules.dividend_tools import dca_calculator

st.set_page_config(layout="wide", page_title="Dividend Tracker", page_icon="📈")

menu = st.sidebar.radio("เมนู", ["📊 ภาพรวม", "📁 พอร์ต", "📅 ปฏิทิน XD", "🧮 ถัวเฉลี่ย (DCA)"])

if menu == "📊 ภาพรวม":
    st.header("📊 Dashboard: Portfolio + Dividend")
    portfolio_page(show_dividend=True)

elif menu == "📁 พอร์ต":
    portfolio_page(show_dividend=False)

elif menu == "📅 ปฏิทิน XD":
    show_calendar()

elif menu == "🧮 ถัวเฉลี่ย (DCA)":
    dca_calculator()
