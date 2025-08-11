import streamlit as st
import pandas as pd
from math import floor

# Ensure these helpers/constants exist or adjust as needed
DEFAULT_ANNUAL_GOAL = 10000  # Example fallback
def get_dividends(symbol: str) -> pd.DataFrame:
    # TODO: Replace with your real implementation
    return pd.DataFrame(columns=["ExDate", "Dividend"])

def plot_dividend_progress(total_div, goal_amount):
    import plotly.graph_objects as go
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=total_div,
        gauge={'axis': {'range': [0, goal_amount]}},
        title={'text': 'Annual Dividend Progress'}
    ))
    return fig

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

    if dividend_data:
        df = pd.DataFrame(dividend_data)
        st.dataframe(df, use_container_width=True)

    fig = plot_dividend_progress(total_div, goal_amount)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"💰 รวมปันผลจากหุ้นทั้งหมด: **{total_div:,.2f} บาท**")

def dca_calculator():
    st.subheader("🧮 DCA (Dollar-Cost Averaging) Calculator")

    # Inputs
    symbol = st.text_input("Stock Symbol (e.g., ADVANC)", value="")
    current_price = st.number_input("Current Price (THB)", min_value=0.0, value=0.0, step=0.01)
    periodic_amount = st.number_input("Investment Amount per Period (THB)", min_value=0.0, value=1000.0, step=100.0)
    periods_per_year = st.selectbox("Frequency", [
        ("Monthly (12x)", 12),
        ("Bi-Weekly (~26x)", 26),
        ("Weekly (52x)", 52),
        ("Quarterly (4x)", 4),
        ("Annually (1x)", 1)
    ], format_func=lambda x: x[0])[1]

    use_dividend_lookup = st.checkbox("Fetch estimated annual dividend per share from history (if available)", value=True)
    manual_dividend = st.number_input("OR manual expected annual dividend per share (THB)", min_value=0.0, value=0.0, step=0.01)

    if st.button("Calculate"):
        if not symbol:
            st.warning("Please enter a symbol.")
            return
        if current_price <= 0:
            st.warning("Current price must be greater than 0.")
            return
        if periodic_amount <= 0:
            st.warning("Investment amount must be greater than 0.")
            return

        shares_per_period = periodic_amount / current_price
        total_shares_year = shares_per_period * periods_per_year
        total_invested_year = periodic_amount * periods_per_year

        if use_dividend_lookup:
            div_df = get_dividends(symbol)
            if not div_df.empty and "Dividend" in div_df.columns:
                annual_div_per_share = div_df["Dividend"].sum()
            else:
                annual_div_per_share = manual_dividend
        else:
            annual_div_per_share = manual_dividend

        est_annual_div_income = total_shares_year * annual_div_per_share if annual_div_per_share else 0.0
        forward_yield = (annual_div_per_share / current_price * 100) if current_price > 0 and annual_div_per_share else 0.0
        effective_yield_on_invested = (est_annual_div_income / total_invested_year * 100) if total_invested_year > 0 and est_annual_div_income else 0.0

        st.markdown("### Results")
        st.write(f"Shares purchased per period: **{shares_per_period:.4f}**")
        st.write(f"Estimated shares accumulated in 1 year: **{total_shares_year:.4f}**")
        st.write(f"Total invested in 1 year: **{total_invested_year:,.2f} THB**")
        st.write(f"Annual dividend per share (estimated): **{annual_div_per_share:.2f} THB**")
        st.write(f"Estimated annual dividend income after 1 year: **{est_annual_div_income:,.2f} THB**")
        st.write(f"Forward yield (% of current price): **{forward_yield:.2f}%**")
        st.write(f"Effective yield on first-year invested capital: **{effective_yield_on_invested:.2f}%**")
