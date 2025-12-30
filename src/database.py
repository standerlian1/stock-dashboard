import os
from supabase import create_client, Client
from typing import List, Dict, Any
import pandas as pd
from datetime import datetime
import pytz

class SupabaseStockDB:
    def __init__(self):
        # Streamlit secrets format
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        self.client: Client = create_client(url, key)
    
    def create_table(self):
        """Create table if not exists"""
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
        self.client.rpc('execute_sql', {'query': table_schema})
    
    def insert_data(self, df: pd.DataFrame):
        """Insert DataFrame to Supabase"""
        data = df.to_dict('records')
        self.client.table('stocks_data').insert(data).execute()
    
    def get_latest_data(self, symbol: str, days: int = 90) -> pd.DataFrame:
        """Get last N days data for symbol"""
        response = self.client.table('stocks_data')\
            .select("*")\
            .eq('symbol', symbol)\
            .order('fetch_timestamp', desc=True)\
            .limit(days * 20)  # ~20 candles/day
        return pd.DataFrame(response.data)
    
    def get_last_update(self, symbol: str) -> str:
        """Get exact last update timestamp"""
        response = self.client.table('stocks_data')\
            .select('fetch_timestamp')\
            .eq('symbol', symbol)\
            .order('fetch_timestamp', desc=True)\
            .limit(1)
        if response.data:
            dt = pd.to_datetime(response.data<a href="" class="citation-link" target="_blank" style="vertical-align: super; font-size: 0.8em; margin-left: 3px;">[0]</a>['fetch_timestamp'])
            eastern = pytz.timezone('US/Eastern')
            dt_eastern = dt.astimezone(eastern)
            return dt_eastern.strftime('%Y-%m-%d %H:%M:%S %Z')
        return "No data"
