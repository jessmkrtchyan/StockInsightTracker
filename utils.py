import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

@st.cache_data(ttl=300)  # Cache data for 5 minutes
def get_stock_data(symbol: str, period: str = "1y"):
    """
    Fetch stock data from Yahoo Finance
    """
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)
        info = stock.info
        return hist, info
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {str(e)}")
        return None, None

@st.cache_data(ttl=300)
def get_company_info(symbol: str):
    """
    Get company information and key statistics
    """
    try:
        stock = yf.Ticker(symbol)
        info = {
            'Company Name': stock.info.get('longName', 'N/A'),
            'Sector': stock.info.get('sector', 'N/A'),
            'Market Cap': format_market_cap(stock.info.get('marketCap', 0)),
            'P/E Ratio': round(stock.info.get('trailingPE', 0), 2),
            '52 Week High': stock.info.get('fiftyTwoWeekHigh', 0),
            '52 Week Low': stock.info.get('fiftyTwoWeekLow', 0),
            'Volume': stock.info.get('volume', 0),
        }
        return info
    except:
        return None

def format_market_cap(market_cap: int) -> str:
    """
    Format market cap in billions/millions
    """
    if market_cap >= 1e9:
        return f"${market_cap/1e9:.2f}B"
    elif market_cap >= 1e6:
        return f"${market_cap/1e6:.2f}M"
    else:
        return f"${market_cap:,.0f}"

def prepare_download_data(hist_data: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare historical data for CSV download
    """
    df = hist_data.copy()
    df.index = df.index.strftime('%Y-%m-%d')
    df = df.round(2)
    return df
