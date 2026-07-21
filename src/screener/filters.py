# ==========================================================
# FILTER ENGINE
# ==========================================================

import pandas as pd
from src.screener.scoring import calculate_quality_score
from src.screener.ranking import calculate_rankings

# Mapping of YAML filter names to DataFrame columns
FILTER_MAPPING = {
    "roe_min": ("return_on_equity_pct", ">="),
    "debt_to_equity_max": ("debt_to_equity", "<="),
    "free_cash_flow_min": ("free_cash_flow_cr", ">="),
    "operating_margin_min": ("operating_profit_margin_pct", ">="),
    "pe_max": ("pe_ratio", "<="),
    "pb_max": ("pb_ratio", "<="),
    "dividend_yield_min": ("dividend_yield_pct", ">="),
    "interest_coverage_min": ("interest_coverage", ">="),
    "market_cap_min": ("market_cap_crore", ">="),
    "net_profit_min": ("net_profit", ">="),
    "asset_turnover_min": ("asset_turnover", ">="),
    "sales_min": ("sales", ">="),
}


def apply_filters(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Apply all enabled screener filters from screener_config.yaml.
    """

    filters = config.get("filters", {})
    filtered_df = df.copy()

    print("\nApplying Filters...\n")

    # ------------------------------------------------------
    # Apply Filters
    # ------------------------------------------------------
    for filter_name, value in filters.items():

        if value is None:
            continue

        if filter_name not in FILTER_MAPPING:
            print(f"Skipping unknown filter: {filter_name}")
            continue

        column, operator = FILTER_MAPPING[filter_name]

        if column not in filtered_df.columns:
            print(f"Column '{column}' not found. Skipping.")
            continue

        before = len(filtered_df)

        if operator == ">=":
            filtered_df = filtered_df[
                filtered_df[column] >= value
            ]

        elif operator == "<=":
            filtered_df = filtered_df[
                filtered_df[column] <= value
            ]

        after = len(filtered_df)

        print(
            f"{filter_name} ({column} {operator} {value}) : "
            f"{before} -> {after}"
        )

    # ------------------------------------------------------
    # Screening Summary
    # ------------------------------------------------------
    print("\n==============================")
    print("SCREENING SUMMARY")
    print("==============================")
    print(f"Original Records : {len(df)}")
    print(f"Filtered Records : {len(filtered_df)}")
    print(f"Rejected Records : {len(df) - len(filtered_df)}")

    # ------------------------------------------------------
    # Calculate Composite Quality Score
    # ------------------------------------------------------
    filtered_df = calculate_quality_score(filtered_df)
    filtered_df = calculate_rankings(filtered_df)

    # ------------------------------------------------------
    # Rank Companies
    # ------------------------------------------------------
    filtered_df = filtered_df.sort_values(
        by="composite_quality_score",
        ascending=False,
        na_position="last"
    ).reset_index(drop=True)

    # ------------------------------------------------------
    # Final Output Columns
    # ------------------------------------------------------
    output_columns = [
        "quality_rank",
    "quality_percentile",
    "company_id",
    "company_name",
    "year",
    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "operating_profit_margin_pct",
    "interest_coverage",
    "asset_turnover",
    "market_cap_crore",
    "pe_ratio",
    "pb_ratio",
    "dividend_yield_pct",
    "sales",
    "net_profit",
    "composite_quality_score",
    ]

    output_columns = [
        col for col in output_columns
        if col in filtered_df.columns
    ]

    return filtered_df[output_columns]