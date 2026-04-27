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
        st.error("❌ Metadata file not found. Please check data folder.")
        st.stop()

    # Fix encoding issue
    try:
        meta = pd.read_csv(meta_path, encoding="utf-8")
    except:
        meta = pd.read_csv(meta_path, encoding="latin1")

    # ---------------- FIND CORRECT COUNTRY COLUMN ----------------
    possible_cols = ["Country Name", "country", "Country", "Long Name"]

    meta_col = None
    for col in possible_cols:
        if col in meta.columns:
            meta_col = col
            break

    if meta_col is None:
        st.error("❌ No matching country column found in metadata")
        st.write("Available columns:", list(meta.columns))
        st.stop()

    # ---------------- MERGE ----------------
    df = df.merge(meta, left_on="country", right_on=meta_col, how="left")

    # ---------------- DATA CLEANING ----------------
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
        st.warning("No data available for selected country")
        return

    st.subheader(f"{country} Analysis")

    # ---------------- KPI ----------------
    st.metric("💰 Total Value", f"{data['value'].sum():,.2f}")

    # ---------------- METADATA VISUALIZATION ----------------
    st.subheader("📌 Country Metadata Overview")

    meta_cols = [
        "Latest agricultural census",
        "Latest industrial data",
        "Latest trade data",
        "Latest water withdrawal data",
        "Latest population census"
    ]

    # Keep only available columns
    meta_cols = [col for col in meta_cols if col in data.columns]

    if meta_cols:
        meta_values = data[meta_cols].iloc[0].replace("..", None)

        meta_df = pd.DataFrame({
            "Category": meta_cols,
            "Year": pd.to_numeric(meta_values.values, errors="coerce")
        }).dropna()

        if not meta_df.empty:
            st.plotly_chart(
                px.bar(meta_df, x="Category", y="Year",
                       title="Latest Available Data (Year-wise)"),
                use_container_width=True
            )
        else:
            st.warning("Metadata exists but contains no usable values")
    else:
        st.warning("Metadata columns not found in dataset")

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
    st.subheader("🔵 Scatter Plot (Year vs Value)")
    data["size_value"] = data["value"].abs()
    st.plotly_chart(
        px.scatter(data, x="year", y="value", size="size_value"),
        use_container_width=True
    )

    # ---------------- HEATMAP ----------------
    st.subheader("🔥 Heatmap (Year vs Indicator)")
    pivot = data.pivot_table(values="value", index="year",
                             columns="indicator", aggfunc="sum")

    if not pivot.empty:
        st.plotly_chart(px.imshow(pivot, aspect="auto"),
                        use_container_width=True)
    else:
        st.warning("No data available for heatmap")
