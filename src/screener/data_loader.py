import sqlite3
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATABASE = ROOT / "data" / "db" / "nifty100.db"


def load_screener_data():
    """
    Load and merge all tables required for the financial screener.
    """

    conn = sqlite3.connect(DATABASE)

    # -----------------------------
    # Financial Ratios
    # -----------------------------
    ratios = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    # -----------------------------
    # Profit & Loss
    # -----------------------------
    pnl = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            sales,
            operating_profit,
            net_profit,
            eps,
            dividend_payout
        FROM profitandloss
        """,
        conn
    )

    # Remove duplicate company-year records
    pnl = pnl.drop_duplicates(
        subset=["company_id", "year"],
        keep="first"
    )

    # -----------------------------
    # Market Cap
    # -----------------------------
    market = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            market_cap_crore,
            pe_ratio,
            pb_ratio,
            dividend_yield_pct
        FROM market_cap
        """,
        conn
    )

    # -----------------------------
    # Company Details
    # -----------------------------
    companies = pd.read_sql(
        """
        SELECT
            id AS company_id,
            company_name,
            roce_percentage,
            roe_percentage
        FROM companies
        """,
        conn
    )

    conn.close()

    # =====================================================
    # Merge All Tables
    # =====================================================

    master_df = (
        ratios
        .merge(
            pnl,
            on=["company_id", "year"],
            how="left"
        )
        .merge(
            market,
            on=["company_id", "year"],
            how="left"
        )
        .merge(
            companies,
            on="company_id",
            how="left"
        )
    )

    # =====================================================
    # Keep Latest Financial Year for Each Company
    # =====================================================

    master_df["year"] = pd.to_numeric(
        master_df["year"],
        errors="coerce"
    )

    master_df = (
        master_df
        .sort_values("year")
        .groupby("company_id", as_index=False)
        .last()
    )

    master_df = (
        master_df
        .sort_values("company_id")
        .reset_index(drop=True)
    )

    return master_df