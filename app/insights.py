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
        st.error("Metadata file not found")
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
        st.error("Country column not found in metadata")
        st.stop()

    df = df.merge(meta, left_on="country", right_on=meta_col, how="left")

    # ---------------- FILTER ----------------
    st.sidebar.header("🔍 Filters")

    country = st.sidebar.selectbox(
        "Country",
        sorted(df["country"].dropna().unique())
    )

    category = st.sidebar.selectbox(
        "Category",
        ["All", "Agriculture", "Industry", "Trade", "Population", "Water"]
    )

    data = df[df["country"] == country]

    if data.empty:
        st.warning("No data available")
        return

    st.subheader(f"{country} Analysis")

    # ---------------- CATEGORY MAP ----------------
    category_map = {
        "Agriculture": "Latest agricultural census",
        "Industry": "Latest industrial data",
        "Trade": "Latest trade data",
        "Population": "Latest population census",
        "Water": "Latest water withdrawal data"
    }

    # ---------------- EXTRACT METADATA ----------------
    meta_values = []
    for cat, col in category_map.items():
        if col in data.columns:
            val = data[col].iloc[0]

            if val not in ["..", "", None]:
                try:
                    meta_values.append((cat, int(val)))
                except:
                    pass

    if not meta_values:
        st.warning("No usable metadata found")
        return

    meta_df = pd.DataFrame(meta_values, columns=["Category", "Year"])

    # ---------------- VISUALIZATION ----------------
    st.subheader("📌 Metadata Year Visualization")

    if category != "All":
        meta_df = meta_df[meta_df["Category"] == category]

    st.plotly_chart(
        px.bar(
            meta_df,
            x="Category",
            y="Year",
            color="Category",
            title=f"{country} - Latest Data Year by Category"
        ),
        use_container_width=True
    )

    # ---------------- KPI ----------------
    st.metric("💰 Total Value", f"{data['value'].sum():,.2f}")

    # ---------------- TREND ----------------
    st.subheader("📈 Year-wise Trend")
    trend = data.groupby("year")["value"].sum().reset_index()
    st.plotly_chart(px.line(trend, x="year", y="value"), use_container_width=True)

    # ---------------- OTHER CHARTS ----------------
    st.subheader("📊 Indicator Distribution")
    ind = data.groupby("indicator")["value"].sum().reset_index()
    st.plotly_chart(px.bar(ind, x="indicator", y="value"), use_container_width=True)

    st.subheader("🥧 Indicator Share")
    st.plotly_chart(px.pie(ind, names="indicator", values="value"), use_container_width=True)

    st.subheader("📉 Histogram")
    st.plotly_chart(px.histogram(data, x="value"), use_container_width=True)

    st.subheader("📦 Box Plot")
    st.plotly_chart(px.box(data, y="value"), use_container_width=True)

    st.subheader("🔵 Scatter")
    data["size_value"] = data["value"].abs()
    st.plotly_chart(px.scatter(data, x="year", y="value", size="size_value"), use_container_width=True)

    st.subheader("🔥 Heatmap")
    pivot = data.pivot_table(values="value", index="year", columns="indicator", aggfunc="sum")
    if not pivot.empty:
        st.plotly_chart(px.imshow(pivot, aspect="auto"), use_container_width=True)
