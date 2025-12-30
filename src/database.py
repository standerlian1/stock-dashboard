import os
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
from supabase import create_client, Client
import pytz

class SupabaseStockDB:
    def __init__(self):
        """Initialize Supabase client from Streamlit secrets"""
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in secrets.toml")
        
        self.client: Client = create_client(url, key)
    
    def create_table(self):
        """Create stocks_data table with indexes"""
        table_schema = """
        CREATE TABLE IF NOT EXISTS stocks_data (
            id BIGSERIAL PRIMARY KEY,
            symbol VARCHAR(10) NOT NULL,
            date DATE NOT NULL,
            time TIME NOT NULL,
            fetch_timestamp TIMESTAMPTZ NOT NULL,
            open DECIMAL(12,4) NOT NULL,
            high DECIMAL(12,4) NOT NULL,
            low DECIMAL(12,4) NOT NULL,
            close DECIMAL(12,4) NOT NULL,
            volume BIGINT,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        
        CREATE INDEX IF NOT EXISTS idx_symbol_date ON stocks_data(symbol, date);
        CREATE INDEX IF NOT EXISTS idx_symbol_fetch ON stocks_data(symbol, fetch_timestamp DESC);
        """
        
        # Use PostgreSQL extension for raw SQL
        self.client.rpc('execute_sql', {'query': table_schema}).execute()
    
    def insert_data(self, df: pd.DataFrame):
        """Insert pandas DataFrame to Supabase"""
        if df.empty:
            return
        
        # Ensure required columns exist
        required_cols = ['symbol', 'date', 'time', 'fetch_timestamp', 'open', 'high', 'low', 'close']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        data = df[required_cols + ['volume']].to_dict('records')
        response = self.client.table('stocks_data').insert(data).execute()
        return response
    
    def get_latest_data(self, symbol: str, days: int = 90) -> pd.DataFrame:
        """Get last N days of data for symbol"""
        three_months_ago = pd.Timestamp.now() - pd.Timedelta(days=days)
        
        response = self.client.table('stocks_data')\
            .select("*")\
            .eq('symbol', symbol)\
            .gte('fetch_timestamp', three_months_ago.isoformat())\
            .order('fetch_timestamp', desc=True)\
            .limit(days * 30)  # ~30 candles/day max
        
        data = response.data
        if not data:
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        df['fetch_timestamp'] = pd.to_datetime(df['fetch_timestamp'])
        return df
    
    def get_last_update(self, symbol: str) -> str:
        """Get exact last update timestamp in NY time"""
        response = self.client.table('stocks_data')\
            .select('fetch_timestamp')\
            .eq('symbol', symbol)\
            .order('fetch_timestamp', desc=True)\
            .limit(1)\
            .execute()
        
        if response.data:
            dt = pd.to_datetime(response.data<a href="" class="citation-link" target="_blank" style="vertical-align: super; font-size: 0.8em; margin-left: 3px;">[0]</a>['fetch_timestamp'])
            eastern = pytz.timezone('US/Eastern')
            dt_eastern = dt.tz_convert(eastern)
            return dt_eastern.strftime('%Y-%m-%d %H:%M:%S %Z')
        return "No data available"
    
    def delete_old_data(self, days: int = 95):
        """Clean up data older than specified days"""
        cutoff_date = (pd.Timestamp.now() - pd.Timedelta(days=days)).isoformat()
        self.client.table('stocks_data')\
            .delete()\
            .lt('fetch_timestamp', cutoff_date)\
            .execute()
