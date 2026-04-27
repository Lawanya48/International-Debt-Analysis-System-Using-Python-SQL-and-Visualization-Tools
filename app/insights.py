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
    for col in ["Country Name", "country", "Country", "Long Name"]:
        if col in meta.columns:
            meta_col = col
            break

    df = df.merge(meta, left_on="country", right_on=meta_col, how="left")

    # ---------------- FILTERS ----------------
    st.sidebar.header("🔍 Insights Filters")

    category = st.sidebar.selectbox(
        "Category",
        ["All", "Agriculture", "Industry", "Trade", "Population", "Water"]
    )

    country = st.sidebar.selectbox(
        "Country",
        sorted(df["country"].dropna().unique())
    )

    data = df[df["country"] == country]

    if data.empty:
        st.warning("No data available")
        return

    st.subheader(f"{country} - {category} Analysis")

    # ---------------- KPI ----------------
    st.metric("💰 Total Value", f"{data['value'].sum():,.2f}")

    # ---------------- CATEGORY → METADATA ----------------
    category_map = {
        "Agriculture": "Latest agricultural census",
        "Industry": "Latest industrial data",
        "Trade": "Latest trade data",
        "Population": "Latest population census",
        "Water": "Latest water withdrawal data"
    }

    if category != "All":

        col_name = category_map.get(category)

        if col_name in data.columns:

            val = data[col_name].iloc[0]

            # Clean value
            if val in ["..", "", None]:
                st.warning(f"No metadata available for {category}")
            else:
                try:
                    year_val = int(val)
                    st.success(f"📅 {category} Latest Data Year: {year_val}")
                except:
                    st.warning(f"Invalid metadata value for {category}")
        else:
            st.warning(f"{category} column not found")

    # ---------------- METADATA OVERVIEW ----------------
    st.subheader("📌 Country Metadata Overview")

    meta_cols = list(category_map.values())
    meta_cols = [c for c in meta_cols if c in data.columns]

    clean_data = []
    for col in meta_cols:
        val = data[col].iloc[0]

        if val not in ["..", "", None]:
            try:
                clean_data.append((col, int(val)))
            except:
                pass

    if clean_data:
        meta_df = pd.DataFrame(clean_data, columns=["Category", "Year"])
        st.plotly_chart(px.bar(meta_df, x="Category", y="Year"), use_container_width=True)
    else:
        st.warning("No metadata available")

    # ---------------- TIME SERIES ----------------
    st.subheader("📈 Year-wise Trend")
    trend = data.groupby("year")["value"].sum().reset_index()
    st.plotly_chart(px.line(trend, x="year", y="value"), use_container_width=True)

    # ---------------- DISTRIBUTION ----------------
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
