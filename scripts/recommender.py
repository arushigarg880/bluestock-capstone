"""
recommender.py
--------------
Bluestock Fintech — Mutual Fund Analytics Platform
Capstone Project | June 2026

Description:
    Fund recommendation engine that suggests top 3 mutual
    funds based on investor risk appetite using Sharpe Ratio.

Usage:
    python recommender.py

    Or import as function:
    from recommender import recommend_funds
    recommend_funds('Low')
    recommend_funds('Moderate')
    recommend_funds('High')

Author: Arushi Garg
"""
import pandas as pd

def recommend_funds(risk_appetite, performance_path='../data/processed/clean_performance.csv'):
    """
    Recommends top 3 mutual funds based on investor risk appetite.
    
    Parameters:
    -----------
    risk_appetite : str
        'Low', 'Moderate', or 'High'
    
    Returns:
    --------
    DataFrame with top 3 recommended funds
    """
    performance = pd.read_csv(performance_path)
    
    filtered = performance[
        performance['risk_grade'].str.lower() == risk_appetite.lower()
    ]
    
    if filtered.empty:
        print(f"No funds found for risk appetite: {risk_appetite}")
        return None
    
    top3 = filtered.nlargest(3, 'sharpe_ratio')[
        ['scheme_name', 'sharpe_ratio', 'return_3yr_pct', 'risk_grade']
    ]
    
    print(f"\n✅ Top 3 funds for {risk_appetite} risk investors:")
    print(top3.to_string(index=False))
    return top3

if __name__ == "__main__":
    for risk in ['Low', 'Moderate', 'High']:
        recommend_funds(risk)