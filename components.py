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
        # Data validation
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in hist_data.columns for col in required_columns):
            missing_cols = [col for col in required_columns if col not in hist_data.columns]
            raise ValueError(f"Missing required columns: {missing_cols}")
            
        # Add technical indicators
        from utils import add_technical_indicators
        df = add_technical_indicators(hist_data)
            
        # Create subplots with space for indicators
        fig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=[0.5, 0.2, 0.15, 0.15]
        )

        # Candlestick chart
        candlestick = go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='OHLC'
        )
        fig.add_trace(candlestick, row=1, col=1)

        # Add Moving Averages
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], name='SMA 20', line=dict(color='blue')), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], name='SMA 50', line=dict(color='orange')), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA_20'], name='EMA 20', line=dict(color='purple')), row=1, col=1)

        # Volume
        volume_bar = go.Bar(x=df.index, y=df['Volume'], name='Volume')
        fig.add_trace(volume_bar, row=2, col=1)

        # RSI
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color='red')), row=3, col=1)
        # Add reference lines for RSI overbought/oversold levels
        fig.add_shape(type="line", x0=df.index[0], x1=df.index[-1], y0=70, y1=70,
                     line=dict(color="red", width=1, dash="dash"), row="3", col="1")
        fig.add_shape(type="line", x0=df.index[0], x1=df.index[-1], y0=30, y1=30,
                     line=dict(color="green", width=1, dash="dash"), row="3", col="1")

        # MACD
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='blue')), row=4, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], name='Signal', line=dict(color='orange')), row=4, col=1)
        fig.add_trace(go.Bar(x=df.index, y=df['MACD_Hist'], name='MACD Histogram'), row=4, col=1)

        # Update layout
        fig.update_layout(
            title=f'{symbol} Stock Price and Technical Indicators',
            yaxis_title='Price',
            yaxis2_title='Volume',
            yaxis3_title='RSI',
            yaxis4_title='MACD',
            xaxis_rangeslider_visible=False,
            height=1000,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        return fig

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
    summary_data = {
        'Current': hist_data['Close'].iloc[-1],
        'Open': hist_data['Open'].iloc[-1],
        'High': hist_data['High'].iloc[-1],
        'Low': hist_data['Low'].iloc[-1],
        'Volume': hist_data['Volume'].iloc[-1],
        'Change %': ((hist_data['Close'].iloc[-1] - hist_data['Open'].iloc[-1]) / 
                    hist_data['Open'].iloc[-1] * 100)
    }
    
    summary = pd.DataFrame.from_dict(summary_data, orient='index', columns=['Value'])
    return summary
