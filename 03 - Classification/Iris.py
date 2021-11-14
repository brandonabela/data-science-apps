####################
# Import Libraries
####################

import streamlit as st
import pandas as pd

from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

####################
# Show Header
####################

st.write("""
# Simple Iris Flower Prediction App
""")

####################
# Show Sidebar
####################

st.sidebar.header('User Input Parameters')

####################
# Defining user input features
####################

def user_input_features():
    sepal_length = st.sidebar.slider('Sepal Length', 4.3, 7.9, 5.4)
    sepal_width = st.sidebar.slider('Sepal Width', 2.0, 4.4, 3.4)
    petal_length = st.sidebar.slider('Petal Length', 1.0, 6.9, 1.3)
    petal_width = st.sidebar.slider('Petal Length', 0.1, 2.5, 0.2)

    data = {
        'sepal_length': sepal_length,
        'sepal_width': sepal_width,
        'petal_length': petal_length,
        'petal_width': petal_width
    }

    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()

####################
# Show User Inputs
####################

st.subheader('User Input Parameters')
st.write(df)

####################
# Training Iris using Random Forest
####################

iris = datasets.load_iris()
X = iris.data
Y = iris.target

clf = RandomForestClassifier()
clf.fit(X, Y)

####################
# Predict Iris using Inputs
####################

prediction = clf.predict(df)
prediction_prob = clf.predict_proba(df)

####################
# Show Class Labels
####################

st.subheader('Class labels and their corresponding index number')
st.write(iris.target_names)

####################
# Show Prediction
####################

st.subheader('Prediction')
st.write(iris.target_names[prediction])

####################
# Show Prediction Probability
####################

st.subheader('Prediction Probability')
st.write(prediction_prob)
