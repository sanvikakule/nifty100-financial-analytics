# ==========================================================
# PRESET SCREENERS
# ==========================================================

PRESET_SCREENERS = {

    "quality_compounder": {
        "roe_min": 20,
        "debt_to_equity_max": 0.5,
        "operating_margin_min": 15,
        "free_cash_flow_min": 0,
    },

    "value_pick": {
        "pe_max": 20,
        "pb_max": 3,
        "roe_min": 15,
    },

    "growth_accelerator": {
        "roe_min": 18,
        "operating_margin_min": 18,
    },

    "dividend_champion": {
        "dividend_yield_min": 2,
        "roe_min": 15,
    },

    "debt_free_bluechip": {
        "debt_to_equity_max": 0.2,
        "market_cap_min": 50000,
        "roe_min": 15,
    },

    "turnaround_watch": {
        "free_cash_flow_min": 0,
        "operating_margin_min": 5,
    }

}

from src.screener.filters import apply_filters


def run_preset(df, preset_name):
    """
    Apply one of the predefined screeners.
    """

    if preset_name not in PRESET_SCREENERS:
        raise ValueError(f"Unknown preset: {preset_name}")

    config = {
        "filters": PRESET_SCREENERS[preset_name]
    }

    return apply_filters(df, config)