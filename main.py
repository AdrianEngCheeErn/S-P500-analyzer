import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

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
price_history = yf.Ticker(input_symbol)
if input_symbol != "-":
    price_history = price_history.history(period=input_period)
    st.dataframe(price_history)


    #Stock price prediction TODO
    price_history["Tomorrow"] = price_history["Close"].shift(-1)
    price_history = price_history.loc["1990-01-01":].copy()
    st.dataframe(price_history)
