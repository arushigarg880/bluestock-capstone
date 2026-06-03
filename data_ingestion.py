import pandas as pd
import os

DATA_PATH = "data/raw/"

files = {
    "fund_master":          "01_fund_master.csv",
    "nav_history":          "02_nav_history.csv",
    "aum_by_fund_house":    "03_aum_by_fund_house.csv",
    "monthly_sip":          "04_monthly_sip_inflows.csv",
    "category_inflows":     "05_category_inflows.csv",
    "folio_count":          "06_industry_folio_count.csv",
    "scheme_performance":   "07_scheme_performance.csv",
    "investor_transactions":"08_investor_transactions.csv",
    "portfolio_holdings":   "09_portfolio_holdings.csv",
    "benchmark_indices":    "10_benchmark_indices.csv",
}

dataframes = {}

for name, filename in files.items():
    filepath = os.path.join(DATA_PATH, filename)
    df = pd.read_csv(filepath)
    dataframes[name] = df
    print(f"{'='*50}")
    print(f"Dataset: {name}")
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"Columns: {list(df.columns)}")
    print(f"Dtypes:{df.dtypes}")
    print(f"First 3 rows:")
    print(df.head(3))

print("All 10 datasets loaded successfully!")
print(f"Total datasets: {len(dataframes)}")