-- =====================================================
-- NIFTY100 FINANCIAL ANALYTICS
-- SQLite Database Schema
-- Sprint 1 - Day 4
-- =====================================================

DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS profitandloss;
DROP TABLE IF EXISTS balancesheet;
DROP TABLE IF EXISTS cashflow;
DROP TABLE IF EXISTS analysis;
DROP TABLE IF EXISTS financial_ratios;

---------------------------------------------------------
-- Companies
---------------------------------------------------------

CREATE TABLE companies (

    id TEXT PRIMARY KEY,

    company_logo TEXT,

    company_name TEXT,

    chart_link TEXT,

    about_company TEXT,

    website TEXT,

    nse_profile TEXT,

    bse_profile TEXT,

    face_value REAL,

    book_value REAL,

    roce_percentage REAL,

    roe_percentage REAL
);

---------------------------------------------------------
-- Profit & Loss
---------------------------------------------------------

CREATE TABLE profitandloss (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    year INTEGER,

    sales REAL,

    expenses REAL,

    operating_profit REAL,

    opm_percentage REAL,

    other_income REAL,

    interest REAL,

    depreciation REAL,

    profit_before_tax REAL,

    tax_percentage REAL,

    net_profit REAL,

    eps REAL,

    dividend_payout REAL
);

---------------------------------------------------------
-- Balance Sheet
---------------------------------------------------------

CREATE TABLE balancesheet (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    year INTEGER,

    equity_capital REAL,

    reserves REAL,

    borrowings REAL,

    other_liabilities REAL,

    total_liabilities REAL,

    fixed_assets REAL,

    cwip REAL,

    investments REAL,

    other_asset REAL,

    total_assets REAL
);

---------------------------------------------------------
-- Cash Flow
---------------------------------------------------------

CREATE TABLE cashflow (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    year INTEGER,

    operating_activity REAL,

    investing_activity REAL,

    financing_activity REAL,

    net_cash_flow REAL
);

---------------------------------------------------------
-- Analysis
---------------------------------------------------------

CREATE TABLE analysis (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    compounded_sales_growth REAL,

    compounded_profit_growth REAL,

    stock_price_cagr REAL,

    roe REAL
);

---------------------------------------------------------
-- Financial Ratios
---------------------------------------------------------

CREATE TABLE financial_ratios (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    year INTEGER,

    net_profit_margin_pct REAL,

    operating_profit_margin_pct REAL,

    return_on_equity_pct REAL,

    debt_to_equity REAL,

    interest_coverage REAL,

    asset_turnover REAL,

    free_cash_flow_cr REAL,

    capex_cr REAL,

    earnings_per_share REAL,

    book_value_per_share REAL,

    dividend_payout_ratio_pct REAL,

    total_debt_cr REAL,

    cash_from_operations_cr REAL
);