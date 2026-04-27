import streamlit as st
import pandas as pd
import os
import insights
import queries

st.set_page_config(layout="wide")

base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "final_dataset.csv")

df = pd.read_csv(file_path)

page = st.sidebar.radio("Navigation", ["Dashboard", "Insights", "Queries"])

# Dashboard
if page == "Dashboard":

    st.title("🌍 Global Dashboard")

    country = st.selectbox("Country", df["country"].unique())
    data = df[df["country"] == country]

    st.metric("Total Value", f"{data['value'].sum():,.2f}")

    st.line_chart(data.groupby("year")["value"].sum())
    st.bar_chart(data.groupby("indicator")["value"].sum())

# Insights
elif page == "Insights":
    insights.show_insights()

# Queries
elif page == "Queries":
    queries.show_queries()
