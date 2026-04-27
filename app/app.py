import streamlit as st
import pandas as pd
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.insights import show_insights
from src.queries import show_queries

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