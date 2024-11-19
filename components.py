import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def create_price_chart(hist_data: pd.DataFrame, symbol: str):
    """
    Create an interactive price chart using Plotly
    """
    try:
        # Debug logging
        st.write("Debug: Historical data shape:", hist_data.shape)
        st.write("Debug: Columns present:", hist_data.columns.tolist())
        
        # Data validation
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in hist_data.columns for col in required_columns):
            missing_cols = [col for col in required_columns if col not in hist_data.columns]
            raise ValueError(f"Missing required columns: {missing_cols}")
            
        # Verify data types and handle any non-numeric values
        for col in required_columns:
            if not np.issubdtype(hist_data[col].dtype, np.number):
                st.write(f"Debug: Converting {col} to numeric, current dtype:", hist_data[col].dtype)
                hist_data[col] = pd.to_numeric(hist_data[col], errors='coerce')
            
        # Check for null values
        null_counts = hist_data[required_columns].isnull().sum()
        if null_counts.any():
            st.write("Debug: Null values found:", null_counts[null_counts > 0])
            hist_data = hist_data.dropna(subset=required_columns)
            
        if len(hist_data) == 0:
            raise ValueError("No valid data points after cleaning")

        # Create subplots with corrected parameter name
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=[0.7, 0.3]
        )

        try:
            # Candlestick chart
            candlestick = go.Candlestick(
                x=hist_data.index,
                open=hist_data['Open'],
                high=hist_data['High'],
                low=hist_data['Low'],
                close=hist_data['Close'],
                name='OHLC'
            )
            fig.add_trace(candlestick, row=1, col=1)

            # Volume bar chart
            volume_bar = go.Bar(
                x=hist_data.index,
                y=hist_data['Volume'],
                name='Volume'
            )
            fig.add_trace(volume_bar, row=2, col=1)

            # Update layout
            fig.update_layout(
                title=f'{symbol} Stock Price',
                yaxis_title='Price',
                yaxis2_title='Volume',
                xaxis_rangeslider_visible=False,
                height=800
            )

            return fig

        except Exception as e:
            st.error(f"Error creating Plotly figure: {str(e)}")
            raise

    except Exception as e:
        st.error(f"Error in create_price_chart: {str(e)}")
        raise

def display_metrics(info: dict):
    """
    Display key financial metrics in columns
    """
    cols = st.columns(4)
    metrics = list(info.items())
    
    for i, col in enumerate(cols):
        for j in range(2):
            idx = i * 2 + j
            if idx < len(metrics):
                key, value = metrics[idx]
                col.metric(key, value)

def create_summary_table(hist_data: pd.DataFrame):
    """
    Create a summary statistics table
    """
    summary = pd.DataFrame({
        'Current': hist_data['Close'].iloc[-1],
        'Open': hist_data['Open'].iloc[-1],
        'High': hist_data['High'].iloc[-1],
        'Low': hist_data['Low'].iloc[-1],
        'Volume': hist_data['Volume'].iloc[-1],
        'Change %': ((hist_data['Close'].iloc[-1] - hist_data['Open'].iloc[-1]) / 
                    hist_data['Open'].iloc[-1] * 100)
    }, index=[hist_data.index[-1].strftime('%Y-%m-%d')])
    
    return summary.T
