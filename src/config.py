"""Configuration for Stock Dashboard"""
import pytz
from datetime import time
from typing import List, Tuple

# Stock symbols
STOCKS = ["TSM", "AAPL", "NVDA", "GSPC"]

# Market hours (NY Time)
MARKET_OPEN = time(9, 30)
MARKET_CLOSE = time(16, 0)
TIMEZONE = pytz.timezone('US/Eastern')

# Data settings
INTERVAL_30MIN = "30m"
INTERVAL_1DAY = "1d"
HISTORICAL_DAYS = 90
FETCH_LIMIT_PER_DAY = 20  # Max candles per day

# Theme colors
DARK_THEME = {
    'bg': '#0e1117',
    'sidebar': '#1a1a1e',
    'card': '#262730',
    'text': '#FAFAFA',
    'green': '#00D4AA',
    'red': '#FF6B6B'
}

def is_market_hours() -> bool:
    """Check if current time is within market hours (Mon-Fri, 09:30-16:00 NY)"""
    now_ny = datetime.now(TIMEZONE)
    if now_ny.weekday() >= 5:  # Weekend
        return False
    current_time = now_ny.time()
    return MARKET_OPEN <= current_time <= MARKET_CLOSE

