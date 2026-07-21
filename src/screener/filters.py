# ==========================================================
# FILTER ENGINE
# ==========================================================

import pandas as pd

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

    for filter_name, value in filters.items():

        # Skip disabled filters
        if value is None:
            continue

        # Skip filters that are not mapped
        if filter_name not in FILTER_MAPPING:
            print(f"Skipping unknown filter: {filter_name}")
            continue

        column, operator = FILTER_MAPPING[filter_name]

        # Skip if column does not exist
        if column not in filtered_df.columns:
            print(f"Column '{column}' not found. Skipping.")
            continue

        before = len(filtered_df)

        # Apply filter
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

    print("\n==============================")
    print("SCREENING SUMMARY")
    print("==============================")
    print(f"Original Records : {len(df)}")
    print(f"Filtered Records : {len(filtered_df)}")
    print(f"Rejected Records : {len(df) - len(filtered_df)}")

    # ------------------------------------------------------
    # Sort Results
    # ------------------------------------------------------
    filtered_df = filtered_df.sort_values(
        by="return_on_equity_pct",
        ascending=False,
        na_position="last"
    ).reset_index(drop=True)

    # ------------------------------------------------------
    # Placeholder Composite Quality Score
    # ------------------------------------------------------
    filtered_df["composite_quality_score"] = 0.0

    # ------------------------------------------------------
    # Screener Output Columns
    # ------------------------------------------------------
    output_columns = [
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

    # Keep only columns that actually exist
    output_columns = [
        col for col in output_columns
        if col in filtered_df.columns
    ]

    filtered_df = filtered_df[output_columns]

    return filtered_df