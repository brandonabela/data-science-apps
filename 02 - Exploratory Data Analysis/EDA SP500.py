####################
# Import Libraries
####################

import base64

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import yfinance as yf

####################
# Show header
####################

st.title('S&P 500 App')

st.markdown("""
This app retrieves the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year to date)
""")

####################
# Show sidebar
####################

st.sidebar.header('User Input Features')

####################
# Web Scraping of S&P 500
####################

@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

    html = pd.read_html(url, header=0)
    df = html[0]
    return df

df = load_data()
sector = df.groupby('GICS Sector')

####################
# Sidebar - Sector selection
####################

sorted_sector_unique = sorted(df['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

####################
# Filtering data
####################

df_selected_sector = df[df['GICS Sector'].isin(selected_sector)]

####################
# Show Dataframe
####################

st.header('Display Companies in Selected Sector')
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df_selected_sector)

####################
# Download file
####################

def file_download(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

st.markdown(file_download(df_selected_sector), unsafe_allow_html=True)

####################
# Yahoo finance data
####################

data = yf.download(
    tickers = list(df_selected_sector[:10].Symbol),
    period = "ytd",
    interval = "1d",
    group_by = 'ticker',
    auto_adjust = True,
    prepost = True,
    threads = True,
    proxy = None
)

####################
# Price Plot
####################

def price_plot(symbol):
    df = pd.DataFrame(data[symbol].Close)
    df['Date'] = df.index

    plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
    plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Closing Price', fontweight='bold')

    return st.pyplot(plt)

num_company = st.sidebar.slider('Number of Companies', 1, 5)

####################
# Show Price Plot
####################

if st.button('Show Plots'):
    st.header('Stock Closing Price')

    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)
