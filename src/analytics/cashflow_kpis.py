"""
==========================================================
NIFTY100 Financial Analytics
Sprint 2 - Day 11
Cash Flow KPI Engine
==========================================================
"""

from typing import Optional


# ==========================================================
# Free Cash Flow
# ==========================================================

def free_cash_flow(
    operating_activity: float,
    investing_activity: float
) -> float:

    return round(
        operating_activity + investing_activity,
        2
    )


# ==========================================================
# CFO Quality
# ==========================================================

def cfo_quality_score(
    operating_activity: float,
    net_profit: float
):

    if net_profit == 0:
        return None

    score = operating_activity / net_profit

    if score > 1:
        return "High Quality"

    if score >= 0.5:
        return "Moderate"

    return "Accrual Risk"


# ==========================================================
# CapEx Intensity
# ==========================================================

def capex_intensity(
    investing_activity: float,
    sales: float
):

    if sales == 0:
        return None

    pct = abs(investing_activity) / sales * 100

    if pct < 3:
        return "Asset Light"

    if pct <= 8:
        return "Moderate"

    return "Capital Intensive"


# ==========================================================
# FCF Conversion
# ==========================================================

def fcf_conversion(
    free_cash_flow_value: float,
    operating_profit: float
):

    if operating_profit == 0:
        return None

    return round(
        free_cash_flow_value /
        operating_profit * 100,
        2
    )


# ==========================================================
# Capital Allocation Pattern
# ==========================================================

def capital_allocation_pattern(
    cfo: float,
    cfi: float,
    cff: float
):

    signs = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-"
    )

    patterns = {

        ("+","-","-"): "Reinvestor",

        ("+","+","-"): "Liquidating Assets",

        ("-","+","+"): "Distress Signal",

        ("-","-","+"): "Growth Funded by Debt",

        ("+","+","+"): "Cash Accumulator",

        ("-","-","-"): "Pre-Revenue",

        ("+","-","+"): "Mixed"

    }

    return patterns.get(signs, "Unknown")