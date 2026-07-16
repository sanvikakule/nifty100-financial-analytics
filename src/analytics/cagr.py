"""
==========================================================
NIFTY100 Financial Analytics
Sprint 2 - Day 10
CAGR Engine
==========================================================
"""

from typing import Optional, Tuple


# ==========================================================
# CAGR Formula
# ==========================================================

def calculate_cagr(
    start_value: float,
    end_value: float,
    years: int
) -> Tuple[Optional[float], str]:

    if years <= 0:
        return None, "INVALID_PERIOD"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value > 0 and end_value > 0:

        cagr = ((end_value / start_value) ** (1 / years) - 1) * 100

        return round(cagr, 2), "OK"

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    return None, "UNKNOWN"


# ==========================================================
# Revenue CAGR
# ==========================================================

def revenue_cagr(start_sales, end_sales, years):
    return calculate_cagr(start_sales, end_sales, years)


# ==========================================================
# PAT CAGR
# ==========================================================

def pat_cagr(start_profit, end_profit, years):
    return calculate_cagr(start_profit, end_profit, years)


# ==========================================================
# EPS CAGR
# ==========================================================

def eps_cagr(start_eps, end_eps, years):
    return calculate_cagr(start_eps, end_eps, years)


# ==========================================================
# Sufficient Data Check
# ==========================================================

def has_sufficient_data(total_years: int, required_years: int):

    return total_years >= required_years