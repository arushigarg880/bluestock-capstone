CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code        TEXT PRIMARY KEY,
    fund_house       TEXT NOT NULL,
    scheme_name      TEXT NOT NULL,
    category         TEXT,
    sub_category     TEXT,
    plan             TEXT,
    benchmark        TEXT,
    expense_ratio_pct REAL,
    exit_load_pct    REAL,
    min_sip_amount   REAL,
    fund_manager     TEXT,
    risk_category    TEXT,
    sebi_category_code TEXT,
    launch_date      TEXT
);
CREATE TABLE IF NOT EXISTS dim_date (
    date_id    TEXT PRIMARY KEY,
    date       TEXT NOT NULL,
    year       INTEGER,
    month      INTEGER,
    quarter    INTEGER,
    month_name TEXT,
    is_weekday INTEGER
);

-- FACT TABLE 1: Daily NAV
CREATE TABLE IF NOT EXISTS fact_nav (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code       TEXT REFERENCES dim_fund(amfi_code),
    date_id         TEXT REFERENCES dim_date(date_id),
    nav             REAL NOT NULL,
    daily_return_pct REAL
);

-- FACT TABLE 2: Investor transactions
CREATE TABLE IF NOT EXISTS fact_transactions (
    tx_id            TEXT PRIMARY KEY,
    investor_id      TEXT,
    amfi_code        TEXT REFERENCES dim_fund(amfi_code),
    date_id          TEXT REFERENCES dim_date(date_id),
    amount           REAL,
    transaction_type TEXT,
    state            TEXT,
    city             TEXT,
    age_group        TEXT,
    kyc_status       TEXT
);

-- FACT TABLE 3: Scheme performance metrics
CREATE TABLE IF NOT EXISTS fact_performance (
    amfi_code      TEXT REFERENCES dim_fund(amfi_code),
    as_of_date     TEXT,
    return_1yr     REAL,
    return_3yr     REAL,
    return_5yr     REAL,
    sharpe         REAL,
    sortino        REAL,
    alpha          REAL,
    beta           REAL,
    max_drawdown   REAL,
    std_dev        REAL
);

-- FACT TABLE 4: AUM by fund house
CREATE TABLE IF NOT EXISTS fact_aum (
    fund_house   TEXT,
    date_id      TEXT,
    aum_crore    REAL,
    num_schemes  INTEGER
);

-- FACT TABLE 5: Portfolio holdings
CREATE TABLE IF NOT EXISTS fact_portfolio (
    amfi_code    TEXT REFERENCES dim_fund(amfi_code),
    stock_symbol TEXT,
    weight_pct   REAL,
    sector       TEXT,
    date_id      TEXT
);

-- FACT TABLE 6: Industry SIP data
CREATE TABLE IF NOT EXISTS fact_sip_industry (
    month              TEXT PRIMARY KEY,
    sip_inflow_crore   REAL,
    sip_accounts_crore REAL,
    new_registrations  REAL
);

-- INDEXES for fast queries
CREATE INDEX IF NOT EXISTS idx_nav_code ON fact_nav(amfi_code);
CREATE INDEX IF NOT EXISTS idx_nav_date ON fact_nav(date_id);
CREATE INDEX IF NOT EXISTS idx_tx_code  ON fact_transactions(amfi_code);
CREATE INDEX IF NOT EXISTS idx_tx_state ON fact_transactions(state);