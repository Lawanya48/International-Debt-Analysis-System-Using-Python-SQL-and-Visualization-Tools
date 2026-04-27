import streamlit as st
import pandas as pd
import plotly.express as px

def show_insights(df):

    st.title("📊 Insights Dashboard")

    df = df.copy()

    # ---------------- DATA CLEAN ----------------
    df["value"] = df.groupby(["country", "indicator"])["value"].ffill()
    df["value"] = df.groupby(["country", "indicator"])["value"].bfill()
    df = df.dropna(subset=["value"])

    # ---------------- FILTER ----------------
    st.sidebar.header("🔍 Insights Filters")

    country = st.sidebar.selectbox(
        "Country",
        sorted(df["country"].dropna().unique())
    )

    data = df[df["country"] == country]

    if data.empty:
        st.warning("No data available")
        return

    st.subheader(f"{country} Analysis")

    # ---------------- KPI ----------------
    st.metric("💰 Total Value", f"{data['value'].sum():,.2f}")

    # ---------------- LINE CHART ----------------
    st.subheader("📈 Year-wise Trend")
    trend = data.groupby("year")["value"].sum().reset_index()
    st.plotly_chart(px.line(trend, x="year", y="value"), use_container_width=True)

    # ---------------- BAR CHART ----------------
    st.subheader("📊 Indicator Distribution")
    ind = data.groupby("indicator")["value"].sum().reset_index()
    st.plotly_chart(px.bar(ind, x="indicator", y="value"), use_container_width=True)

    # ---------------- PIE CHART ----------------
    st.subheader("🥧 Indicator Share")
    st.plotly_chart(px.pie(ind, names="indicator", values="value"), use_container_width=True)

    # ---------------- HISTOGRAM ----------------
    st.subheader("📉 Value Distribution")
    st.plotly_chart(px.histogram(data, x="value"), use_container_width=True)

    # ---------------- BOX PLOT ----------------
    st.subheader("📦 Value Spread")
    st.plotly_chart(px.box(data, y="value"), use_container_width=True)

    # ---------------- SCATTER ----------------
    st.subheader("🔵 Scatter Plot")
    data["size_value"] = data["value"].abs()
    st.plotly_chart(
        px.scatter(data, x="year", y="value", size="size_value"),
        use_container_width=True
    )

    # ---------------- HEATMAP ----------------
    st.subheader("🔥 Heatmap")
    pivot = data.pivot_table(values="value", index="year",
                             columns="indicator", aggfunc="sum")

    if not pivot.empty:
        st.plotly_chart(px.imshow(pivot, aspect="auto"), use_container_width=True)
    else:
        st.warning("No data available for heatmap")
