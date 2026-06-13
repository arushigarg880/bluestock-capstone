<div align="center">

# 🏦 Bluestock Fintech
## Mutual Fund Analytics Platform

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?style=for-the-badge&logo=sqlite&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-yellow?style=for-the-badge&logo=powerbi&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-orange?style=for-the-badge&logo=jupyter&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-Repo-black?style=for-the-badge&logo=github&logoColor=white)

**Capstone Project | Data Analyst Intern | Bluestock Fintech Pvt. Ltd. | June 2026**

*An end-to-end Mutual Fund Analytics Platform covering 40 real schemes, 87,000+ rows of data, and 5 bonus challenges*

---

[📊 View Dashboard](#dashboard) • [🚀 Quick Start](#how-to-run) • [📁 Data Sources](#data-sources) • [🏆 Bonus Challenges](#bonus-challenges)

</div>

---

## 📌 Project Overview

Bluestock Fintech is a financial technology company focused on democratising investment analytics for retail and institutional investors in India. This capstone project is a **full-stack Mutual Fund Analytics Platform** that:

- Ingests publicly available data from **AMFI India** and free public APIs
- Transforms it through a robust **ETL pipeline** with error handling and validation
- Stores it in a **normalised SQLite database** with star schema design
- Analyses it using **Python-based risk and performance metrics**
- Presents insights via a **4-page interactive Power BI dashboard**
- Includes **5 bonus features** including Streamlit app, Monte Carlo simulation, and Markowitz Efficient Frontier

### 🇮🇳 Industry Context

| Metric | Value | Source |
|--------|-------|--------|
| Industry AUM | Rs. 81 lakh crore | AMFI India |
| Total MF Schemes | 1,908 | AMFI India |
| Total Investor Folios | 26.12 crore | AMFI / Business Standard |
| Monthly SIP Inflow (Dec 2025) | Rs. 31,002 crore *(all-time high)* | AMFI Monthly Note |
| Active SIP Accounts | 9.35 crore | AMFI Monthly Note |
| SBI MF AUM | Rs. 12.50 lakh crore *(largest AMC)* | AMFI Quarterly |

---

## 🗂️ Project Structure

```
bluestock_capstone/
├── data/
│   ├── raw/                    ← 10 original CSV datasets
│   ├── processed/              ← 7 cleaned + computed CSVs
│   └── db/
│       └── bluestock_mf.db     ← SQLite database (8 tables)
├── notebooks/
│   ├── EDA_Analysis.ipynb      ← 15+ publication-quality charts
│   └── Performance_Analytics.ipynb  ← Sharpe, Alpha, Beta, VaR
├── scripts/
│   ├── data_ingestion.py       ← Loads all 10 raw datasets
│   ├── clean_data.py           ← Cleans and validates all data
│   ├── live_nav_fetch.py       ← Fetches live NAV from mfapi.in
│   ├── load_to_db.py           ← Loads data into SQLite database
│   ├── run_queries.py          ← Runs 10 analytical SQL queries
│   ├── markowitz.py            ← Efficient Frontier optimisation (B4)
│   ├── email_report.py         ← HTML email report generator (B5)
│   └── run_pipeline.py         ← Master pipeline run script
├── sql/
│   ├── schema.sql              ← Star schema CREATE TABLE statements
│   └── queries.sql             ← 10 analytical SQL queries
├── dashboard/
│   └── bluestock_mf_dashboard.pbix  ← Power BI dashboard
├── reports/
│   ├── chart_01_nav_trend.png
│   ├── chart_02_aum_growth.png
│   ├── chart_03_sip_trend.png
│   ├── chart_04_category_heatmap.png
│   ├── chart_05_demographics.png
│   ├── chart_06_geo_distribution.png
│   ├── chart_07_folio_growth.png
│   ├── chart_08_correlation.png
│   ├── chart_09_sector_allocation.png
│   ├── efficient_frontier.png  ← Markowitz chart (B4)
│   ├── weekly_report.html      ← HTML email report (B5)
│   ├── Final_Report.pdf
│   └── Presentation.pptx
├── data_dictionary.md          ← Column-level documentation
├── requirements.txt
└── README.md
```

---

## ⚙️ Tech Stack

| Category | Tool / Library |
|----------|---------------|
| Language | Python 3.11 |
| Data Processing | Pandas, NumPy |
| Visualisation | Matplotlib, Seaborn, Plotly |
| Statistics & Optimisation | SciPy |
| Database | SQLite3, SQLAlchemy |
| Dashboard | Power BI Desktop |
| Web App | Streamlit *(Bonus B2)* |
| Notebooks | Jupyter Lab / VS Code |
| API | mfapi.in *(no auth required)* |
| Version Control | Git, GitHub |

---

## 📁 Dataset Inventory

| File | Rows | Description |
|------|------|-------------|
| `01_fund_master.csv` | 40 | Master list — AMFI codes, fund house, category, expense ratio |
| `02_nav_history.csv` | ~46,000 | Daily NAV for 40 schemes from Jan 2022 to May 2026 |
| `03_aum_by_fund_house.csv` | ~90 | Quarterly AUM for top 10 fund houses |
| `04_monthly_sip_inflows.csv` | 48 | Monthly SIP inflow, active accounts, new registrations |
| `05_category_inflows.csv` | ~144 | Net inflows by category (FY 2024-25) |
| `06_industry_folio_count.csv` | 21 | Total folios by Equity, Debt, Hybrid |
| `07_scheme_performance.csv` | 40 | 1yr/3yr/5yr returns, Sharpe, Alpha, Beta, Max Drawdown |
| `08_investor_transactions.csv` | ~32,000 | SIP + Lumpsum + Redemption for 5,000 investors |
| `09_portfolio_holdings.csv` | ~320 | Top equity holdings by fund (stock, weight %, sector) |
| `10_benchmark_indices.csv` | ~8,000 | Daily closing — Nifty 50, Nifty 100, BSE SmallCap, CRISIL |

---

## 🗄️ Database Schema (Star Schema)

```
                    ┌─────────────┐
                    │  dim_fund   │
                    │  (40 rows)  │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
  ┌──────▼──────┐  ┌───────▼──────┐  ┌──────▼──────────┐
  │  fact_nav   │  │fact_transact │  │fact_performance │
  │ (46K rows)  │  │ (32K rows)   │  │   (40 rows)     │
  └─────────────┘  └──────────────┘  └─────────────────┘
         │
  ┌──────▼──────┐
  │  dim_date   │
  │ (1,150 rows)│
  └─────────────┘
```

| Table | Type | Rows |
|-------|------|------|
| `dim_fund` | Dimension | 40 |
| `dim_date` | Dimension | 1,150 |
| `fact_nav` | Fact | 46,000 |
| `fact_transactions` | Fact | 32,778 |
| `fact_performance` | Fact | 40 |
| `fact_aum` | Fact | 90 |
| `fact_portfolio` | Fact | 320 |
| `fact_sip_industry` | Fact | 48 |

---

## 🚀 How to Run

### Step 1 — Clone the Repository
```bash
git clone https://github.com/arushigarg880/bluestock-mf-capstone.git
cd bluestock-mf-capstone
```

### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Run Complete Pipeline
```bash
python scripts/run_pipeline.py
```

Expected output:
```
🚀 Bluestock Fintech MF Analytics Pipeline Starting...
✅ data_ingestion.py completed successfully!
✅ clean_data.py completed successfully!
✅ load_to_db.py completed successfully!
✅ run_queries.py completed successfully!
✅ Complete pipeline executed successfully!
```

### Step 4 — Open Notebooks
```bash
jupyter lab
```
Open notebooks in order: `EDA_Analysis.ipynb` → `Performance_Analytics.ipynb`

### Step 5 — Open Power BI Dashboard
Open `dashboard/bluestock_mf_dashboard.pbix` in Power BI Desktop

### Step 6 — Run Streamlit App *(Bonus B2)*
```bash
streamlit run scripts/streamlit_app.py
```

---

## 📊 Key Results

| Metric | Value |
|--------|-------|
| Fund schemes analysed | 40 |
| Years of NAV data | 4.5 years (Jan 2022 – May 2026) |
| Total data rows processed | 87,000+ |
| Investor transactions analysed | 32,778 |
| Database tables | 8 |
| EDA charts generated | 15+ |
| Risk metrics computed per fund | 7 (Sharpe, Sortino, Alpha, Beta, Max DD, VaR, CVaR) |
| Dashboard pages | 4 |
| SQL queries written | 10 |
| Bonus challenges completed | 5 / 5 |

---

## 📈 Performance Metrics Computed

| Metric | Formula | Purpose |
|--------|---------|---------|
| **Sharpe Ratio** | (Rp - Rf) / σp × √252 | Return per unit of total risk |
| **Sortino Ratio** | (Rp - Rf) / σ_downside × √252 | Return per unit of downside risk |
| **Alpha (Jensen's)** | Intercept × 252 from OLS regression | Excess return vs benchmark |
| **Beta** | Slope from OLS regression vs Nifty 100 | Market sensitivity |
| **Max Drawdown** | min(NAV / running_max - 1) | Worst peak-to-trough fall |
| **CAGR** | (NAV_end/NAV_start)^(252/n_days) - 1 | Annualised compound growth |
| **VaR (95%)** | 5th percentile of return distribution | Maximum likely daily loss |

> Risk-free rate used: **6.5% p.a.** (RBI repo rate proxy)
> Trading days used for annualisation: **252** (not calendar days)

---

## 🏆 Bonus Challenges

| # | Challenge | Status | Output |
|---|-----------|--------|--------|
| **B1** | Scheduled ETL — auto NAV fetch every weekday at 8 PM | ✅ Complete | Cron / Task Scheduler |
| **B2** | Streamlit web app as Power BI alternative | ✅ Complete | `streamlit_app.py` |
| **B3** | Monte Carlo simulation — 5-year NAV projection with uncertainty bands | ✅ Complete | Monte Carlo chart |
| **B4** | Markowitz Efficient Frontier — optimal portfolio for 5 funds | ✅ Complete | `efficient_frontier.png` |
| **B5** | Automated HTML email report — weekly performance summary | ✅ Complete | `weekly_report.html` |

### B4 — Markowitz Efficient Frontier Results
```
Optimal Portfolio (Max Sharpe = 1.04):
  Expected Annual Return : 22.90%
  Annual Risk (Std Dev)  : 15.80%

Optimal Weights:
  SBI Small Cap Fund     : 25.8%
  Nippon India Small Cap : 56.0%
  ABSL Small Cap Fund    : 8.2%
  Axis Small Cap Fund    : 5.0%
  SBI Small Cap (Direct) : 5.0%
```

---

## 📁 Data Sources

| Source | URL | Data |
|--------|-----|------|
| AMFI India | www.amfiindia.com | NAV, AUM, Folio, SIP |
| mfapi.in | api.mfapi.in/mf/{code} | Historical NAV (JSON) |
| mfdata.in | mfdata.in/api/v1/schemes | NAV + Expense Ratio |
| NSE India | nseindia.com/reports | Nifty index prices |
| BSE India | bseindia.com | BSE SmallCap index |
| AMFI Monthly Notes | amfiindia.com/research | Industry SIP & Flow Data |

> All data is **publicly available and free** — no proprietary or paid sources used.

---

## 📅 7-Day Project Breakdown

| Day | Focus | Key Deliverable |
|-----|-------|----------------|
| Day 1 | Data Ingestion + Live API Fetch | `data_ingestion.py`, 15 raw CSV files |
| Day 2 | Data Cleaning + SQLite Database | `bluestock_mf.db`, `schema.sql`, `queries.sql` |
| Day 3 | Exploratory Data Analysis | `EDA_Analysis.ipynb`, 9 charts |
| Day 4 | Performance Analytics | `Performance_Analytics.ipynb`, `fund_scorecard.csv` |
| Day 5 | Power BI Dashboard | 4-page interactive `.pbix` file |
| Day 6 | Advanced Analytics + Bonus | VaR, CVaR, Monte Carlo, Markowitz, Streamlit |
| Day 7 | Final Report + Submission | PDF report, slides, GitHub cleanup |

---

## ✅ Deliverables Checklist

- [x] **D1** — ETL pipeline script (`run_pipeline.py`) — *runs without manual steps*
- [x] **D2** — SQLite database (`bluestock_mf.db`) — *8 tables, star schema*
- [x] **D3** — EDA notebook (`EDA_Analysis.ipynb`) — *15+ charts*
- [x] **D4** — Performance metrics (`Performance_Analytics.ipynb`) — *Sharpe, Beta, VaR*
- [x] **D5** — Power BI dashboard (`.pbix`) — *4 pages, slicers on every page*
- [x] **D6** — Advanced analytics — *VaR, CVaR, cohort analysis, recommender*
- [x] **D7** — Final report + slides — *PDF + PPTX*
- [x] **B1** — Scheduled ETL cron job
- [x] **B2** — Streamlit web app
- [x] **B3** — Monte Carlo simulation
- [x] **B4** — Markowitz Efficient Frontier
- [x] **B5** — HTML email report generator

---

## ⚠️ Important Notes

- `.db` files are excluded from GitHub via `.gitignore` — use `schema.sql` to recreate the database
- All file paths use `pathlib.Path` for cross-platform compatibility
- NAV missing values (weekends/holidays) handled with `ffill()` after reindexing
- CAGR computed using **252 trading days** (not 365 calendar days) as per industry standard
- Risk-free rate: **6.5% p.a.** (RBI repo rate proxy, annualised to daily: 6.5/100/252)

---

## ⚠️ Disclaimer

All data is sourced from publicly available AMFI India information. This project is for **educational purposes only** and does not constitute financial advice. Mutual Fund investments are subject to market risks. Please read all scheme-related documents carefully before investing.

---

## 👤 Author

**Arushi Garg**
Data Analyst Intern
Bluestock Fintech Pvt. Ltd.
June 2026



