"""
clean_data.py
-------------
Bluestock Fintech — Mutual Fund Analytics Platform
Capstone Project | June 2026

Description:
    Cleans and validates all 10 raw datasets including:
    - Parsing dates to datetime format
    - Forward-filling missing NAV values for holidays
    - Removing duplicate rows
    - Standardising transaction type values
    - Validating numeric columns and ranges
    Saves cleaned files to data/processed/ folder.

Usage:
    python clean_data.py

Author: Arushi Garg
"""
import pandas as pd
import numpy as np
import os

os.makedirs("data/processed", exist_ok=True)

# ── Load ──────────────────────────────────────
df = pd.read_csv("data/raw/02_nav_history.csv")
print("Raw shape:", df.shape)
print("Columns:", df.columns.tolist())
print("\nFirst look:")
print(df.head(3))

# ── 1. Parse dates ────────────────────────────
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# ── 2. Sort by fund + date ─────────────────────
df = df.sort_values(['amfi_code','date']).reset_index(drop=True)

# ── 3. Forward-fill missing NAV (holidays/gaps) ─
df['nav'] = df.groupby('amfi_code')['nav'].ffill()

# ── 4. Remove duplicates ───────────────────────
before = len(df)
df = df.drop_duplicates(subset=['amfi_code','date'])
print(f"Duplicates removed: {before - len(df)}")

# ── 5. Remove invalid NAV (must be > 0) ────────
df = df[df['nav'] > 0]

# ── 6. Add daily return % column ──────────────
df['daily_return_pct'] = df.groupby('amfi_code')['nav'].pct_change() * 100

# ── Save ───────────────────────────────────────
df.to_csv("data/processed/clean_nav.csv", index=False)
print(f"\nClean shape: {df.shape}")
print("Saved → data/processed/clean_nav.csv")

import re

# ── Load ──────────────────────────────────────
tx = pd.read_csv("data/raw/08_investor_transactions.csv")
print("\nTransactions raw shape:", tx.shape)
print("Columns:", tx.columns.tolist())
print(tx.head(3))
# ── 1. Standardise transaction_type ───────────
#    (make all variations consistent)
tx['transaction_type'] = tx['transaction_type'].str.strip().str.title()

# Map variations to standard names
type_map = {
    'Sip': 'SIP',
    'Systematic Investment Plan': 'SIP',
    'Lumpsum': 'Lumpsum',
    'Lump Sum': 'Lumpsum',
    'Redemption': 'Redemption',
    'Redeem': 'Redemption',
}
tx['transaction_type'] = tx['transaction_type'].replace(type_map)

print("Transaction types after cleaning:")
print(tx['transaction_type'].value_counts())

# ── 2. Remove invalid amounts (must be > 0) ───
tx = tx[tx['amount_inr'] > 0]


# ── 3. Fix date format ─────────────────────────
tx['date'] = pd.to_datetime(tx['transaction_date'], format='%Y-%m-%d')

# ── 4. Check KYC status values ─────────────────
print("\nKYC status values:")
print(tx['kyc_status'].value_counts() if 'kyc_status' in tx.columns else "No kyc_status column")

# ── Save ───────────────────────────────────────
tx.to_csv("data/processed/clean_transactions.csv", index=False)
print(f"\nClean transactions shape: {tx.shape}")
print("Saved → data/processed/clean_transactions.csv")
# ── Load ──────────────────────────────────────
perf = pd.read_csv("data/raw/07_scheme_performance.csv")
print("\nPerformance raw shape:", perf.shape)
print("Columns:", perf.columns.tolist())

# ── 1. Make sure return columns are numeric ────
return_cols = [c for c in perf.columns if 'return' in c.lower()]
for col in return_cols:
    perf[col] = pd.to_numeric(perf[col], errors='coerce')

# ── 2. Flag negative Sharpe ratios (not errors,
#    but worth noting — means fund lost money) ──
if 'sharpe' in perf.columns:
    neg_sharpe = perf[perf['sharpe'] < 0]
    print(f"\nFunds with negative Sharpe: {len(neg_sharpe)}")
    if len(neg_sharpe) > 0:
        print(neg_sharpe[['amfi_code','sharpe']])

# ── 3. Validate expense_ratio range 0.1% – 2.5%
exp_col = [c for c in perf.columns if 'expense' in c.lower()]
if exp_col:
    col = exp_col[0]
    out_of_range = perf[(perf[col] < 0.1) | (perf[col] > 2.5)]
    print(f"\nExpense ratios out of range: {len(out_of_range)}")

# ── 4. Fill any missing numeric values with median
num_cols = perf.select_dtypes(include=np.number).columns
perf[num_cols] = perf[num_cols].fillna(perf[num_cols].median())

# ── Save ───────────────────────────────────────
perf.to_csv("data/processed/clean_performance.csv", index=False)
print(f"\nClean performance shape: {perf.shape}")
print("Saved → data/processed/clean_performance.csv")