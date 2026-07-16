import pandas as pd
from pathlib import Path

PROCESSED = Path("data/processed")


# ==========================================================
# COMPANIES
# ==========================================================

def test_companies_has_id():
    df = pd.read_csv(PROCESSED / "companies_clean.csv")
    assert "id" in df.columns


def test_companies_has_company_name():
    df = pd.read_csv(PROCESSED / "companies_clean.csv")
    assert "company_name" in df.columns


def test_company_ids_unique():
    df = pd.read_csv(PROCESSED / "companies_clean.csv")
    assert df["id"].is_unique


def test_company_ids_not_null():
    df = pd.read_csv(PROCESSED / "companies_clean.csv")
    assert df["id"].isnull().sum() == 0


# ==========================================================
# PROFIT & LOSS
# ==========================================================

def test_profit_has_company_id():
    df = pd.read_csv(PROCESSED / "profitandloss_clean.csv")
    assert "company_id" in df.columns


def test_profit_has_year():
    df = pd.read_csv(PROCESSED / "profitandloss_clean.csv")
    assert "year" in df.columns


def test_sales_positive():
    df = pd.read_csv(PROCESSED / "profitandloss_clean.csv")
    assert (df["sales"] >= 0).all()


def test_net_profit_exists():
    df = pd.read_csv(PROCESSED / "profitandloss_clean.csv")
    assert "net_profit" in df.columns


# ==========================================================
# BALANCE SHEET
# ==========================================================

def test_balance_has_year():
    df = pd.read_csv(PROCESSED / "balancesheet_clean.csv")
    assert "year" in df.columns


def test_total_assets_exists():
    df = pd.read_csv(PROCESSED / "balancesheet_clean.csv")
    assert "total_assets" in df.columns


# ==========================================================
# CASH FLOW
# ==========================================================

def test_cashflow_has_company():
    df = pd.read_csv(PROCESSED / "cashflow_clean.csv")
    assert "company_id" in df.columns


def test_cashflow_has_net_cash():
    df = pd.read_csv(PROCESSED / "cashflow_clean.csv")
    assert "net_cash_flow" in df.columns


# ==========================================================
# MARKET CAP
# ==========================================================

def test_market_cap_positive():
    df = pd.read_csv(PROCESSED / "market_cap_clean.csv")
    assert (df["market_cap_crore"] >= 0).all()


def test_pe_ratio_exists():
    df = pd.read_csv(PROCESSED / "market_cap_clean.csv")
    assert "pe_ratio" in df.columns


# ==========================================================
# STOCK PRICES
# ==========================================================

def test_stock_price_columns():
    df = pd.read_csv(PROCESSED / "stock_prices_clean.csv")

    required = [
        "date",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
    ]

    for col in required:
        assert col in df.columns


def test_stock_prices_not_empty():
    df = pd.read_csv(PROCESSED / "stock_prices_clean.csv")
    assert len(df) > 0