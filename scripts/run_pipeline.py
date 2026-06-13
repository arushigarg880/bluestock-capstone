"""
run_pipeline.py
---------------
Bluestock Fintech — Mutual Fund Analytics Platform
Capstone Project | June 2026

Description:
    Master run script that executes the complete pipeline
    in correct order.

Usage:
    python run_pipeline.py

Author: Arushi Garg
"""

import subprocess
import sys

def run_script(script_name):
    """Run a Python script and print its status."""
    print(f"\n{'='*50}")
    print(f"▶ Running: {script_name}")
    print('='*50)
    result = subprocess.run(
        [sys.executable, script_name],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"✅ {script_name} completed successfully!")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"❌ {script_name} failed!")
        if result.stderr:
            print(result.stderr)

if __name__ == "__main__":
    print("🚀 Bluestock Fintech MF Analytics Pipeline Starting...")

    run_script("live_nav_fetch.py")
    run_script("data_ingestion.py")
    run_script("clean_data.py")
    run_script("load_to_db.py")
    run_script("run_queries.py")
    run_script("recommender.py")

    print("\n✅ Complete pipeline executed successfully!")
    print("📊 Open dashboard/bluestock_mf_dashboard.pbix in Power BI")