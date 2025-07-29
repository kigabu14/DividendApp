import streamlit as st
from modules.stock_data import get_price

def dca_calculator():
    st.header("🧮 เครื่องคำนวณถัวเฉลี่ย (DCA)")
    symbol = st.text_input("ชื่อหุ้น (เช่น PTT)", value="PTT")
    old_price = st.number_input("ราคาซื้อเดิม", min_value=0.0)
    old_qty = st.number_input("จำนวนเดิม", min_value=0)
    new_qty = st.number_input("จำนวนที่จะซื้อเพิ่ม", min_value=0)
    if st.button("คำนวณ DCA"):
        current = get_price(symbol)
        total = old_price * old_qty + current * new_qty
        qty = old_qty + new_qty
        avg = total / qty if qty > 0 else 0
        st.success(f"ราคาถัวเฉลี่ยใหม่: {avg:.2f} บาท")
