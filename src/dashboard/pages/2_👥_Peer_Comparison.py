import streamlit as st
import plotly.express as px

from dashboard_utils import (
    get_companies,
    get_peer_comparison,
    get_peer_group
)

st.set_page_config(
    page_title="Peer Comparison",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Peer Comparison")

# ==========================
# Company Selection
# ==========================

companies = get_companies()

company = st.selectbox(
    "Select Company",
    companies
)

peer_group = get_peer_group(company)

st.success(f"Peer Group: {peer_group}")

# ==========================
# Load Data
# ==========================

df = get_peer_comparison(company)

if df.empty:
    st.warning("No peer comparison data found.")
    st.stop()

# ==========================
# Year Filter
# ==========================

years = sorted(df["year"].unique(), reverse=True)

selected_year = st.selectbox(
    "Select Year",
    years
)

plot_df = df[df["year"] == selected_year].copy()

# ==========================
# Metric Name Mapping
# ==========================

metric_map = {
    "net_profit_margin_pct": "Net Profit Margin",
    "operating_profit_margin_pct": "Operating Margin",
    "return_on_equity_pct": "ROE",
    "debt_to_equity": "Debt / Equity",
    "interest_coverage": "Interest Coverage",
    "asset_turnover": "Asset Turnover",
    "free_cash_flow_cr": "Free Cash Flow",
    "earnings_per_share": "EPS",
    "book_value_per_share": "Book Value",
    "dividend_payout_ratio_pct": "Dividend Payout",
    "cash_from_operations_cr": "Cash Flow"
}

plot_df["Metric"] = plot_df["metric"].map(metric_map).fillna(plot_df["metric"])

# ==========================
# KPI Cards
# ==========================

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Peer Group",
        peer_group
    )

with c2:
    st.metric(
        "Metrics",
        len(plot_df)
    )

with c3:
    st.metric(
        "Average Percentile",
        f"{plot_df['percentile'].mean():.1f}%"
    )

st.divider()

# ==========================
# Company vs Peer Average
# ==========================

st.subheader("📊 Company vs Peer Average")

fig = px.bar(
    plot_df,
    x="Metric",
    y=["value", "peer_average"],
    barmode="group",
    title=f"{company} vs Peer Average ({selected_year})",
    labels={
        "value": company,
        "peer_average": "Peer Average"
    }
)

fig.update_layout(
    height=600,
    xaxis_title="Financial Metric",
    yaxis_title="Value",
    legend_title="",
    xaxis_tickangle=-30
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# Percentile Chart
# ==========================

st.subheader("🏆 Percentile Ranking")

fig2 = px.bar(
    plot_df,
    x="Metric",
    y="percentile",
    title=f"{company} Percentile Ranking ({selected_year})"
)

fig2.update_layout(
    height=450,
    yaxis_range=[0, 100],
    xaxis_tickangle=-30,
    xaxis_title="Financial Metric",
    yaxis_title="Percentile"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================
# Comparison Table
# ==========================

st.subheader("📋 Comparison Table")

display_df = plot_df[
    [
        "Metric",
        "value",
        "peer_average",
        "percentile"
    ]
].rename(
    columns={
        "value": company,
        "peer_average": "Peer Average",
        "percentile": "Percentile"
    }
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# ==========================
# Download Button
# ==========================

st.download_button(
    label="📥 Download Comparison CSV",
    data=display_df.to_csv(index=False),
    file_name=f"{company}_peer_comparison_{selected_year}.csv",
    mime="text/csv"
)