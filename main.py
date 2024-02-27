import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
import xgboost as xgb 
import time


#pandas html scaper
df = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', header = 0)[0]


st.title('S&P 500 Analyzer')

st.sidebar.header('Filter by GICS sector')
sorted_sector_unique = sorted( df['GICS Sector'].unique() )
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)
df_selected_sector = df[ (df['GICS Sector'].isin(selected_sector)) ]    

#Display companies based on selected GICS Sector
st.header('Filtered Companies')
st.dataframe(df_selected_sector)

#Display stock price
st.header('Stock Price')
stock_symbols = df["Symbol"]
input_symbol =  st.selectbox("Select symbol of stock", ["-"] + list(stock_symbols))
input_period =  st.selectbox("Select period", ["1D", "5D", "1M", "6M", "YTD", "1Y", "5Y", "Max"])
if input_symbol != "-":
    price_history = yf.Ticker(input_symbol)
    price_history = price_history.history(period=input_period)
    st.dataframe(price_history)
    fig, ax = plt.subplots()
    plot = st.pyplot(fig)

    # Loop to fetch and update stock values
    while True:
        historical_prices = price_history
        latest_price = historical_prices['Close'].iloc[-1]
        latest_time = historical_prices.index[-1].strftime('%H:%M:%S')
        ax.clear()
        ax.plot(historical_prices.index, historical_prices['Close'], label='Stock Value')
        ax.set_xlabel('Time')
        ax.set_ylabel('Stock Value')
        ax.set_title('Apple Stock Value')
        ax.legend(loc='upper left')
        ax.tick_params(axis='x', rotation=45)
        plot.pyplot(fig)
        st.write(f"Latest Price ({latest_time}): {latest_price}")
        time.sleep(60)


#Stock price prediction TODO
    train_data = price_history