-- ================================================
-- Bluestock Fintech | queries.sql
-- 10 analytical SQL queries
-- ================================================

-- Q1: Top 5 fund houses by latest AUM
SELECT fund_house,
       ROUND(MAX(aum_crore), 2) AS latest_aum_crore
FROM fact_aum
GROUP BY fund_house
ORDER BY latest_aum_crore DESC
LIMIT 5;

-- Q2: Average NAV per month for each scheme
SELECT f.scheme_name,
       d.year,
       d.month_name,
       ROUND(AVG(n.nav), 2) AS avg_nav
FROM fact_nav n
JOIN dim_fund f ON n.amfi_code = f.amfi_code
JOIN dim_date d ON n.date_id = d.date_id
GROUP BY f.scheme_name, d.year, d.month
ORDER BY f.scheme_name, d.year, d.month;

-- Q3: SIP inflow year-on-year growth
SELECT year,
       ROUND(SUM(sip_inflow_crore), 2) AS total_sip,
       ROUND(SUM(sip_inflow_crore) - LAG(SUM(sip_inflow_crore))
             OVER (ORDER BY year), 2) AS yoy_growth
FROM fact_sip_industry s
JOIN dim_date d ON s.month = d.date_id
GROUP BY year
ORDER BY year;

-- Q4: Total transactions by state (top 10)
SELECT state,
       COUNT(*) AS num_transactions,
       ROUND(SUM(amount), 2) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC
LIMIT 10;

-- Q5: Funds with expense ratio below 1%
SELECT f.scheme_name,
       f.fund_house,
       f.expense_ratio_pct,
       p.return_1yr,
       p.sharpe
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
WHERE f.expense_ratio_pct < 1.0
ORDER BY p.return_1yr DESC;

-- Q6: Top 5 best performing funds (1-year return)
SELECT f.scheme_name,
       f.fund_house,
       f.category,
       ROUND(p.return_1yr, 2) AS return_1yr_pct,
       ROUND(p.sharpe, 3) AS sharpe_ratio
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.return_1yr DESC
LIMIT 5;

-- Q7: Monthly SIP trend (last 12 months)
SELECT month,
       ROUND(sip_inflow_crore, 2) AS sip_crore,
       ROUND(sip_accounts_crore, 3) AS sip_accounts_crore
FROM fact_sip_industry
ORDER BY month DESC
LIMIT 12;

-- Q8: Transaction count by type
SELECT transaction_type,
       COUNT(*) AS count,
       ROUND(SUM(amount), 2) AS total_amount,
       ROUND(AVG(amount), 2) AS avg_amount
FROM fact_transactions
GROUP BY transaction_type;

-- Q9: Funds with highest Alpha (beating benchmark most)
SELECT f.scheme_name,
       f.fund_house,
       ROUND(p.alpha, 4) AS alpha,
       ROUND(p.beta, 4) AS beta,
       ROUND(p.return_1yr, 2) AS return_1yr_pct
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.alpha DESC
LIMIT 5;

-- Q10: AUM growth by fund house (2022 to latest)
SELECT fund_house,
       ROUND(MIN(aum_crore), 2) AS aum_start,
       ROUND(MAX(aum_crore), 2) AS aum_latest,
       ROUND(MAX(aum_crore) - MIN(aum_crore), 2) AS growth
FROM fact_aum
GROUP BY fund_house
ORDER BY growth DESC;