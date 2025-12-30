import streamlit as st
from src.database import SupabaseStockDB
from src.chart_builder import create_candlestick_chart

st.set_page_config(page_title="Stock Dashboard", layout="wide")

st.title("📈 Real-time Stock Dashboard")
stocks = ["AAPL", "NVDA", "TSM", "GSPC"]

# Sidebar (1/6 width)
with st.sidebar:
    st.header("📱 Stocks")
    selected_stock = st.radio("Select stock:", stocks, index=1)

db = SupabaseStockDB()
df = db.get_latest_data(selected_stock)

if not df.empty:
    fig = create_candlestick_chart(df, selected_stock)
    st.plotly_chart(fig, use_container_width=True)
    
    last_update = db.get_last_update(selected_stock)
    st.info(f"**Last updated**: {last_update}")
else:
    st.warning("⏳ Data loading... Check back during market hours (09:30-16:00 EST)")
