# Data Dictionary — Bluestock Fintech MF Analytics

## dim_fund
| Column | Type | Description | Source |
|--------|------|-------------|--------|
| amfi_code | TEXT (PK) | Unique AMFI scheme code | AMFI India |
| fund_house | TEXT | Fund house / AMC name | AMFI India |
| scheme_name | TEXT | Full scheme name | AMFI India |
| category | TEXT | Category (Equity/Debt/Hybrid) | AMFI India |
| expense_ratio_pct | REAL | Annual management fee % | mfdata.in |
| risk_category | TEXT | SEBI risk label | AMFI India |

## dim_date
| Column | Type | Description |
|--------|------|-------------|
| date_id | TEXT (PK) | Date in YYYY-MM-DD format |
| year | INT | Calendar year |
| month | INT | Month number (1-12) |
| quarter | INT | Quarter (1-4) |
| is_weekday | INT | 1 = weekday, 0 = weekend |

## fact_nav
| Column | Type | Description | Source |
|--------|------|-------------|--------|
| amfi_code | TEXT (FK) | Links to dim_fund | AMFI / mfapi.in |
| date_id | TEXT (FK) | Links to dim_date | AMFI / mfapi.in |
| nav | REAL | NAV value in Rs. | AMFI / mfapi.in |
| daily_return_pct | REAL | % change from previous day | Computed |

## fact_transactions
| Column | Type | Description |
|--------|------|-------------|
| investor_id | TEXT | Unique investor ID |
| transaction_date | TEXT | Date of transaction |
| amfi_code | TEXT (FK) | Links to dim_fund |
| transaction_type | TEXT | SIP / Lumpsum / Redemption |
| amount_inr | REAL | Transaction amount in Rs. |
| state | TEXT | Indian state of investor |
| city | TEXT | City of investor |
| city_tier | TEXT | T30 or B30 city |
| age_group | TEXT | Investor age bracket |
| gender | TEXT | Investor gender |
| annual_income_lakh | REAL | Annual income in lakhs |
| payment_mode | TEXT | UPI / Cheque / Mandate |
| kyc_status | TEXT | Verified or Pending |

## fact_performance
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | TEXT (FK) | Links to dim_fund |
| scheme_name | TEXT | Full scheme name |
| return_1yr_pct | REAL | 1-year CAGR return % |
| return_3yr_pct | REAL | 3-year CAGR return % |
| return_5yr_pct | REAL | 5-year CAGR return % |
| alpha | REAL | Jensen's Alpha vs benchmark |
| beta | REAL | Market sensitivity (1 = moves with market) |
| sharpe_ratio | REAL | Return per unit of risk |
| sortino_ratio | REAL | Return per unit of downside risk |
| max_drawdown_pct | REAL | Worst peak-to-trough fall % |
| std_dev_ann_pct | REAL | Annualised standard deviation |
| expense_ratio_pct | REAL | Annual fee % charged by fund |
| morningstar_rating | INT | Star rating (1-5) |
| risk_grade | TEXT | Low / Moderate / High |

## fact_aum
| Column | Type | Description |
|--------|------|-------------|
| fund_house | TEXT | Fund house name |
| aum_crore | REAL | AUM in Rs. crore |
| num_schemes | INT | Number of schemes managed |

## fact_sip_industry
| Column | Type | Description |
|--------|------|-------------|
| month | TEXT | Month in YYYY-MM format |
| sip_inflow_crore | REAL | Monthly SIP inflow in Rs. crore |
| sip_accounts_crore | REAL | Active SIP accounts in crore |
| new_registrations | REAL | New SIP registrations that month |

---
*Generated for Bluestock Fintech Capstone Project*