import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from scipy.optimize import minimize
from pathlib import Path

BASE    = Path(__file__).parent.parent
RF      = 0.065 / 252

nav = pd.read_csv(BASE / "data/processed/returns_computed.csv", parse_dates=['date'])
fund = pd.read_csv(BASE / "data/raw/01_fund_master.csv")
perf = pd.read_csv(BASE / "data/processed/clean_performance.csv")

top5 = perf.nlargest(5, 'return_1yr_pct')['amfi_code'].tolist()
print("Selected funds:")
for code in top5:
    name = fund[fund['amfi_code']==code]['scheme_name'].values[0]
    print(f"  {code}: {name[:40]}")

returns_pivot = (nav[nav['amfi_code'].isin(top5)]
                 .pivot_table(index='date', columns='amfi_code', values='daily_return')
                 .dropna())

print(f"Returns matrix: {returns_pivot.shape}")

mean_returns = returns_pivot.mean() * 252
cov_matrix   = returns_pivot.cov() * 252
n_funds      = len(top5)

print("Annualised returns per fund:")
for code, ret in mean_returns.items():
    name = fund[fund['amfi_code']==code]['scheme_name'].values[0][:25]
    print(f"  {name}: {ret*100:.2f}%")

np.random.seed(42)
N_PORTFOLIOS = 10000

port_returns = []
port_risks   = []
port_sharpes = []
port_weights = []

for _ in range(N_PORTFOLIOS):
    w = np.random.random(n_funds)
    w = w / w.sum()
    
    ret  = np.dot(w, mean_returns)
    risk = np.sqrt(w.T @ cov_matrix.values @ w)
    sharpe = (ret - RF * 252) / risk
    
    port_returns.append(ret)
    port_risks.append(risk)
    port_sharpes.append(sharpe)
    port_weights.append(w)

port_returns = np.array(port_returns)
port_risks   = np.array(port_risks)
port_sharpes = np.array(port_sharpes)

def neg_sharpe(weights):
    ret   = np.dot(weights, mean_returns)
    risk  = np.sqrt(weights.T @ cov_matrix.values @ weights)
    return -(ret - RF * 252) / risk

constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
bounds = tuple((0.05, 0.60) for _ in range(n_funds))
init_w = np.array([1/n_funds] * n_funds)

result = minimize(neg_sharpe, init_w,
                  method='SLSQP',
                  bounds=bounds,
                  constraints=constraints)

opt_w      = result.x
opt_return = np.dot(opt_w, mean_returns)
opt_risk   = np.sqrt(opt_w.T @ cov_matrix.values @ opt_w)
opt_sharpe = (opt_return - RF * 252) / opt_risk

print(f"Optimal Portfolio (Max Sharpe):")
print(f"  Expected Annual Return: {opt_return*100:.2f}%")
print(f"  Annual Risk (Std Dev):  {opt_risk*100:.2f}%")
print(f"  Sharpe Ratio:           {opt_sharpe:.4f}")
print(f"Optimal Weights:")
for i, code in enumerate(top5):
    name = fund[fund['amfi_code']==code]['scheme_name'].values[0][:30]
    print(f"  {name}: {opt_w[i]*100:.1f}%")

fig, ax = plt.subplots(figsize=(12, 8))

scatter = ax.scatter(port_risks * 100, port_returns * 100,
                     c=port_sharpes, cmap='viridis',
                     alpha=0.4, s=8)
plt.colorbar(scatter, ax=ax, label='Sharpe Ratio')

ax.scatter(opt_risk * 100, opt_return * 100,
           color='red', s=200, zorder=5,
           marker='*', label=f'Max Sharpe Portfolio(Sharpe={opt_sharpe:.2f})')

min_risk_idx = np.argmin(port_risks)
ax.scatter(port_risks[min_risk_idx] * 100,
           port_returns[min_risk_idx] * 100,
           color='blue', s=150, zorder=5,
           marker='D', label='Min Risk Portfolio')

for i, code in enumerate(top5):
    name = fund[fund['amfi_code']==code]['scheme_name'].values[0].split('-')[0][:15]
    ind_risk   = np.sqrt(cov_matrix.values[i, i]) * 100
    ind_return = mean_returns.iloc[i] * 100
    ax.scatter(ind_risk, ind_return, s=100, zorder=5, marker='o')
    ax.annotate(name, (ind_risk, ind_return),
                textcoords='offset points', xytext=(5, 5), fontsize=8)

ax.set_title('Markowitz Efficient Frontier — 5 Selected Funds', fontsize=14, pad=15)
ax.set_xlabel('Annual Risk / Volatility (%)')
ax.set_ylabel('Expected Annual Return (%)')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(BASE / "reports/efficient_frontier.png", dpi=150, bbox_inches='tight')
plt.show()
print("Saved → reports/efficient_frontier.png")

weights_df = pd.DataFrame({
    'amfi_code': top5,
    'scheme_name': [fund[fund['amfi_code']==c]['scheme_name'].values[0] for c in top5],
    'optimal_weight_pct': (opt_w * 100).round(2)
})
weights_df.to_csv(BASE / "data/processed/optimal_portfolio.csv", index=False)
print("Saved → data/processed/optimal_portfolio.csv")