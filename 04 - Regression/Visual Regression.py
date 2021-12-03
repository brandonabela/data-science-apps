####################
# Import Libraries
####################

import shap

import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import matplotlib.pyplot as plt

from math import sqrt
from dataclasses import dataclass
from sklearn.metrics import mean_squared_error

####################
# Default Values
####################

X_MIN = 0
X_MAX = 1

####################
# Weight Data Structure
####################

@dataclass
class Weight:
    w0: float
    w1: float
    w2: float

####################
# Create Dataset
####################

@st.cache
def build_dataset(x_resolution):
    X_source = np.linspace(X_MIN, X_MAX, x_resolution)
    y_source = (
        np.polynomial.polynomial.polyval(X_source, [0, 2, 5])
        + np.sin(8 * X_source)
        + 0.5 * np.random.normal(size=x_resolution)
    )

    return pd.DataFrame({"x_source": X_source, "y_source": y_source})

####################
# Create Regression
####################

def build_regression(source_df, w: Weight):
    X_reg = source_df["x_source"].copy()
    y_reg = np.polynomial.polynomial.polyval(X_reg, [0, w.w0, w.w1]) + np.sin(
        w.w2 * X_reg
    )
    return pd.DataFrame({"x_reg": X_reg, "y_reg": y_reg})

####################
# Create Metrics
####################

def build_error(source_df, res_df):
    y_error = np.abs(source_df["y_source"] - res_df["y_reg"])
    return pd.DataFrame({"x": source_df["x_source"], "y_err": y_error})


def compute_rmse(source_df, res_df):
    rmse = sqrt(mean_squared_error(source_df["y_source"], res_df["y_reg"]))
    return rmse

####################
# Show Header
####################

st.title("Regression")

st.markdown("Play with weights in sidebar and see if you can fit the points.")
st.markdown("$$f(x)=w_0 \\times x+w_1 \\times x^2 + sin(w_2 \\times x)$$")

####################
# Create Sidebar
####################

st.sidebar.subheader("Parameters")
xres = st.sidebar.slider("Number of points", 100, 1000, 100, 100)

w0 = st.sidebar.slider("w0", 0.0, 10.0, 1.0, 0.5)
w1 = st.sidebar.slider("w1", 0.0, 10.0, 1.0, 0.5)
w2 = st.sidebar.slider("w2", 0.0, 10.0, 1.0, 0.5)
w = Weight(w0, w1, w2)

####################
# Create Sidebar
####################

source_data = build_dataset(xres)
regression_data = build_regression(source_data, w)
error_data = build_error(source_data, regression_data)
rmse = compute_rmse(source_data, regression_data)

####################
# Show Graphs
####################

plt.figure(figsize=(5,4))
plt.plot(regression_data.x_reg, regression_data.y_reg, color='blue', linewidth=2.0)
plt.plot(source_data.x_source, source_data.y_source, 'o', color='black', markersize=2)
st.pyplot(plt, bbox_inches='tight')

plt.figure(figsize=(5,2))
plt.ylabel("abs error |data - reg|")
plt.fill_between(error_data.x, 0, error_data.y_err)
st.pyplot(plt, bbox_inches='tight')

rmse_text = st.text(f"Current RMSE : {rmse}")
