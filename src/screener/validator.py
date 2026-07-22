# ==========================================================
# SCREENER VALIDATOR
# ==========================================================

import pandas as pd


REQUIRED_COLUMNS = [
    "company_id",
    "company_name",
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "free_cash_flow_cr",
    "interest_coverage",
    "asset_turnover",
    "market_cap_crore",
]


def validate_dataframe(df: pd.DataFrame):
    """
    Validate that the screener DataFrame contains
    all required columns and is not empty.
    """

    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    missing = [
        col
        for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    print("✓ Data validation passed.")