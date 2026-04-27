# 🌍 International Debt Analysis System

## 📌 Project Overview

The **International Debt Analysis System** is an end-to-end data analytics project that processes and analyzes global debt data using Python and visualization tools.

It integrates multiple datasets, performs data cleaning and transformation, and presents insights through an interactive **Streamlit dashboard** with multiple visualization types.

---

## 🎯 Objectives

* Integrate multiple international debt datasets
* Clean and preprocess raw financial data
* Remove null-heavy year columns (2000–2005, 2025–2032)
* Analyze trends from **2006 to 2024**
* Perform multi-level analytical queries
* Build an interactive visualization dashboard

---

## 📂 Dataset Used

This project uses **5 datasets**:

* `IDS_ALLCountries_Data.csv`
* `IDS_CountryMetaData.csv`
* `IDS_SeriesMetaData.csv`
* `Country-Series - Metadata.csv`
* `IDS_FootNoteMetaData.csv`

---

## ⚙️ Tech Stack

* **Language:** Python
* **Libraries:** Pandas, NumPy
* **Visualization:** Plotly, Matplotlib, Seaborn
* **Dashboard:** Streamlit

---

## 🔄 Project Workflow

### 1️⃣ Data Preprocessing

* Cleaned column names and handled encoding issues
* Removed null-heavy year columns (2000–2005, 2025–2032)
* Selected valid years **(2006–2024)**
* Converted data from wide format → long format
* Handled missing values using forward & backward filling
* Filtered relevant indicators (debt, export, import)
* Reduced dataset size using top countries & indicators

---

### 2️⃣ Data Analysis

* Implemented **30 analytical queries**

  * Basic
  * Intermediate
  * Advanced

---

### 3️⃣ Visualization

The dashboard includes multiple visualization types:

* 📈 Line Chart → Trend analysis
* 📊 Area Chart → Trend + volume
* 📊 Bar Chart → Comparison
* 🥧 Pie Chart → Proportion
* 📉 Histogram → Distribution
* 📦 Box Plot → Spread
* 🔵 Scatter Plot → Relationships
* 🔥 Heatmap → Correlation

---

### 4️⃣ Dashboard Features

* Multi-page Streamlit app:

  * 🌍 Dashboard (overview)
  * 📊 Queries (30 queries + charts)
  * 💡 Insights (interactive visual analysis)
* Dynamic filters:

  * Country
  * Indicator
  * Year range

---

## 📊 Key Features

* Uses all 5 datasets
* Dynamic filtering (no empty results)
* Optimized dataset for performance
* Interactive charts using Plotly
* Clean modular architecture

---

## 💡 Key Insights

* Debt trends show significant variation across countries
* Few countries contribute major share of global debt
* Certain indicators dominate financial patterns
* Strong year-wise trends observed from 2006–2024

---

## 🚀 How to Run the Project

### 1️⃣ Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 2️⃣ Process Data

```bash
python src/data_processing.py
```

### 3️⃣ Run the Dashboard

```bash
python -m streamlit run app/app.py
```

---

## 📁 Project Structure

```bash
international-debt-analysis-system/
│
├── app/
│   └── app.py
│
├── src/
│   ├── data_processing.py
│   ├── insights.py
│   └── queries.py
│
├── data/
│   ├── raw datasets (5 CSV files)
│   └── final_cleaned_debt_data.csv
```

---

## 🧠 Challenges Faced

* Handling encoding errors (`latin1`)
* Managing missing and null-heavy columns
* Aligning different dataset schemas
* Optimizing dataset size for performance
* Ensuring no empty visualization outputs

---

## 🏁 Results

* Built a complete data pipeline from raw data to insights
* Integrated multiple datasets successfully
* Created interactive and dynamic visualizations
* Delivered a fully functional dashboard

---

## 👩‍💻 Author

**Lawanya Duraisamy**

---

## 🧠 Viva Ready Points

* Explained removal of null-heavy year columns
* Justified use of multiple visualizations
* Demonstrated data cleaning and transformation
* Showcased interactive dashboard design

---

## 📌 Conclusion

This project demonstrates a complete data analytics workflow, from data preprocessing to visualization, highlighting the importance of structured analysis in global financial datasets.
