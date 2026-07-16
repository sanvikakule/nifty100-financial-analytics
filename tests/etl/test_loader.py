from pathlib import Path
import pandas as pd

PROCESSED = Path("data/processed")


def test_processed_folder_exists():
    assert PROCESSED.exists()


def test_companies_csv_exists():
    assert (PROCESSED / "companies_clean.csv").exists()


def test_profitandloss_csv_exists():
    assert (PROCESSED / "profitandloss_clean.csv").exists()


def test_balancesheet_csv_exists():
    assert (PROCESSED / "balancesheet_clean.csv").exists()


def test_cashflow_csv_exists():
    assert (PROCESSED / "cashflow_clean.csv").exists()


def test_analysis_csv_exists():
    assert (PROCESSED / "analysis_clean.csv").exists()


def test_financial_ratios_csv_exists():
    assert (PROCESSED / "financial_ratios_clean.csv").exists()


def test_documents_csv_exists():
    assert (PROCESSED / "documents_clean.csv").exists()


def test_peer_groups_csv_exists():
    assert (PROCESSED / "peer_groups_clean.csv").exists()


def test_prosandcons_csv_exists():
    assert (PROCESSED / "prosandcons_clean.csv").exists()


def test_sectors_csv_exists():
    assert (PROCESSED / "sectors_clean.csv").exists()


def test_stock_prices_csv_exists():
    assert (PROCESSED / "stock_prices_clean.csv").exists()


def test_market_cap_csv_exists():
    assert (PROCESSED / "market_cap_clean.csv").exists()


def test_companies_not_empty():
    df = pd.read_csv(PROCESSED / "companies_clean.csv")
    assert len(df) > 0


def test_profit_not_empty():
    df = pd.read_csv(PROCESSED / "profitandloss_clean.csv")
    assert len(df) > 0