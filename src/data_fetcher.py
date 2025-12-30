"""Fetch stock data from yfinance and prepare for database"""
import yfinance as yf
import pandas as pd
import pytz
from datetime import datetime, timedelta
from src.config import STOCKS, TIMEZONE, HISTORICAL_DAYS, INTERVAL_30MIN, INTERVAL_1DAY

def fetch_stock_data(symbol: str, days: int = 90) -> pd.DataFrame:
    """Fetch intraday + historical data for symbol"""
    try:
        ticker = yf.Ticker(symbol)
        
        # Get historical daily data (3 months)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        hist_daily = ticker.history(start=start_date, end=end_date, interval=INTERVAL_1DAY)
        
        # Get intraday 30min data (last 60 days max for yfinance)
        hist_intraday = ticker.history(period="60d", interval=INTERVAL_30MIN)
        
        # Combine and clean
        if not hist_intraday.empty:
            df = pd.concat([hist_intraday, hist_daily]).drop_duplicates()
        else:
            df = hist_daily
        
        df = df.sort_index()
        df = df.reset_index()
        df = df.rename(columns={
            'Datetime': 'timestamp',
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        })
        
        return df
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return pd.DataFrame()

def prepare_db_data(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    """Convert DataFrame to database format with NY timezone"""
    if df.empty:
        return df
    
    ny_tz = TIMEZONE
    df['timestamp_ny'] = df['timestamp'].dt.tz_convert(ny_tz)
    df['date'] = df['timestamp_ny'].dt.date
    df['time'] = df['timestamp_ny'].dt.time
    df['fetch_timestamp'] = datetime.now(pytz.UTC)
    df['symbol'] = symbol
    
    # Select and reorder columns
    db_cols = ['symbol', 'date', 'time', 'fetch_timestamp', 'open', 'high', 'low', 'close', 'volume']
    df_db = df[db_cols].copy()
    
    # Round prices to 4 decimals
    price_cols = ['open', 'high', 'low', 'close']
    df_db[price_cols] = df_db[price_cols].round(4)
    
    # Filter market hours only (09:30-16:00)
    df_db = df_db[df_db['time'] >= pd.to_datetime('09:30').time()]
    df_db = df_db[df_db['time'] <= pd.to_datetime('16:00').time()]
    
    return df_db

def fetch_and_store_stocks():
    """Fetch and store ALL stocks"""
    from src.database import SupabaseStockDB
    
    db = SupabaseStockDB()
    success_count = 0
    
    for symbol in STOCKS:
        try:
            print(f"Fetching {symbol}...")
            df_raw = fetch_stock_data(symbol)
            if df_raw.empty:
                print(f"No data for {symbol}")
                continue
                
            df_db = prepare_db_data(df_raw, symbol)
            if not df_db.empty:
                db.insert_data(df_db)
                success_count += 1
                print(f"✅ Stored {len(df_db)} records for {symbol}")
            else:
                print(f"No market hours data for {symbol}")
                
        except Exception as e:
            print(f"❌ Error fetching {symbol}: {e}")
    
    print(f"🎉 Completed: {success_count}/{len(STOCKS)} stocks updated")
    return success_count

