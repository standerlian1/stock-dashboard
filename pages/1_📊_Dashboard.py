import streamlit as st
from src import SupabaseStockDB, create_candlestick_chart, STOCKS, is_market_hours, DARK_THEME

st.set_page_config(page_title="Stock Dashboard", page_icon="📈", layout="wide")

st.title("📈 Real-time Stock Dashboard")
st.markdown("**TSM • AAPL • NVDA • GSPC** - Live 30min updates")

# 1/6 vs 5/6 layout
col1, col2 = st.columns([1, 5])

with col1:
    st.header("📱 Stocks")
    selected_stock = st.radio("Select:", STOCKS, index=1)

with col2:
    db = SupabaseStockDB()
    df = db.get_latest_data(selected_stock)
    
    if not df.empty:
        fig = create_candlestick_chart(df, selected_stock)
        st.plotly_chart(fig, use_container_width=True)
        last_update = db.get_last_update(selected_stock)
        st.info(f"**Last updated**: {last_update}")
    else:
        st.warning("⏳ No data - check market hours")

