import numpy as np
import pandas as pd
import streamlit as st
pd.set_option('display.max_columns', None)
# Load data and historical scores
scores = pd.read_excel("Fantasy.xlsx", sheet_name="ScoringData")
records = pd.read_excel("Fantasy.xlsx", sheet_name="Records")
schedule = pd.read_excel("Fantasy.xlsx", sheet_name="Schedule")
playoffs = pd.read_excel("Fantast.xlsx", sheet_name="Playoffs")
st.title("hello")
