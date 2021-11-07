####################
# Import Libraries
####################

import streamlit as st
import pandas as pd
import base64

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

####################
# Show header
####################

st.title('NFL Football Stats Explorer')

st.markdown("""
This app performs simple webscraping of NFL football player stats data
""")

####################
# Showing Sidebar
####################

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1990,2020))))

####################
# Web scraping NFL Player Stats
####################

@st.cache
def load_data(year):
    url = "https://www.pro-football-reference.com/years/" + str(year) + "/rushing.htm"

    html = pd.read_html(url, header=1)
    df = html[0]

    raw = df.drop(df[df['Age'] == 'Age'].index)
    raw = raw.fillna(0)

    player_stats = raw.drop(['Rk'], axis=1)
    return player_stats

player_stats = load_data(selected_year)
player_stats = player_stats[player_stats.columns[:9]]

####################
# Sidebar - Team Selection
####################

sorted_unique_teams = sorted(player_stats['Tm'].unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_teams, sorted_unique_teams)

####################
# Sidebar - Position Selection
####################

unique_pos = ['RB', 'QB', 'WR', 'FB', 'TE']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

####################
# Filtering Data
####################

df_selected_team = player_stats[(player_stats['Tm'].isin(selected_team)) & (player_stats['Pos'].isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimensions: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]))
st.dataframe(df_selected_team)

####################
# Download NBA Player stats data
####################

def file_download(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()

    href = f'<a href="data:file/csv;base64,{b64}" download="player_stats.csv"> Download CSV File </a>'
    return href

st.markdown(file_download(df_selected_team), unsafe_allow_html=True)

####################
# Heatmap
####################

if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv', index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True

    f, ax = plt.subplots(figsize=(7, 5))

    with sns.axes_style("white"):
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)

    st.pyplot(f)
