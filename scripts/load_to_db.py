import pandas as pd
import sqlite3
import os
from pathlib import Path
BASE = Path(__file__).parent.parent
DB_PATH = BASE / "data" / "db" / "bluestock_mf.db"

# ── Create database and tables from schema ─────
conn = sqlite3.connect(DB_PATH)
print(f"Database created: {DB_PATH}")

with open(BASE/"sql"/"schema.sql", "r") as f:
    schema_sql = f.read()

conn.executescript(schema_sql)
conn.commit()
print("Tables created from schema.sql")
# ── Load dim_fund ─────────────────────────────
fund = pd.read_csv(BASE / "data" / "raw" / "01_fund_master.csv")
fund.to_sql("dim_fund", conn, if_exists="replace", index=False)
print(f"dim_fund: {len(fund)} rows loaded")

# ── Load dim_date (build from nav dates) ──────
nav  = pd.read_csv(BASE / "data" / "processed" / "clean_nav.csv")
nav['date'] = pd.to_datetime(nav['date'])
dates = nav[['date']].drop_duplicates().copy()
dates['date_id']   = dates['date'].dt.strftime('%Y-%m-%d')
dates['year']      = dates['date'].dt.year
dates['month']     = dates['date'].dt.month
dates['quarter']   = dates['date'].dt.quarter
dates['month_name']= dates['date'].dt.strftime('%B')
dates['is_weekday']= (dates['date'].dt.dayofweek < 5).astype(int)
dates['date']      = dates['date_id']
dates.to_sql("dim_date", conn, if_exists="replace", index=False)
print(f"dim_date: {len(dates)} rows loaded")

# ── Load fact_nav ─────────────────────────────
nav['date_id'] = pd.to_datetime(nav['date']).dt.strftime('%Y-%m-%d')
nav[['amfi_code','date_id','nav','daily_return_pct']].to_sql(
    "fact_nav", conn, if_exists="replace", index=False)
print(f"fact_nav: {len(nav)} rows loaded")

# ── Load fact_transactions ─────────────────────
tx   = pd.read_csv(BASE / "data" / "processed" / "clean_transactions.csv")
tx['date_id'] = pd.to_datetime(tx['date']).dt.strftime('%Y-%m-%d')
tx.to_sql("fact_transactions", conn, if_exists="replace", index=False)
print(f"fact_transactions: {len(tx)} rows loaded")

# ── Load fact_performance ──────────────────────
perf = pd.read_csv(BASE / "data" / "processed" / "clean_performance.csv")
perf.to_sql("fact_performance", conn, if_exists="replace", index=False)
print(f"fact_performance: {len(perf)} rows loaded")

# ── Load fact_aum ──────────────────────────────
aum  = pd.read_csv(BASE / "data" / "raw" / "03_aum_by_fund_house.csv")
aum.to_sql("fact_aum", conn, if_exists="replace", index=False)
print(f"fact_aum: {len(aum)} rows loaded")

# ── Load fact_sip_industry ─────────────────────
sip  = pd.read_csv(BASE / "data" / "raw" / "04_monthly_sip_inflows.csv")
sip.to_sql("fact_sip_industry", conn, if_exists="replace", index=False)
print(f"fact_sip_industry: {len(sip)} rows loaded")

conn.close()
print("\nAll data loaded into bluestock_mf.db!")