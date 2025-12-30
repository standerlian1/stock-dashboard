import streamlit as st
from src.data_fetcher import fetch_and_store_stocks

st.title("🔄 Data Updater (Admin)")
if st.button("🔔 Update All Stocks Now"):
    with st.spinner("Fetching live data..."):
        fetch_and_store_stocks()
    st.success("✅ Data updated successfully!")
