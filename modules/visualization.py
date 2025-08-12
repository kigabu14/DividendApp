# modules/visualization.py
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

def summary_dashboard():
    st.header("📊 ภาพรวมพอร์ต")

    conn = sqlite3.connect("database/database.db", check_same_thread=False)
    df = pd.read_sql("SELECT * FROM portfolio", conn)

    if not df.empty:
        from modules.stock_data import get_price
        df['current'] = df['symbol'].apply(get_price)
        df['value'] = df['current'] * df['quantity']

        fig = px.pie(df, names='symbol', values='value', title='พอร์ตของคุณ',
                     hole=0.4)
        fig.update_traces(textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

        total = df['value'].sum()
        st.subheader(f"💰 มูลค่ารวมพอร์ต: {total:,.2f} บาท")
    else:
        st.warning("ยังไม่มีข้อมูลในพอร์ต")
