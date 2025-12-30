import streamlit as st
import plotly.graph_objects as go
from src import SupabaseStockDB, create_candlestick_chart, STOCKS, is_market_hours, DARK_THEME
from src.database import SupabaseStockDB
import time

st.set_page_config(
    page_title="Stock Dashboard", 
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for perfect dark theme + layout
st.markdown(f"""
    <style>
    .main .block-container {{
        padding-top: 1rem;
        background-color: {DARK_THEME['bg']};
    }}
    .css-1d391kg {{
        padding-top: 0rem;
    }}
    .css-1aumxhk {{
        background-color: {DARK_THEME['sidebar']};
    }}
    </style>
""", unsafe_allow_html=True)

# Header
st.title("📈 Real-time Stock Dashboard", anchor=False)
st.markdown("**TSM • AAPL • NVDA • GSPC** - Live 30min updates (09:30-16:00 NY Time)")

# Layout: Sidebar (stocks) + Main (chart)
col1, col2 = st.columns([1, 5])  # 1/6 vs 5/6 width

with col1:
    st.markdown("### 📱 Select Stock")
    selected_stock = st.radio(
        " ", 
        STOCKS, 
        index=1,
        label_visibility="collapsed",
        horizontal=False
    )

# Main chart area
with col2:
    db = SupabaseStockDB()
    df = db.get_latest_data(selected_stock)
    
    if not df.empty:
        fig = create_candlestick_chart(df, selected_stock)
        st.plotly_chart(fig, use_container_width=True)
        
        # Last update timestamp
        last_update = db.get_last_update(selected_stock)
        st.markdown(f"**🕐 Last updated**: {last_update}")
        
        if is_market_hours():
            st.success("✅ Live market data")
        else:
            st.info("💤 Market closed - showing latest data")
            
    else:
        st.markdown("### ⏳ No data yet")
        st.info("💡 Data updates every 30min during market hours (09:30-16:00 EST)")
        st.balloons()

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit + Supabase + yfinance*")
