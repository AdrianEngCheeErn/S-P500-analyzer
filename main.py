import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import plotly.express as px
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
st.text(" ")
st.text(" ")
st.text(" ")

st.header('Stock Details')
stock_symbols = df["Symbol"]
input_symbol =  st.selectbox("Select symbol of stock", ["-"] + list(stock_symbols))

st.sidebar.header('Select Time Frame')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')


if input_symbol != "-":
    data = yf.download(input_symbol, start=start_date, end=end_date)
    fig = px.line(data, x = data.index, y = data['Adj Close'], title=input_symbol)
    st.plotly_chart(fig)
    
    st.header("Price Movement")
    data2 = data
    data2['Change'] = (data['Adj Close'] / data['Adj Close'].shift(periods = 1)) - 1
    data2.dropna(inplace = True)
    try:
        annual_change = (data.iloc[-1]['Adj Close'] - data.iloc[0]['Adj Close']) / data.iloc[0]['Adj Close'] * 100
        annual_change = round(annual_change, 2)
        st.write("Annual Change : " + str(annual_change) + "%")
    except:
        pass
    st.write(data2)
    st.text(" ")
    st.text(" ")
    st.text(" ")

    TODAY = date.today().strftime("%Y-%m-%d")
    START = "2015-01-01"

    @st.cache_data
    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        return data
 
    data = load_data(input_symbol)
    st.text(" ")
    st.text(" ")
    st.text(" ")

    st.subheader('Stock price prediction')
    # Predict forecast with Prophet.
    n_years = st.slider('Years of prediction:', 1, 4)
    period = n_years * 365
    df_train = data[['Date','Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
    st.text(" ")
    st.text(" ")
    st.text(" ")

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    # Show and plot forecast
    st.subheader('Forecast data')
    st.write(forecast.tail())
    
    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.header(f'Forecast plot for {n_years} years')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)

    st.write("Forecast components")
    fig2 = m.plot_components(forecast)
    st.write(fig2)