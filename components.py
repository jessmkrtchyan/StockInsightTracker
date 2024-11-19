import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def create_price_chart(hist_data: pd.DataFrame, symbol: str):
    """
    Create an interactive price chart using Plotly
    """
    fig = make_subplots(rows=2, cols=1, shared_xaxis=True, 
                        vertical_spacing=0.03,
                        row_heights=[0.7, 0.3])

    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=hist_data.index,
            open=hist_data['Open'],
            high=hist_data['High'],
            low=hist_data['Low'],
            close=hist_data['Close'],
            name='OHLC'
        ),
        row=1, col=1
    )

    # Volume bar chart
    fig.add_trace(
        go.Bar(
            x=hist_data.index,
            y=hist_data['Volume'],
            name='Volume'
        ),
        row=2, col=1
    )

    fig.update_layout(
        title=f'{symbol} Stock Price',
        yaxis_title='Price',
        yaxis2_title='Volume',
        xaxis_rangeslider_visible=False,
        height=800
    )

    return fig

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
