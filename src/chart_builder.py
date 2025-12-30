"""Build Plotly candlestick charts"""
import plotly.graph_objects as go
import pandas as pd
import pytz
from src.config import TIMEZONE, DARK_THEME

def create_candlestick_chart(df: pd.DataFrame, symbol: str) -> go.Figure:
    """Create professional dark candlestick chart"""
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False, font_size=20)
        return fig
    
    # Prepare data
    df_plot = df.copy()
    df_plot['timestamp_ny'] = pd.to_datetime(df_plot['fetch_timestamp']).dt.tz_convert(TIMEZONE)
    
    # Candlestick colors
    colors = ['green' if close > open else 'red' 
              for open, close in zip(df_plot['open'], df_plot['close'])]
    
    fig = go.Figure(data=[
        go.Candlestick(
            x=df_plot['timestamp_ny'],
            open=df_plot['open'],
            high=df_plot['high'],
            low=df_plot['low'],
            close=df_plot['close'],
            increasing_line_color=DARK_THEME['green'],
            decreasing_line_color=DARK_THEME['red'],
            increasing_fillcolor=DARK_THEME['green'],
            decreasing_fillcolor=DARK_THEME['red'],
            line=dict(width=1)
        )
    ])
    
    # Dark theme layout
    fig.update_layout(
        title=f"{symbol} - Live Candlestick Chart",
        title_font_color=DARK_THEME['text'],
        xaxis_title="NY Time (09:30-16:00)",
        yaxis_title="Price ($)",
        xaxis_rangeslider_visible=False,
        plot_bgcolor=DARK_THEME['bg'],
        paper_bgcolor=DARK_THEME['bg'],
        font_color=DARK_THEME['text'],
        height=600,
        showlegend=False,
        xaxis=dict(
            gridcolor='#333',
            showgrid=True,
            type='date',
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1D", step="day", stepmode="backward"),
                    dict(count=5, label="5D", step="day", stepmode="backward"),
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeselector=dict(
                bgcolor="#262730",
                activecolor=DARK_THEME['green'],
                font_color=DARK_THEME['text']
            )
        ),
        yaxis=dict(
            gridcolor='#333',
            showgrid=True
        )
    )
    
    return fig

