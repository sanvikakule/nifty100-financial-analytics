# ==========================================================
# COMPOSITE QUALITY SCORING ENGINE
# ==========================================================

import pandas as pd


# Weight assigned to each metric
WEIGHTS = {
    "return_on_equity_pct": 25,
    "debt_to_equity": 20,
    "operating_profit_margin_pct": 20,
    "free_cash_flow_cr": 15,
    "interest_coverage": 10,
    "asset_turnover": 10,
}


def normalize(series: pd.Series, reverse: bool = False) -> pd.Series:
    """
    Normalize values to a 0–1 range.
    """

    series = series.fillna(series.median())

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(1.0, index=series.index)

    normalized = (series - minimum) / (maximum - minimum)

    if reverse:
        normalized = 1 - normalized

    return normalized


def calculate_quality_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate weighted composite quality score.
    """

    scored = df.copy()

    scored["composite_quality_score"] = 0.0

    for column, weight in WEIGHTS.items():

        if column not in scored.columns:
            continue

        reverse = column == "debt_to_equity"

        score = normalize(
            scored[column],
            reverse=reverse
        )

        scored["composite_quality_score"] += score * weight

    scored["composite_quality_score"] = (
        scored["composite_quality_score"]
        .round(2)
    )

    return scored