# streamlit_app.py
import streamlit as st
from modules.portfolio import portfolio_page
from modules.dividend_tools import dca_calculator
from modules.calendar_view import xd_calendar
from modules.visualization import summary_dashboard

st.set_page_config(layout="wide", page_title="Dividend Tracker", page_icon="📈")

menu = st.sidebar.radio("📌 เลือกเมนู", ["📊 ภาพรวม", "📁 พอร์ต", "📅 ปฏิทิน XD", "🧮 ถัวเฉลี่ย (DCA)"])

if menu == "📊 ภาพรวม":
    summary_dashboard()

elif menu == "📁 พอร์ต":
    portfolio_page()

elif menu == "📅 ปฏิทิน XD":
    xd_calendar()

elif menu == "🧮 ถัวเฉลี่ย (DCA)":
    dca_calculator()
