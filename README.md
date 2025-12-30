# 📈 Stock Dashboard - Real-time TSM, AAPL, NVDA, GSPC

**Dark-themed, professional dashboard with live 30-minute candlestick updates (09:30-16:00 NY Time)**

[![Streamlit](https://img.shields.io/badge/Streamlit-Black?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![Supabase](https://img.shields.io/badge/Supabase-FB923C?style=for-the-badge&logo=supabase)](https://supabase.com)
[![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly)](https://plotly.com)

## ✨ **Features**
- **4 Stocks**: TSM, AAPL, NVDA, GSPC (S&P 500)
- **Live Updates**: Every 30min (09:30-16:00 NY Time)
- **Candlestick Charts**: Green/Red OHLC, zoom 30min→daily
- **3 Months History** + real-time data
- **Dark Theme**: Professional black/white design
- **Public Access**: No login required
- **Exact Timestamps**: "Last updated: 2025-01-15 14:23:17 EST"

## 📱 **Demo**
┌─────────────────────┬─────────────────────────────────────┐
│ TSM ✗ AAPL ✓ NVDA   │ [Interactive Candlestick Chart]     │
│ GSPC                │ Last updated: 2025-01-15 15:30 EST  │
└─────────────────────┴─────────────────────────────────────┘


 Copy code


## 🚀 **Live Demo**
**[Your Streamlit URL will appear here after deployment]**

## 🛠️ **Quick Setup (5 minutes)**

1. **Supabase**: [supabase.com](https://supabase.com) → New Project → Copy URL + anon key
2. **Deploy**: Connect GitHub repo to [share.streamlit.io](https://share.streamlit.io)
3. **Secrets**: Add `SUPABASE_URL` + `SUPABASE_ANON_KEY` to Streamlit settings

## 📊 **Tech Stack**
Frontend: Streamlit + Plotly
Backend: yfinance + APScheduler
Database: Supabase PostgreSQL
Deployment: Streamlit Cloud


 Copy code


## 🔧 **Local Development**
ash
pip install -r requirements.txt
cp secrets.toml.example .streamlit/secrets.toml
streamlit run pages/1_📊_Dashboard.py


 Copy code


---
**Built with ❤️ for real-time stock analysis**
