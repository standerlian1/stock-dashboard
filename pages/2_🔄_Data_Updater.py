import streamlit as st
from src import fetch_and_store_stocks, is_market_hours, STOCKS
import pandas as pd

st.set_page_config(page_title="Data Updater", layout="wide")

st.title("🔄 Data Updater (Admin)")
st.markdown("**Manual trigger for all stocks**")

if st.button("🔥 UPDATE ALL STOCKS NOW", type="primary", use_container_width=True):
    with st.spinner("🚀 Fetching live data from Yahoo Finance..."):
        success_count = fetch_and_store_stocks()
    
    if success_count > 0:
        st.success(f"✅ **SUCCESS**: Updated {success_count}/{len(STOCKS)} stocks!")
        st.balloons()
    else:
        st.error("❌ No data updated. Check market hours (09:30-16:00 EST)")

# Status
col1, col2 = st.columns(2)
with col1:
    market_open = is_market_hours()
    status = "🟢 OPEN" if market_open else "🔴 CLOSED"
    st.metric("Market Status", status)

with col2:
    st.metric("Auto-updates", "Every 30min")

st.info("💡 This page auto-runs during market hours. Use manual button for testing.")
