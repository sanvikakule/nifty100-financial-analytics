import streamlit as st
import os

from dashboard_utils import (
    get_companies,
    get_company_metrics,
    get_peer_group,
    get_latest_year
)

st.set_page_config(
    page_title="Company Analysis",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Company Analysis")

# -----------------------------------------
# Company Selection
# -----------------------------------------

companies = get_companies()

selected = st.selectbox(
    "Select Company",
    companies
)

metrics = get_company_metrics(selected)

if metrics is None:
    st.error("No financial data available.")
    st.stop()

peer = get_peer_group(selected)

st.success(f"Peer Group : {peer}")

st.divider()

# -----------------------------------------
# Financial Highlights
# -----------------------------------------

st.subheader("📊 Financial Highlights")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "ROE",
        f"{metrics['return_on_equity_pct']:.2f}%"
    )

with col2:
    st.metric(
        "Net Profit Margin",
        f"{metrics['net_profit_margin_pct']:.2f}%"
    )

with col3:
    st.metric(
        "Operating Margin",
        f"{metrics['operating_profit_margin_pct']:.2f}%"
    )

with col4:
    st.metric(
        "Debt / Equity",
        f"{metrics['debt_to_equity']:.2f}"
    )

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "Interest Coverage",
        f"{metrics['interest_coverage']:.2f}"
    )

with col6:
    st.metric(
        "Asset Turnover",
        f"{metrics['asset_turnover']:.2f}"
    )

with col7:
    st.metric(
        "EPS",
        f"{metrics['earnings_per_share']:.2f}"
    )

with col8:
    st.metric(
        "Book Value",
        f"{metrics['book_value_per_share']:.2f}"
    )

st.divider()

# -----------------------------------------
# Company Details & Radar Chart
# -----------------------------------------

left, right = st.columns([1, 2])

with left:

    st.subheader("🏢 Company Details")

    st.write(f"**Company** : {selected}")
    st.write(f"**Peer Group** : {peer}")
    st.write(f"**Financial Year** : {metrics['year']}")

    st.write(f"**Free Cash Flow** : ₹ {metrics['free_cash_flow_cr']:.2f} Cr")
    st.write(f"**Cash From Operations** : ₹ {metrics['cash_from_operations_cr']:.2f} Cr")
    st.write(f"**Dividend Payout** : {metrics['dividend_payout_ratio_pct']:.2f}%")

with right:

    st.subheader("📈 Company vs Peer")

    image_path = (
        f"outputs/radar_charts/"
        f"{selected}_{metrics['year']}.png"
    )

    if os.path.exists(image_path):

        st.image(
            image_path,
            use_container_width=True
        )

    else:

        st.warning("Radar chart not found.")