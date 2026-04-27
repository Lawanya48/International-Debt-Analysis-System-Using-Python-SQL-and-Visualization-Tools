import streamlit as st
import pandas as pd
import os

# Import modules (must be inside app/)
import insights
import queries

# Page config
st.set_page_config(layout="wide", page_title="Global Debt Dashboard")

# ---------------- LOAD DATA ----------------
base_path = os.path.dirname(__file__)

# Go to parent folder → data/
file_path = os.path.join(base_path, "..", "data", "final_cleaned_debt_data.csv")

# Safe loading
if not os.path.exists(file_path):
    st.error("❌ Dataset not found. Please check 'data/final_cleaned_debt_data.csv'")
    st.stop()

df = pd.read_csv(file_path)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Insights", "Queries"])

# ================= DASHBOARD =================
if page == "Dashboard":

    st.title("🌍 Global Debt Analysis Dashboard")

    # Country filter
    country = st.selectbox("🌎 Select Country", sorted(df["country"].dropna().unique()))

    data = df[df["country"] == country]

    # KPI
    st.metric("💰 Total Value", f"{data['value'].sum():,.2f}")

    # Line chart
    st.subheader("📈 Year-wise Trend")
    trend = data.groupby("year")["value"].sum()
    st.line_chart(trend)

    # Bar chart
    st.subheader("📊 Indicator Distribution")
    ind = data.groupby("indicator")["value"].sum()
    st.bar_chart(ind)

# ================= INSIGHTS =================
elif page == "Insights":
    insights.show_insights(df)

# ================= QUERIES =================
elif page == "Queries":
    queries.show_queries(df)
