import streamlit as st
import pandas as pd
from database import db
import yfinance as yf

@st.cache_data
def get_set100_symbols():
    # ดึงจากเว็บ Yahoo Finance ที่ลิสต์ SET100 จริง (แบบ manual)
    set100 = [
        "ADVANC.BK", "AOT.BK", "BANPU.BK", "BBL.BK", "BDMS.BK", "BGRIM.BK", "BH.BK", "BJC.BK", "BTS.BK",
        "CBG.BK", "CENTEL.BK", "COM7.BK", "CPALL.BK", "CPF.BK", "CPN.BK", "DELTA.BK", "DOHOME.BK", "DTAC.BK",
        "EGCO.BK", "GLOBAL.BK", "GPSC.BK", "GULF.BK", "HMPRO.BK", "INTUCH.BK", "IRPC.BK", "IVL.BK", "JMART.BK",
        "KBANK.BK", "KCE.BK", "KTB.BK", "KTC.BK", "LH.BK", "M.BK", "MEGA.BK", "MINT.BK", "MTC.BK", "OR.BK",
        "OSP.BK", "PLANB.BK", "PRM.BK", "PTG.BK", "PTT.BK", "PTTEP.BK", "PTTGC.BK", "RATCH.BK", "SAWAD.BK",
        "SCB.BK", "SCC.BK", "SCGP.BK", "SPRC.BK", "STA.BK", "STARK.BK", "STEC.BK", "STGT.BK", "SUPER.BK",
        "TIDLOR.BK", "TISCO.BK", "TKN.BK", "TMB.BK", "TOP.BK", "TRUE.BK", "TU.BK", "VGI.BK", "WHA.BK"
    ]
    return set100

def show_portfolio():
    st.title("📊 พอร์ตหุ้นของฉัน")

    # 🔹 เพิ่มหุ้นเข้าพอร์ต
    st.subheader("➕ เพิ่มหุ้นเข้าพอร์ต")

    all_symbols = get_set100_symbols()

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_symbol = st.selectbox("เลือกหุ้น (SET100)", all_symbols)
    with col2:
        avg_price = st.number_input("ราคาเฉลี่ย", min_value=0.01, step=0.1)
    with col3:
        quantity = st.number_input("จำนวน (หุ้น)", min_value=1, step=1)

    if st.button("➕ เพิ่มหุ้น"):
        db.add_to_portfolio(
            symbol=selected_symbol,
            group="SET100",
            sector="-",
            avg_price=avg_price,
            quantity=quantity
        )
        st.success(f"เพิ่ม {selected_symbol} เข้าพอร์ตแล้ว!")

    # 🔸 แสดงพอร์ต
    raw_data = db.get_portfolio()
    if raw_data:
        df = pd.DataFrame(raw_data, columns=["Symbol", "Group", "Sector", "Avg Price", "Quantity"])
        st.dataframe(df, use_container_width=True)

        st.subheader("🗑 ลบหุ้นออกจากพอร์ต")
        symbol_to_delete = st.selectbox("เลือกหุ้นที่ต้องการลบ", options=df["Symbol"].tolist())
        if st.button("🗑 ลบหุ้นนี้"):
            db.delete_from_portfolio(symbol_to_delete)
            st.success(f"ลบหุ้น {symbol_to_delete} เรียบร้อยแล้ว!")
    else:
        st.info("ยังไม่มีหุ้นในพอร์ต กรุณาเพิ่มหุ้นก่อน")
