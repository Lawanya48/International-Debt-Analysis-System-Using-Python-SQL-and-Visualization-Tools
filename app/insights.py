import streamlit as st
import plotly.express as px

def show_insights(df):

    st.title("📊 Insights Dashboard")

    # ---------------- COLUMN SAFETY ----------------
    country_col = "country_name" if "country_name" in df.columns else "country"
    indicator_col = "indicator_name" if "indicator_name" in df.columns else "indicator"

    # ---------------- SORT ----------------
    df = df.sort_values([country_col, indicator_col, "year"])

    # ---------------- HANDLE MISSING VALUES ----------------
    df["value"] = df.groupby([country_col, indicator_col])["value"].ffill()
    df["value"] = df.groupby([country_col, indicator_col])["value"].bfill()

    # ---------------- SIDEBAR FILTERS ----------------
    st.sidebar.subheader("🔍 Insights Filters")

    # Indicator filter
    indicators = sorted(df[indicator_col].dropna().unique())
    category = st.sidebar.selectbox("Indicator", ["All"] + indicators)

    if category != "All":
        df = df[df[indicator_col] == category]

    # Year filter (2006–2024)
    year_range = st.sidebar.slider(
        "Year Range",
        int(df["year"].min()),
        int(df["year"].max()),
        (2010, 2024)
    )

    df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

    # Country filter
    country = st.sidebar.selectbox(
        "Country",
        sorted(df[country_col].dropna().unique())
    )

    data = df[df[country_col] == country]

    if data.empty:
        st.warning("⚠ No data available for this selection")
        return

    st.subheader(f"{country} Analysis")

    # ---------------- KPI ----------------
    total_value = data["value"].sum()
    st.metric("Total Debt Value", f"{total_value:,.2f}")

    # ---------------- GLOBAL TREND ----------------
    st.subheader("🌍 Global Year-wise Trend")
    global_trend = df.groupby("year")["value"].sum().reset_index()
    st.plotly_chart(px.line(global_trend, x="year", y="value"))

    # ---------------- COUNTRY TREND ----------------
    st.subheader("📈 Country Year-wise Trend")
    trend = data.groupby("year")["value"].sum().reset_index()
    st.plotly_chart(px.line(trend, x="year", y="value"))

    # ---------------- AREA CHART ----------------
    st.subheader("📊 Area Chart (Trend + Volume)")
    st.plotly_chart(px.area(trend, x="year", y="value"))

    # ---------------- BAR CHART ----------------
    st.subheader("📊 Indicator Distribution")
    ind = data.groupby(indicator_col)["value"].sum().reset_index()
    st.plotly_chart(px.bar(ind, x=indicator_col, y="value"))

    # ---------------- PIE CHART ----------------
    st.subheader("🥧 Indicator Share")
    st.plotly_chart(px.pie(ind, names=indicator_col, values="value"))

    # ---------------- HISTOGRAM ----------------
    st.subheader("📉 Value Distribution")
    st.plotly_chart(px.histogram(data, x="value"))

    # ---------------- BOX PLOT ----------------
    st.subheader("📦 Value Spread")
    st.plotly_chart(px.box(data, y="value"))

    # ---------------- SCATTER ----------------
    st.subheader("🔵 Year vs Value (Scatter)")
    data = data.copy()
    data["size_value"] = data["value"].abs()

    st.plotly_chart(
        px.scatter(
            data,
            x="year",
            y="value",
            size="size_value",
            color=indicator_col
        )
    )

    # ---------------- HEATMAP ----------------
    st.subheader("🔥 Heatmap")

    pivot = data.pivot_table(
        values="value",
        index="year",
        columns=indicator_col,
        aggfunc="sum"
    ).fillna(0)

    st.plotly_chart(px.imshow(pivot, aspect="auto"))
