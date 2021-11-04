####################
# Import Libraries
####################

import streamlit as st
import pandas as pd
import base64

####################
# Header
####################

st.title('NBA Player Stats Explorer')

st.markdown("""
This app performs simple webscraping of NBA player stats data!
""")

####################
# Sidebar - Year
####################

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(2000, 2020))))

####################
# Web Scraping
####################

@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"

    html = pd.read_html(url, header=0)
    df = html[0]

    raw = df.drop(df[df['Age'] == 'Age'].index)
    raw = raw.fillna(0)

    player_stats = raw.drop(['Rk'], axis=1)
    return player_stats.astype(str)

player_stats = load_data(selected_year)
player_stats = player_stats[player_stats.columns[:9]]

####################
# Sidebar - Team
####################

sorted_unique_teams = sorted(player_stats['Tm'].unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_teams, sorted_unique_teams[:10])

####################
# Sidebar - Position
####################

unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

####################
# Filtering Data
####################

df_selected_team = player_stats[(player_stats['Tm'].isin(selected_team)) & (player_stats['Pos'].isin(selected_pos))]

st.header('Show Player Stats of Selected Teams')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

# ####################
# # Download NBA Player Data
# ####################

def file_download(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()

    return f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'

st.markdown(file_download(df_selected_team), unsafe_allow_html=True)
