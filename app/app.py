import streamlit as st
import pandas as pd
import plotly.express as px

def show_queries(df):

    st.title("📊 SQL Analytical Queries (Visual Dashboard)")

    df = df.copy()

    # ---------------- KEY HANDLER ----------------
    key_counter = 0
    def plot(fig):
        nonlocal key_counter
        st.plotly_chart(fig, key=f"chart_{key_counter}", use_container_width=True)
        key_counter += 1

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
    plot(px.bar(rec, x="country", y="count", title="Records per Country"))

    # High values
    high = df[df["value"] > 1_000_000_000]
    plot(px.histogram(high, x="value", title="Values > 1 Billion"))

    # ================= INTERMEDIATE =================
    st.header("🔸 Intermediate Analysis")

    q_country = df.groupby("country")["value"].sum().reset_index()

    plot(px.bar(q_country, x="country", y="value", title="Total Value per Country"))

    plot(px.bar(
        q_country.sort_values("value", ascending=False).head(10),
        x="country", y="value", title="Top 10 Countries"
    ))

    avg_country = df.groupby("country")["value"].mean().reset_index()
    plot(px.bar(avg_country, x="country", y="value", title="Average Value per Country"))

    q_ind = df.groupby("indicator")["value"].sum().reset_index()
    plot(px.pie(q_ind, names="indicator", values="value", title="Indicator Contribution"))

    plot(px.bar(
        q_ind.sort_values("value", ascending=False).head(1),
        x="indicator", y="value", title="Highest Indicator"
    ))

    plot(px.bar(
        q_country.sort_values("value").head(1),
        x="country", y="value", title="Lowest Country"
    ))

    # Heatmap
    pivot = df.pivot_table(values="value", index="country", columns="indicator", aggfunc="sum")
    plot(px.imshow(pivot, aspect="auto", title="Country vs Indicator Heatmap"))

    # Indicator count
    ind_count = df.groupby("country")["indicator"].nunique().reset_index()
    plot(px.bar(ind_count, x="country", y="indicator", title="Indicator Count per Country"))

    # Above average
    avg = df["value"].mean()
    above = q_country[q_country["value"] > avg]
    plot(px.bar(above, x="country", y="value", title="Above Global Average"))

    # Ranking
    q_country["rank"] = q_country["value"].rank(ascending=False)
    plot(px.bar(q_country, x="country", y="rank", title="Country Ranking"))

    # ================= ADVANCED =================
    st.header("🔺 Advanced Analysis")

    plot(px.bar(
        q_ind.sort_values("value", ascending=False).head(5),
        x="indicator", y="value", title="Top 5 Indicators"
    ))

    contrib = q_country.copy()
    contrib["%"] = contrib["value"] / total_value * 100
    plot(px.pie(contrib, names="country", values="%", title="% Contribution per Country"))

    # Top 3 countries per indicator
    q23 = df.groupby(["indicator","country"])["value"].sum().reset_index()
    top3 = q23.sort_values(["indicator","value"], ascending=[True,False]).groupby("indicator").head(3)
    plot(px.bar(top3, x="country", y="value", color="indicator", title="Top 3 Countries per Indicator"))

    # Difference max-min
    diff = df.groupby("country")["value"].agg(lambda x: x.max()-x.min()).reset_index()
    plot(px.bar(diff, x="country", y="value", title="Difference (Max-Min)"))

    # Top 10 again (view)
    plot(px.bar(
        q_country.sort_values("value", ascending=False).head(10),
        x="country", y="value", title="Top 10 Countries Overview"
    ))

    # Category
    def categorize(x):
        if x > 1e11: return "High"
        elif x > 1e9: return "Medium"
        else: return "Low"

    q_country["Category"] = q_country["value"].apply(categorize)
    plot(px.pie(q_country, names="Category", title="Debt Category"))

    # Cumulative
    df_sorted = df.sort_values(["country","year"])
    df_sorted["cum"] = df_sorted.groupby("country")["value"].cumsum()
    plot(px.line(df_sorted, x="year", y="cum", color="country", title="Cumulative Trend"))

    # Indicators above avg
    overall_avg = df["value"].mean()
    ind_avg = df.groupby("indicator")["value"].mean().reset_index()
    high_ind = ind_avg[ind_avg["value"] > overall_avg]
    plot(px.bar(high_ind, x="indicator", y="value", title="Indicators Above Average"))

    # Countries >5%
    big = contrib[contrib["%"] > 5]
    plot(px.bar(big, x="country", y="%", title="Countries >5% Contribution"))

    # Dominant indicator
    q30 = df.groupby(["country","indicator"])["value"].sum().reset_index()
    idx = q30.groupby("country")["value"].idxmax()
    dominant = q30.loc[idx]
    plot(px.bar(dominant, x="country", y="value", color="indicator", title="Dominant Indicator per Country"))
