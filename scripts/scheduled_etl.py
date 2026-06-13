"""
scheduled_etl.py
----------------
Bluestock Fintech — Mutual Fund Analytics Platform
Capstone Project | June 2026

Description:
    Scheduled ETL script that automatically fetches fresh NAV data
    from mfapi.in every weekday at 8:00 PM and saves to raw folder.

Usage:
    python scripts/scheduled_etl.py
    (Keep this running in background — it will auto-fetch at 8 PM)

Author: [Your Name]
"""

import schedule
import time
import requests
import pandas as pd
from datetime import datetime
import os

# ─────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────
SCHEME_CODES = {
    'SBI Bluechip':       119551,
    'ICICI Bluechip':     120503,
    'Nippon Large Cap':   118632,
    'Axis Bluechip':      119092,
    'Kotak Bluechip':     120841,
    'HDFC Top 100':       125497,
    'Mirae Large Cap':    118989,
    'DSP Top 100':        108008,
    'UTI Nifty Index':    120716,
    'Aditya BSL Frontline': 119521
}

RAW_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'data', 'raw'
)

LOG_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'reports', 'etl_log.txt'
)

# ─────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────
def log(message):
    """Log message with timestamp to console and log file."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_msg = f"[{timestamp}] {message}"
    print(full_msg)
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(full_msg + '\n')
    except Exception:
        pass

# ─────────────────────────────────────────
# FETCH NAV FROM mfapi.in
# ─────────────────────────────────────────
def fetch_nav(scheme_name, scheme_code):
    """
    Fetch historical NAV for one scheme from mfapi.in.

    Parameters:
    -----------
    scheme_name : str — Human readable fund name
    scheme_code : int — AMFI scheme code

    Returns:
    --------
    DataFrame with date and nav columns, or None if failed
    """
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            records = data.get('data', [])
            if not records:
                log(f"  ⚠️  No data returned for {scheme_name}")
                return None
            df = pd.DataFrame(records)
            df.columns = ['date', 'nav']
            df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
            df['nav'] = pd.to_numeric(df['nav'], errors='coerce')
            df['amfi_code'] = scheme_code
            df['scheme_name'] = scheme_name
            df = df.dropna(subset=['nav'])
            df = df.sort_values('date')
            log(f"  ✅  {scheme_name}: {len(df)} rows fetched")
            return df
        else:
            log(f"  ❌  {scheme_name}: HTTP {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        log(f"  ❌  {scheme_name}: Request timed out")
        return None
    except Exception as e:
        log(f"  ❌  {scheme_name}: {str(e)}")
        return None

# ─────────────────────────────────────────
# MAIN ETL JOB
# ─────────────────────────────────────────
def run_etl():
    """
    Main ETL job — fetches NAV for all schemes and saves to CSV.
    Runs automatically every weekday at 8 PM.
    """
    log("=" * 55)
    log("🚀 SCHEDULED ETL JOB STARTED")
    log("=" * 55)

    # Check if today is a weekday
    today = datetime.now()
    if today.weekday() >= 5:
        log("📅 Today is weekend — skipping NAV fetch")
        log("=" * 55)
        return

    all_data = []
    success_count = 0
    fail_count = 0

    log(f"📡 Fetching NAV for {len(SCHEME_CODES)} schemes...")

    for name, code in SCHEME_CODES.items():
        df = fetch_nav(name, code)
        if df is not None:
            all_data.append(df)
            success_count += 1
        else:
            fail_count += 1
        # Small delay to avoid rate limiting
        time.sleep(0.5)

    if all_data:
        # Combine all schemes
        combined = pd.concat(all_data, ignore_index=True)

        # Save to raw folder
        filename = f"live_nav_{today.strftime('%Y%m%d')}.csv"
        filepath = os.path.join(RAW_FOLDER, filename)
        combined.to_csv(filepath, index=False)

        # Also update the master nav file
        master_path = os.path.join(RAW_FOLDER, 'live_nav_latest.csv')
        combined.to_csv(master_path, index=False)

        log(f"💾 Saved {len(combined)} rows to {filename}")
        log(f"💾 Updated live_nav_latest.csv")
        log(f"✅ Success: {success_count} schemes")
        log(f"❌ Failed:  {fail_count} schemes")
    else:
        log("❌ No data fetched — all requests failed")

    log("=" * 55)
    log("✅ ETL JOB COMPLETE")
    log("=" * 55)

# ─────────────────────────────────────────
# SCHEDULER
# ─────────────────────────────────────────
def start_scheduler():
    """Start the schedule — runs ETL every weekday at 8 PM."""
    log("⏰ Bluestock Fintech — Scheduled ETL Starting...")
    log(f"📅 Schedule: Every weekday at 20:00")
    log(f"📁 Saving to: {RAW_FOLDER}")
    log("Press Ctrl+C to stop\n")

    # Schedule for 8 PM every day
    schedule.every().day.at("20:00").do(run_etl)

    # Also run immediately once on startup
    log("▶ Running initial ETL fetch now...")
    run_etl()

    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

# ─────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────
if __name__ == "__main__":
    start_scheduler()