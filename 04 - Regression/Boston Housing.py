####################
# Import Libraries
####################

import shap
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn.ensemble import RandomForestRegressor

####################
# Show Header
####################

st.write("""
# Boston House Price Prediction App

This app predicts the **Boston House Price**!
""")

####################
# Load Boston House Price Dataset
####################

boston = datasets.load_boston()

X = pd.DataFrame(boston.data, columns=boston.feature_names)
Y = pd.DataFrame(boston.target, columns=["MEDV"])

####################
# Create Sidebar
####################

st.sidebar.header('Specify Input Parameters')

def user_input_features():
    data = {}

    for col in X.columns:
        data[col] = st.sidebar.slider(col, float(X[col].min()), float(X[col].max()), float(X[col].mean()))

    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()

####################
# Show Input Features
####################

st.header('Specified Input parameters')
st.write(df)

####################
# Train Random Forest Regressor
####################

model = RandomForestRegressor()
model.fit(X, Y)

####################
# Predict and Show Prediction
####################

prediction = model.predict(df)

st.header('Prediction of MEDV')
st.write(prediction)

####################
# Showing an explanation for Forest Tree
####################

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

st.header('Feature Importance')

plt.figure(figsize=(5,25))
plt.title('Feature importance based on SHAP values')
shap.summary_plot(shap_values, X)
st.pyplot(plt, bbox_inches='tight')


plt.figure(figsize=(5,25))
plt.title('Feature importance based on SHAP values (Bar)')
shap.summary_plot(shap_values, X, plot_type="bar")
st.pyplot(plt, bbox_inches='tight')
