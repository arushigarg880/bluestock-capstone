"""
run_queries.py
--------------
Bluestock Fintech — Mutual Fund Analytics Platform
Capstone Project | June 2026

Description:
    Runs 10 analytical SQL queries on the SQLite database
    (bluestock_mf.db) and prints results including:
    - Top 5 funds by AUM
    - Average NAV per month
    - SIP inflow YoY growth
    - Transactions by state
    - Funds with expense ratio below 1%

Usage:
    python run_queries.py

Author: Arushi Garg
"""
import sqlite3
import pandas as pd

conn = sqlite3.connect("bluestock_mf.db")

queries = {
    "Top 5 fund houses by AUM": """
        SELECT fund_house, ROUND(MAX(aum_crore),2) AS latest_aum_crore
        FROM fact_aum GROUP BY fund_house
        ORDER BY latest_aum_crore DESC LIMIT 5""",

    "Top 5 funds by 1yr return": """
        SELECT f.scheme_name, ROUND(p.return_1yr_pct,2) AS return_1yr_pct,
               ROUND(p.sharpe_ratio,3) AS sharpe_ratio
        FROM fact_performance p
        JOIN dim_fund f ON p.amfi_code=f.amfi_code
        ORDER BY p.return_1yr_pct DESC LIMIT 5""",

    "Transactions by type": """
        SELECT transaction_type, COUNT(*) AS count,
               ROUND(SUM(amount_inr),2) AS total
        FROM fact_transactions GROUP BY transaction_type""",

    "Top 5 funds by Alpha": """
        SELECT scheme_name, fund_house,
               ROUND(alpha,4) AS alpha,
               ROUND(beta,4) AS beta,
               ROUND(return_1yr_pct,2) AS return_1yr_pct
        FROM fact_performance
        ORDER BY alpha DESC LIMIT 5""",

    "Funds with expense ratio below 1%": """
        SELECT scheme_name, fund_house,
               ROUND(expense_ratio_pct,2) AS expense_ratio_pct,
               ROUND(return_1yr_pct,2) AS return_1yr_pct,
               ROUND(sharpe_ratio,3) AS sharpe_ratio
        FROM fact_performance
        WHERE expense_ratio_pct < 1.0
        ORDER BY return_1yr_pct DESC"""
}

for title, sql in queries.items():
    print(f"\n{'='*50}")
    print(f"Query: {title}")
    df = pd.read_sql_query(sql, conn)
    print(df.to_string(index=False))

conn.close()