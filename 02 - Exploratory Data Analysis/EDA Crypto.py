####################
# Import Libraries
####################

import base64
import json
import time

import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st

from bs4 import BeautifulSoup

####################
# Set Layout to Wide
####################

st.set_page_config(layout="wide")

####################
# Set Header
####################

st.title('Crypto Price App')

st.markdown("""
    This app retrieves cryptocurrency prices for the top 100 cryptocurrency from **CoinMarketCap**
""")

####################
# Divide Page into 3 Columns
####################

col1 = st.sidebar
col2, col3 = st.columns((2, 1))

####################
# Sidebar + Main Panel
####################

col1.header('Input Options')

####################
# Sidebar - Currency Price Unit
####################

currency_price_unit = col1.selectbox('Select currency for price', ('USD', 'BTC', 'ETH'))

####################
# Web Scraping of CoinMarketCap
####################

@st.cache
def load_data():
    cmc = requests.get('https://coinmarketcap.com')
    soup = BeautifulSoup(cmc.content, 'html.parser')

    data = soup.find('script', id='__NEXT_DATA__', type='application/json')

    coin_data = json.loads(data.contents[0])
    listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']

    keys = list(listings[0]['keysArr'])

    df_values = []

    for i in listings[1:]:
        df_values.append([
            i[keys.index('name')],
            i[keys.index('symbol')],
            i[keys.index('quote.' + currency_price_unit + '.price')],
            i[keys.index('quote.' + currency_price_unit + '.percentChange1h')],
            i[keys.index('quote.' + currency_price_unit + '.percentChange24h')],
            i[keys.index('quote.' + currency_price_unit + '.percentChange7d')],
            i[keys.index('quote.' + currency_price_unit + '.marketCap')],
            i[keys.index('quote.' + currency_price_unit + '.volume24h')]
        ])

    df = pd.DataFrame(
        data=df_values,
        columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'price', 'volume_24h']
    )
    return df

df = load_data()

####################
# Sidebar - Crypto Selection
####################

sorted_coin = sorted(df['coin_symbol'])
selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)

df_selected_coin = df[ (df['coin_symbol'].isin(selected_coin))]

####################
# Sidebar - Number of Coins to Display
####################

num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
df_coins = df_selected_coin[:num_coin]

####################
# Sidebar - Percent Change Timeframe
####################

percent_timeframe = col1.selectbox('Percent change time frame', ['7d','24h', '1h'])
percent_dict = {"7d":'percent_change_7d', "24h":'percent_change_24h', "1h":'percent_change_1h'}
selected_percent_timeframe = percent_dict[percent_timeframe]

####################
# Sidebar - Sorting values
####################

sort_values = col1.selectbox('Sort values?', ['Yes', 'No'])

####################
# Show header in column 2
####################

col2.subheader('Price Data of Selected Cryptocurrency')
col2.write('Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')

col2.dataframe(df_coins)

####################
# Download file
####################

def file_download(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href

col2.markdown(file_download(df_selected_coin), unsafe_allow_html=True)

####################
# Bar plot of % Price change
####################

col2.subheader('Table of % Price Change')

df_change = pd.concat([df_coins.coin_symbol, df_coins.percent_change_1h, df_coins.percent_change_24h, df_coins.percent_change_7d], axis=1)
df_change = df_change.set_index('coin_symbol')

df_change['positive_percent_change_1h'] = df_change['percent_change_1h'] > 0
df_change['positive_percent_change_24h'] = df_change['percent_change_24h'] > 0
df_change['positive_percent_change_7d'] = df_change['percent_change_7d'] > 0

col2.dataframe(df_change)

col3.subheader('Bar plot of % Price Change')

####################
# Conditional creation of Bar plot (timeframe)
####################

if percent_timeframe == '7d':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_7d'])

    col3.write('*7 days period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percent_change_7d'].plot(kind='barh', color=df_change.positive_percent_change_7d.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
elif percent_timeframe == '24h':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_24h'])

    col3.write('*24 hour period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percent_change_24h'].plot(kind='barh', color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
else:
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_1h'])

    col3.write('*1 hour period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percent_change_1h'].plot(kind='barh', color=df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
