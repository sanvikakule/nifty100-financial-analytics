import streamlit as st
from dashboard_utils import (
    get_company_count,
    get_peer_group_count,
    get_latest_year,
    get_metric_count
)

st.set_page_config(
    page_title="Nifty100 Financial Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.title("📈 Nifty100 Analytics")
st.sidebar.markdown("---")
st.sidebar.success("Sprint 4 Dashboard")

# Main Title
st.title("📈 Nifty100 Financial Analytics Platform")
st.markdown("### AI-Powered Financial Analysis & Stock Screening")

st.divider()

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Companies", get_company_count())

with col2:
    st.metric("Peer Groups", get_peer_group_count())

with col3:
    st.metric("Financial Metrics", get_metric_count())

with col4:
    st.metric("Latest Year", get_latest_year())

st.divider()

st.subheader("Project Overview")

st.write("""
This platform provides:

- Financial Ratio Analysis
- Peer Comparison
- Stock Screeners
- Composite Scoring
- Radar Chart Visualization
- Excel Reports
- Analytics Dashboard
""")

st.info("Database integration will be added in the next step.")