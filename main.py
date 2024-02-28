import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
from datetime import date, timedelta
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
st.header('Stock Details')
stock_symbols = df["Symbol"]
input_symbol =  st.selectbox("Select symbol of stock", ["-"] + list(stock_symbols))
input_period =  st.selectbox("Select period", ["1D", "5D", "1M", "6M", "YTD", "1Y", "5Y", "Max"])
price_history = yf.Ticker(input_symbol)

if input_symbol != "-":
    price_history = price_history.history(period=input_period)
    st.dataframe(price_history)
    
    TODAY = date.today().strftime("%Y-%m-%d")
    START = "2015-01-01"

    @st.cache_data
    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        return data

        
    data = load_data(input_symbol)


    st.subheader('Stock price prediction')
    # Predict forecast with Prophet.
    n_years = st.slider('Years of prediction:', 1, 4)
    period = n_years * 365
    df_train = data[['Date','Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    # Show and plot forecast
    st.subheader('Forecast data')
    st.write(forecast.tail())
        
    st.write(f'Forecast plot for {n_years} years')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)

    st.write("Forecast components")
    fig2 = m.plot_components(forecast)
    st.write(fig2)