####################
# Import Libraries
####################

import yfinance as yf
import streamlit as st
import pandas as pd

####################
# Page Logic
####################

st.write("""
# Simple Stock Price App

Shown are the stock ***closing price*** and ***volume*** of Google!
""")

tickerData = yf.Ticker('GOOGL')

tickerDf = tickerData.history(period='1d', start='2010-5-31')

st.write("""
## Closing Price
""")
st.line_chart(tickerDf['Close'])

st.write("""
## Volume
""")
st.line_chart(tickerDf['Volume'])
