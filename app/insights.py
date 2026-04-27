import streamlit as st
import pandas as pd
import plotly.express as px
import os

def show_insights(df):

    st.title("📊 Insights Dashboard")

    df = df.copy()

    # ---------------- LOAD METADATA ----------------
    base_path = os.path.dirname(__file__)
    meta_path = os.path.join(base_path, "..", "data", "IDS_CountryMetaData.csv")

    if not os.path.exists(meta_path):
        st.error("❌ Metadata file not found")
        st.stop()

    try:
        meta = pd.read_csv(meta_path, encoding="utf-8")
    except:
        meta = pd.read_csv(meta_path, encoding="latin1")

    # Detect country column
    meta_col = None
    for col in ["Country Name", "country", "Country", "Long Name"]:
        if col in meta.columns:
            meta_col = col
            break

    if meta_col is None:
        st.error("❌ Country column not found in metadata")
        st.stop()

    # Merge
    df = df.merge(meta, left_on="country", right_on=meta_col, how="left")

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

    # ---------------- METADATA VISUALIZATION ----------------
    st.subheader("📌 Metadata Year Overview")

    meta_cols = {
        "Agriculture": "Latest agricultural census",
        "Industry": "Latest industrial data",
        "Trade": "Latest trade data",
        "Population": "Latest population census",
        "Water": "Latest water withdrawal data"
    }

    meta_values = []

    for key, col in meta_cols.items():
        if col in data.columns:
            val = data[col].iloc[0]

            if val not in ["..", "", None]:
                try:
                    meta_values.append((key, int(val)))
                except:
                    pass

    if meta_values:
        meta_df = pd.DataFrame(meta_values, columns=["Category", "Year"])

        st.plotly_chart(
            px.bar(meta_df, x="Category", y="Year", color="Category",
                   title="Latest Data Year by Sector"),
            use_container_width=True
        )
    else:
        st.warning("No metadata available")

    # ---------------- LINE CHART ----------------
    st.subheader("📈 Year-wise Trend")
    trend = data.groupby("year")["value"].sum().reset_index()
    st.plotly_chart(px.line(trend, x="year", y="value"), use_container_width=True)

    # ---------------- BAR CHART ----------------
    st.subheader("📊 Indicator Distribution")
    ind = data.groupby("indicator")["value"].sum().reset_index()
    st.plotly_chart(px.bar(ind, x="indicator", y="value"), use_container_width=True)

    # ---------------- PIE ----------------
    st.subheader("🥧 Indicator Share")
    st.plotly_chart(px.pie(ind, names="indicator", values="value"), use_container_width=True)

    # ---------------- HISTOGRAM ----------------
    st.subheader("📉 Value Distribution")
    st.plotly_chart(px.histogram(data, x="value"), use_container_width=True)

    # ---------------- BOX ----------------
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
