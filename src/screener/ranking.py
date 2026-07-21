# ==========================================================
# PEER RANKING ENGINE
# ==========================================================

import pandas as pd


def calculate_rankings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate company rank and percentile based on
    composite quality score.
    """

    ranked = df.copy()

    # Highest score gets Rank 1
    ranked["quality_rank"] = (
        ranked["composite_quality_score"]
        .rank(
            method="dense",
            ascending=False
        )
        .astype(int)
    )

    total = len(ranked)

    # Percentile
    ranked["quality_percentile"] = (
        (total - ranked["quality_rank"] + 1)
        / total
        * 100
    ).round(2)

    return ranked

def get_company_rank(df: pd.DataFrame, company_id: str):
    """
    Return ranking details for a specific company.
    """

    result = df[df["company_id"] == company_id.upper()]

    if result.empty:
        return None
    
    return result.iloc[0]

def top_companies(df: pd.DataFrame, n: int = 10):
    """
    Return Top N ranked companies.
    """
    return df.sort_values(
        "quality_rank"
    ).head(n)


def bottom_companies(df: pd.DataFrame, n: int = 10):
    """
    Return Bottom N ranked companies.
    """
    return df.sort_values(
        "quality_rank",
        ascending=False
    ).head(n)
