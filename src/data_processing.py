import pandas as pd

def process_and_save():

    # ---------------- LOAD ----------------
    debt = pd.read_csv("data/IDS_ALLCountries_Data.csv", encoding="latin1", low_memory=False)
    country = pd.read_csv("data/IDS_CountryMetaData.csv", encoding="latin1", low_memory=False)

    # ---------------- CLEAN COLUMNS ----------------
    debt.columns = debt.columns.astype(str)
    debt.columns = debt.columns.str.strip().str.lower().str.replace(" ", "_")
    country.columns = country.columns.str.strip().str.lower().str.replace(" ", "_")

    # ---------------- RENAME ----------------
    debt.rename(columns={
        "country_name": "country",
        "countrycode": "country_code",
        "country_code": "country_code",
        "series_name": "indicator",
        "series_code": "indicator_code"
    }, inplace=True)

    # ---------------- REMOVE UNWANTED YEARS ----------------
    drop_years = list(range(2000, 2006)) + list(range(2025, 2033))
    debt = debt.drop(columns=[str(y) for y in drop_years if str(y) in debt.columns])

    # ---------------- KEEP VALID YEARS (2006–2024) ----------------
    valid_years = [str(y) for y in range(2006, 2025) if str(y) in debt.columns]

    # ---------------- MELT ----------------
    df = debt.melt(
        id_vars=["country", "country_code", "indicator"],
        value_vars=valid_years,
        var_name="year",
        value_name="value"
    )

    # ---------------- CLEAN DATA ----------------
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    df = df.dropna(subset=["value"])

    df["value"] = df.groupby(["country", "indicator"])["value"].ffill()
    df["value"] = df.groupby(["country", "indicator"])["value"].bfill()

    df = df.dropna(subset=["value"])

    # ---------------- FINAL YEAR FILTER ----------------
    df = df[(df["year"] >= 2006) & (df["year"] <= 2024)]

    # ---------------- MERGE COUNTRY META ----------------
    if "code" in country.columns:
        country.rename(columns={"code": "country_code"}, inplace=True)

    if "country_code" in country.columns:
        df = df.merge(country, on="country_code", how="left")

    # ---------------- FILTER INDICATORS ----------------
    keywords = ["debt", "export", "import"]
    df = df[df["indicator"].str.contains('|'.join(keywords), case=False, na=False)]

    # ---------------- OPTIMIZE SIZE ----------------
    top_indicators = df["indicator"].value_counts().nlargest(15).index
    df = df[df["indicator"].isin(top_indicators)]

    top_countries = df.groupby("country")["value"].sum().nlargest(50).index
    df = df[df["country"].isin(top_countries)]

    df["country"] = df["country"].astype("category")
    df["indicator"] = df["indicator"].astype("category")
    df["value"] = df["value"].round(2)

    df = df.drop_duplicates()

    # ---------------- SAVE ----------------
    df.to_csv("data/final_cleaned_debt_data.csv", index=False)

    print("✅ FINAL DATASET CREATED (2006–2024)")


if __name__ == "__main__":
    process_and_save()