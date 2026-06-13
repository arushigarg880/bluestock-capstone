"""
live_nav_fetch.py
-----------------
Bluestock Fintech — Mutual Fund Analytics Platform
Capstone Project | June 2026

Description:
    Fetches live historical NAV data from mfapi.in REST API
    for 5 selected mutual fund schemes and saves as raw CSV.

    Schemes fetched:
    - SBI Bluechip (119551)
    - ICICI Bluechip (120503)
    - Nippon Large Cap (118632)
    - Axis Bluechip (119092)
    - Kotak Bluechip (120841)

Usage:
    python live_nav_fetch.py

Author: Arushi Garg
"""
import requests
import pandas as pd
import os
import time

def fetch_nav(scheme_code, scheme_name):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"Fetching: {scheme_name} (code: {scheme_code})")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['data'])
        df.columns = ['date', 'nav']
        df['nav'] = pd.to_numeric(df['nav'])
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
        df['amfi_code'] = scheme_code
        df['scheme_name'] = data['meta']['scheme_name']
        df['fund_house'] = data['meta']['fund_house']
        filename = f"data/raw/live_nav_{scheme_code}.csv"
        df.to_csv(filename, index=False)
        print(f"  {len(df)} rows saved → {filename}")
        return df
    else:
        print(f"  ERROR {response.status_code}")
        return None

# All 5 schemes
schemes = {
    125497: "HDFC Top 100",
    119551: "SBI Bluechip",
    120503: "ICICI Pru Bluechip",
    118632: "Nippon Large Cap",
    119092: "Axis Bluechip",
}

all_dfs = []
for code, name in schemes.items():
    df = fetch_nav(code, name)
    if df is not None:
        all_dfs.append(df)
    time.sleep(1)   # be polite to the API — wait 1 sec between requests

# Combine all into one master file
combined = pd.concat(all_dfs, ignore_index=True)
combined.to_csv("data/raw/live_nav_all_schemes.csv", index=False)
print(f"All done! Combined file: {len(combined)} rows total.")