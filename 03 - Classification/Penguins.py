####################
# Import Libraries
####################

import os
import pickle

import numpy as np
import pandas as pd
import streamlit as st

from sklearn.ensemble import RandomForestClassifier

####################
# Show Header
####################

st.write("""
# Penguin Prediction App

This app predicts the **Palmer Penguin** species
""")

####################
# Show Sidebar
####################

st.sidebar.header('User Input Features')

####################
# Collect user input features into dataframe
####################

uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])

if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
else:
    def user_input_features():
        island = st.sidebar.selectbox('Island', ('Biscoe', 'Dream', 'Torgersen'))
        sex = st.sidebar.selectbox('Sex', ('male', 'female'))
        bill_length_mm = st.sidebar.slider('Bill length (mm)', 32.1, 59.6, 43.9)
        bill_depth_mm = st.sidebar.slider('Bill depth (mm)', 13.1, 21.5, 17.2)
        flipper_length_mm = st.sidebar.slider('Flipper length (mm)', 172.0, 231.0, 201.0)
        body_mass_g = st.sidebar.slider('Body mass (g)', 2700.0, 6300.0, 4207.0)

        data = {
            'island': island,
            'bill_length_mm': bill_length_mm,
            'bill_depth_mm': bill_depth_mm,
            'flipper_length_mm': flipper_length_mm,
            'body_mass_g': body_mass_g,
            'sex': sex
        }

        features = pd.DataFrame(data, index=[0])
        return features

    input_df = user_input_features()

####################
# Read Penguin File
####################

penguins_raw  = pd.read_csv('_data/penguins.csv')
penguins = penguins_raw.drop(columns=['species'])
df = pd.concat([input_df, penguins], axis=0)

# Replace species with an index
target_mapper = {'Adelie': 0, 'Chinstrap': 1, 'Gentoo': 2}
penguins_raw['species'] = penguins_raw['species'].apply(lambda x: target_mapper[x])

####################
# Encoding Ordinal Features
####################

encode = ['sex', 'island']
target = 'species'

for col in encode:
    dummy = pd.get_dummies(df[col], prefix=col)
    df = pd.concat([df, dummy], axis=1)
    del df[col]

# Update input data and training data
input_df = df.iloc[:1]
df = df.iloc[1:]

####################
# Reads Saved Classification Model
####################

model = None
model_path = '_model/penguins.pkl'

if not os.path.isfile(model_path):
    # Train random forest classifier
    model = RandomForestClassifier()
    model.fit(df, penguins_raw['species'])

    # Store trained model
    pickle.dump(model, open(model_path, 'wb'))

# Loading trained model
model = pickle.load(open(model_path, 'rb'))

####################
# Display User Input Features
####################

st.subheader('User Input features')
st.write(input_df)

####################
# Show Prediction
####################

prediction = model.predict(input_df)

st.subheader('Prediction')

penguins_species = np.array(['Adelie', 'Chinstrap', 'Gentoo'])
st.write(penguins_species[prediction])

####################
# Show Prediction Probability
####################

prediction_proba = pd.DataFrame(model.predict_proba(input_df), columns=penguins_species)

st.subheader('Prediction Probability')
st.write(prediction_proba)
