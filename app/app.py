import streamlit as st
import pandas as pd
import sys

import os
import pandas as pd

base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "final_dataset.csv")

#df = pd.read_csv(file_path)

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import insights
import queries

st.set_page_config(layout="wide")

df = pd.read_csv("data/final_cleaned_debt_data.csv")

page = st.sidebar.radio("Navigation", ["Dashboard", "Insights", "Queries"])

if page == "Dashboard":

    st.title("🌍 Global Dashboard")

    country = st.selectbox("Country", df["country"].unique())
    data = df[df["country"] == country]

    st.metric("Total Value", f"{data['value'].sum():,.2f}")

    st.line_chart(data.groupby("year")["value"].sum())
    st.bar_chart(data.groupby("indicator")["value"].sum())

elif page == "Insights":
    show_insights(df)

elif page == "Queries":
    show_queries(df)
