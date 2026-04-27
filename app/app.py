import streamlit as st
import pandas as pd
import os

# Import modules (make sure these files are inside app/)
import insights
import queries

st.set_page_config(layout="wide")

# ---------------- LOAD DATA ----------------
base_path = os.path.dirname(__file__)

# Go to parent → data folder
file_path = os.path.join(base_path, "..", "data", "final_cleaned_debt_data.csv")

# Safe loading
if not os.path.exists(file_path):
    st.error("❌ Dataset not found. Please check 'data/final_cleaned_debt_data.csv'")
    st.stop()

df = pd.read_csv(file_path)

# ---------------- SIDEBAR ----------------
page = st.sidebar.radio("📌 Navigation", ["Dashboard", "Insights", "Queries"])

# ================= DASHBOARD =================
if page == "Dashboard":

    st.title("🌍 Global Debt Analysis Dashboard")

    # Country filter
    country = st.selectbox("🌎 Select Country", sorted(df["country"].dropna().unique()))

    data = df[df["country"] == country]

    # KPI
    st.metric("💰 Total Value", f"{data['value'].sum():,.2f}")

    # Line chart (year trend)
    st.subheader("📈 Year-wise Trend")
    st.line_chart(data.groupby("year")["value"].sum())

    # Bar chart (indicator)
    st.subheader("📊 Indicator Distribution")
    st.bar_chart(data.groupby("indicator")["value"].sum())

# ================= INSIGHTS =================
elif page == "Insights":
    insights.show_insights(df)
        
# ================= QUERIES =================
elif page == "Queries":
    queries.show_queries(df)
