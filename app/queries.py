import streamlit as st
import pandas as pd
import plotly.express as px

def show_queries(df):

    st.title("📊 Queries Dashboard (Visual Analytics)")

    df = df.copy()

    # ---------------- FILTER ----------------
    st.sidebar.header("🔍 Query Filters")

    country = st.sidebar.selectbox(
        "Country",
        ["All"] + sorted(df["country"].dropna().unique())
    )

    if country != "All":
        df = df[df["country"] == country]

    total_value = df["value"].sum()

    # ================= BASIC =================
    st.header("🔹 Basic Analysis")

    col1, col2, col3 = st.columns(3)
    col1.metric("🌎 Countries", df["country"].nunique())
    col2.metric("📊 Indicators", df["indicator"].nunique())
    col3.metric("📁 Records", len(df))

    col4, col5, col6 = st.columns(3)
    col4.metric("⬇ Min", f"{df['value'].min():,.0f}")
    col5.metric("⬆ Max", f"{df['value'].max():,.0f}")
    col6.metric("📈 Avg", f"{df['value'].mean():,.0f}")

    # Records per country
    rec = df["country"].value_counts().reset_index()
    rec.columns = ["country", "count"]
    st.plotly_chart(px.bar(rec, x="country", y="count", title="Records per Country"), use_container_width=True)

    # ================= INTERMEDIATE =================
    st.header("🔸 Intermediate Analysis")

    q_country = df.groupby("country")["value"].sum().reset_index()

    st.plotly_chart(px.bar(q_country, x="country", y="value", title="Total Value per Country"), use_container_width=True)

    st.plotly_chart(px.bar(
        q_country.sort_values("value", ascending=False).head(10),
        x="country", y="value", title="Top 10 Countries"
    ), use_container_width=True)

    avg_country = df.groupby("country")["value"].mean().reset_index()
    st.plotly_chart(px.bar(avg_country, x="country", y="value", title="Average Value per Country"), use_container_width=True)

    q_ind = df.groupby("indicator")["value"].sum().reset_index()
    st.plotly_chart(px.pie(q_ind, names="indicator", values="value", title="Indicator Contribution"), use_container_width=True)

    # ================= ADVANCED =================
    st.header("🔺 Advanced Analysis")

    # % contribution
    contrib = q_country.copy()
    contrib["%"] = contrib["value"] / total_value * 100
    st.plotly_chart(px.pie(contrib, names="country", values="%", title="% Contribution by Country"), use_container_width=True)

    # Top 5 indicators
    st.plotly_chart(px.bar(
        q_ind.sort_values("value", ascending=False).head(5),
        x="indicator", y="value", title="Top 5 Indicators"
    ), use_container_width=True)

    # Heatmap
    pivot = df.pivot_table(values="value", index="country", columns="indicator", aggfunc="sum")
    st.plotly_chart(px.imshow(pivot, aspect="auto", title="Country vs Indicator Heatmap"), use_container_width=True)

    # Cumulative trend
    df_sorted = df.sort_values(["country", "year"])
    df_sorted["cum"] = df_sorted.groupby("country")["value"].cumsum()
    st.plotly_chart(px.line(df_sorted, x="year", y="cum", color="country", title="Cumulative Trend"), use_container_width=True)

    # Dominant indicator
    q30 = df.groupby(["country","indicator"])["value"].sum().reset_index()
    idx = q30.groupby("country")["value"].idxmax()
    dominant = q30.loc[idx]

    st.plotly_chart(px.bar(
        dominant, x="country", y="value", color="indicator",
        title="Dominant Indicator per Country"
    ), use_container_width=True)
