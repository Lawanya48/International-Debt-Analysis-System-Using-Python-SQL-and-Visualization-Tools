import streamlit as st
import plotly.express as px

def show_queries(df):

    st.title("📊 Visual SQL Analytics (All Queries)")

    # ---------------- COLUMN FIX (IMPORTANT) ----------------
    country_col = "country_name" if "country_name" in df.columns else "country"
    indicator_col = "indicator_name" if "indicator_name" in df.columns else "indicator"

    # ---------------- FILTER ----------------
    st.sidebar.header("Filters")

    country = st.sidebar.selectbox(
        "Country",
        ["All"] + sorted(df[country_col].dropna().unique())
    )

    if country != "All":
        df = df[df[country_col] == country]

    total_value = df["value"].sum()

    # ---------------- UNIQUE KEY FUNCTION ----------------
    key_counter = 0
    def plot(fig):
        nonlocal key_counter
        st.plotly_chart(fig, key=f"chart_{key_counter}", use_container_width=True)
        key_counter += 1

    # ================= BASIC =================
    st.header("🔹 Basic Queries")

    col1, col2, col3 = st.columns(3)
    col1.metric("Countries", df[country_col].nunique())
    col2.metric("Indicators", df[indicator_col].nunique())
    col3.metric("Records", len(df))

    col4, col5, col6 = st.columns(3)
    col4.metric("Min", f"{df['value'].min():,.0f}")
    col5.metric("Max", f"{df['value'].max():,.0f}")
    col6.metric("Avg", f"{df['value'].mean():,.0f}")

    rec = df[country_col].value_counts().reset_index()
    rec.columns = [country_col, "count"]
    plot(px.bar(rec, x=country_col, y="count", title="Records per Country"))

    high = df[df["value"] > 1_000_000_000]
    plot(px.histogram(high, x="value", title="Values > 1 Billion"))

    # ================= INTERMEDIATE =================
    st.header("🔸 Intermediate Queries")

    q_country = df.groupby(country_col)["value"].sum().reset_index()

    plot(px.bar(q_country, x=country_col, y="value", title="Total Value per Country"))

    plot(px.bar(q_country.sort_values("value", ascending=False).head(10),
                x=country_col, y="value", title="Top 10 Countries"))

    avg_country = df.groupby(country_col)["value"].mean().reset_index()
    plot(px.bar(avg_country, x=country_col, y="value", title="Average per Country"))

    q_ind = df.groupby(indicator_col)["value"].sum().reset_index()
    plot(px.pie(q_ind, names=indicator_col, values="value", title="Indicator Contribution"))

    plot(px.bar(q_ind.sort_values("value", ascending=False).head(1),
                x=indicator_col, y="value", title="Highest Indicator"))

    plot(px.bar(q_country.sort_values("value").head(1),
                x=country_col, y="value", title="Lowest Country"))

    pivot = df.pivot_table(values="value", index=country_col, columns=indicator_col, aggfunc="sum")
    pivot = pivot.fillna(0).iloc[:20, :20]   # limit size for stability
    plot(px.imshow(pivot, aspect="auto", title="Country vs Indicator Heatmap"))

    ind_count = df.groupby(country_col)[indicator_col].nunique().reset_index()
    plot(px.bar(ind_count, x=country_col, y=indicator_col, title="Indicator Count per Country"))

    avg = df["value"].mean()
    above = q_country[q_country["value"] > avg]
    plot(px.bar(above, x=country_col, y="value", title="Above Global Average"))

    q_country["rank"] = q_country["value"].rank(ascending=False)
    plot(px.bar(q_country, x=country_col, y="rank", title="Country Ranking"))

    # ================= ADVANCED =================
    st.header("🔺 Advanced Queries")

    plot(px.bar(q_ind.sort_values("value", ascending=False).head(5),
                x=indicator_col, y="value", title="Top 5 Indicators"))

    contrib = q_country.copy()
    contrib["%"] = contrib["value"] / total_value * 100
    plot(px.pie(contrib, names=country_col, values="%", title="% Contribution per Country"))

    q23 = df.groupby([indicator_col, country_col])["value"].sum().reset_index()
    top3 = q23.sort_values([indicator_col, "value"], ascending=[True, False]) \
              .groupby(indicator_col).head(3)

    plot(px.bar(top3, x=country_col, y="value", color=indicator_col,
                title="Top 3 Countries per Indicator"))

    diff = df.groupby(country_col)["value"].agg(lambda x: x.max() - x.min()).reset_index()
    plot(px.bar(diff, x=country_col, y="value", title="Difference (Max-Min)"))

    plot(px.bar(q_country.sort_values("value", ascending=False).head(10),
                x=country_col, y="value", title="Top 10 Countries"))

    def categorize(x):
        if x > 1e11: return "High"
        elif x > 1e9: return "Medium"
        else: return "Low"

    q_country["Category"] = q_country["value"].apply(categorize)
    plot(px.pie(q_country, names="Category", title="Debt Category"))

    df_sorted = df.sort_values([country_col, "year"])
    df_sorted["cum"] = df_sorted.groupby(country_col)["value"].cumsum()
    plot(px.line(df_sorted, x="year", y="cum", color=country_col, title="Cumulative Trend"))

    overall_avg = df["value"].mean()
    ind_avg = df.groupby(indicator_col)["value"].mean().reset_index()
    high_ind = ind_avg[ind_avg["value"] > overall_avg]
    plot(px.bar(high_ind, x=indicator_col, y="value", title="Indicators Above Avg"))

    big = contrib[contrib["%"] > 5]
    plot(px.bar(big, x=country_col, y="%", title="Countries >5% Contribution"))

    q30 = df.groupby([country_col, indicator_col])["value"].sum().reset_index()
    idx = q30.groupby(country_col)["value"].idxmax()
    dominant = q30.loc[idx]

    plot(px.bar(dominant, x=country_col, y="value", color=indicator_col,
                title="Dominant Indicator"))