import streamlit as st
import plotly.graph_objects as go
from src import SupabaseStockDB, create_candlestick_chart, STOCKS, is_market_hours, DARK_THEME, TIMEZONE
from src.database import SupabaseStockDB
import pandas as pd

st.set_page_config(
    page_title="Stock Dashboard", 
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 1rem;
        background-color: #0e1117;
        color: #FAFAFA;
    }
    [data-testid="stSidebar"] {
        background-color: #1a1a1e;
    }
    .stRadio > div > div {
        background-color: #262730;
        color: #FAFAFA;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("📈 Real-time Stock Dashboard")
st.markdown("**TSM • AAPL • NVDA • GSPC** - Live 30min updates (09:30-16:00 NY Time)")

# Layout: 1/6 sidebar vs 5/6 main chart
col1, col2 = st.columns([1, 5])

with col1:
    st.header("📱 Stocks")
    selected_stock = st.radio(
        "Select stock:", 
        STOCKS, 
        index=1,
        label_visibility="collapsed"
    )

# Main chart area (5/6 width)
with col2:
    try:
        db = SupabaseStockDB()
        df = db.get_latest_data(selected_stock)
        
        if not df.empty:
            fig = create_candlestick_chart(df, selected_stock)
            st.plotly_chart(fig, use_container_width=True, height=600)
            
            # Last update timestamp
            last_update = db.get_last_update(selected_stock)
            st.markdown(f"**🕐 Last updated**: {last_update}")
            
            # Market status
            if is_market_hours():
                st.success("✅ Live market data - updates every 30min")
            else:
                st.info("💤 Market closed - showing latest available data")
                
        else:
            st.markdown("### ⏳ No data available")
            st.info("💡 Data loads during market hours (09:30-16:00 EST)\nUse **Data Updater** page to fetch initial data")
            
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Please check Data Updater page and Supabase connection")

# Footer
st.markdown("---")
st.markdown("*Dark theme candlestick dashboard • Powered by Streamlit + Supabase + yfinance*")

