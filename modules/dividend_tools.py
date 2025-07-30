def summary_dividend_chart(portfolio_df, goal_amount=DEFAULT_ANNUAL_GOAL):
    st.subheader("📈 ความคืบหน้าของเป้าหมายปันผลรายปี")
    
    dividend_data = []
    total_div = 0.0

    for _, row in portfolio_df.iterrows():
        symbol = row["symbol"]
        quantity = row["quantity"]
        avg_price = row["avg_price"]

        dividends_df = get_dividends(symbol)
        if dividends_df.empty:
            continue

        annual_div = dividends_df["Dividend"].sum()
        total = annual_div * quantity
        yield_percent = (annual_div / avg_price) * 100 if avg_price > 0 else 0

        dividend_data.append({
            "หุ้น": symbol,
            "จำนวน": quantity,
            "ราคาซื้อเฉลี่ย": avg_price,
            "เงินปันผล/หุ้น": round(annual_div, 2),
            "รวมปันผล": round(total, 2),
            "ผลตอบแทนต่อปี (%)": round(yield_percent, 2)
        })

        total_div += total

    # แสดงตาราง
    if dividend_data:
        df = pd.DataFrame(dividend_data)
        st.dataframe(df, use_container_width=True)

    # แสดงกราฟ
    fig = plot_dividend_progress(total_div, goal_amount)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"💰 รวมปันผลจากหุ้นทั้งหมด: **{total_div:,.2f} บาท**")
