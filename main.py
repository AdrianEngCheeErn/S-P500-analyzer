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

#Predict stock prices
st.header('Stock Prediction')
stock_symbols = df["Symbol"]
input_symbol =  st.selectbox("Select symbol of stock", stock_symbols)