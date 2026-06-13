# 🏦 Bluestock Fintech — Mutual Fund Analytics Platform

## Capstone Project | Data Analyst Intern | June 2026

---

## 📌 Project Overview

An end-to-end Mutual Fund Analytics Platform built for
Bluestock Fintech Pvt. Ltd. covering 40 real mutual fund
schemes from 10 major AMCs with 87,000+ rows of data.

The platform includes:
- Automated ETL pipeline from AMFI India public data
- Normalised SQLite database with star schema design
- 15+ EDA charts revealing industry trends
- Risk-adjusted performance metrics for all 40 schemes
- 4-page interactive Power BI dashboard
- Fund recommendation engine for 3 risk profiles

---

## 🗂️ Project Structure

bluestock_mf_capstone/
├── data/
│   ├── raw/               ← Original CSV files (10 datasets)
│   └── processed/         ← Cleaned CSV files
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda_analysis.ipynb
│   ├── 04_performance_analytics.ipynb
│   └── 05_advanced_analytics.ipynb
├── scripts/
│   ├── data_ingestion.py  ← Loads all 10 raw datasets
│   ├── clean_data.py      ← Cleans and validates all data
│   ├── live_nav_fetch.py  ← Fetches live NAV from mfapi.in
│   ├── load_to_db.py      ← Loads data into SQLite database
│   ├── run_queries.py     ← Runs 10 analytical SQL queries
│   ├── recommender.py     ← Fund recommendation engine
│   └── run_pipeline.py    ← Master run script
├── sql/
│   ├── schema.sql         ← CREATE TABLE statements
│   └── queries.sql        ← 10 analytical queries
├── dashboard/
│   └── bluestock_mf_dashboard.pbix
├── reports/
│   ├── Final_Report.pdf
│   ├── Bluestock_MF_Presentation.pptx
│   ├── Dashboard.pdf
│   └── *.png              ← Charts and screenshots
├── requirements.txt
└── README.md

---

## ⚙️ Tech Stack

| Category | Tool |
|---|---|
| Language | Python 3.10+ |
| Data Processing | Pandas, NumPy |
| Visualisation | Matplotlib, Seaborn, Plotly |
| Statistics | SciPy |
| Database | SQLite, SQLAlchemy |
| Dashboard | Power BI Desktop |
| Notebooks | Jupyter Lab |
| API | mfapi.in (no auth required) |
| Version Control | Git, GitHub |

---

## 🚀 How to Run

### Step 1 — Clone the Repository
git clone https://github.com/arushigarg880/bluestock-mf-capstone.git
cd bluestock-mf-capstone

### Step 2 — Install Dependencies
pip install -r requirements.txt

### Step 3 — Run Complete Pipeline
python scripts/run_pipeline.py

### Step 4 — Open Notebooks in Order
Open notebooks 01 through 05 in Jupyter Lab.

### Step 5 — Open Dashboard
Open dashboard/bluestock_mf_dashboard.pbix in Power BI Desktop.

---

## 📊 Key Results

| Metric | Value |
|---|---|
| Fund schemes analysed | 40 |
| Years of NAV data | 4.5 years |
| Total data rows | 87,000+ |
| Investor transactions | 32,000+ |
| Dashboard pages | 4 |
| Risk metrics computed | 6 |
| Industry AUM covered | Rs. 81 lakh crore |
| Record SIP inflow | Rs. 31,002 crore (Dec 2025) |

---

## 📁 Data Sources

- AMFI India: https://www.amfiindia.com
- mfapi.in REST API: https://api.mfapi.in
- NSE India: https://www.nseindia.com

---

## 7-Day Project Breakdown

| Day | Focus | Key Deliverable |
|---|---|---|
| Day 1 | Data Ingestion + API Fetch | Raw CSVs + live_nav_fetch.py |
| Day 2 | Data Cleaning + SQLite DB | bluestock_mf.db + schema.sql |
| Day 3 | Exploratory Data Analysis | 15+ charts + EDA notebook |
| Day 4 | Performance Analytics | Fund scorecard + metrics |
| Day 5 | Power BI Dashboard | 4-page interactive dashboard |
| Day 6 | Advanced Analytics + Risk | VaR, CVaR, Recommender |
| Day 7 | Report + Presentation + GitHub | Final submission package |

---

## ⚠️ Disclaimer

All data is sourced from publicly available AMFI India information.
This project is for educational purposes only and does not
constitute financial advice. Mutual Fund investments are subject
to market risks.

---

## 👤 Author

Arushi Garg
Data Analyst Intern
Bluestock Fintech Pvt. Ltd.
June 2026