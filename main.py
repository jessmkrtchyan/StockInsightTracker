import streamlit as st
import pandas as pd
import os
from utils import get_stock_data, get_company_info, prepare_download_data
from components import create_price_chart, display_metrics, create_summary_table

# Page configuration
st.set_page_config(
    page_title="Stock Data Dashboard",
    page_icon="📈",
    layout="wide"
)

# Load custom CSS
try:
    css_path = os.path.join(os.path.dirname(__file__), 'style.css')
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except Exception as e:
    st.warning(f"Could not load CSS file: {str(e)}")

# Sidebar
st.sidebar.title("Stock Dashboard")
symbol = st.sidebar.text_input("Enter Stock Symbol", value="AAPL").upper()
period = st.sidebar.selectbox(
    "Select Time Period",
    options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
    index=3
)

st.sidebar.markdown("""
<div class="sidebar-text">
Enter a valid stock symbol (e.g., AAPL for Apple Inc.) and select the time period 
for historical data visualization.
</div>
""", unsafe_allow_html=True)

# Main content
st.title("Stock Data Visualization Dashboard")

if symbol:
    with st.spinner(f'Fetching data for {symbol}...'):
        try:
            # Fetch data
            hist_data, raw_info = get_stock_data(symbol, period)
            if hist_data is None or raw_info is None:
                st.error(f"Could not fetch data for {symbol}. Please verify the symbol and try again.")
                st.stop()

            company_info = get_company_info(symbol)
            if company_info is None:
                st.error(f"Could not fetch company information for {symbol}.")
                st.stop()

            # Company information and key metrics
            st.header("Company Overview")
            display_metrics(company_info)

            # Price chart
            st.header("Price Chart")
            try:
                fig = create_price_chart(hist_data, symbol)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating price chart: {str(e)}")

            # Summary statistics
            st.header("Daily Summary")
            try:
                summary = create_summary_table(hist_data)
                st.dataframe(summary, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating summary table: {str(e)}")

            # Historical data table with download option
            st.header("Historical Data")
            try:
                download_data = prepare_download_data(hist_data)
                
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.dataframe(download_data, use_container_width=True)
                with col2:
                    csv = download_data.to_csv()
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"{symbol}_historical_data.csv",
                        mime="text/csv"
                    )
            except Exception as e:
                st.error(f"Error preparing download data: {str(e)}")

        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
else:
    st.info("Please enter a stock symbol to begin.")
