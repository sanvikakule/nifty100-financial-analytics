"""
==========================================================
NIFTY100 Financial Analytics
Sprint 2 - Day 09
Leverage & Efficiency Ratio Engine
==========================================================
"""

from typing import Optional


# ==========================================================
# Debt-to-Equity Ratio
# ==========================================================

def debt_to_equity(
    borrowings: float,
    equity_capital: float,
    reserves: float
) -> Optional[float]:

    equity = equity_capital + reserves

    if borrowings == 0:
        return 0.0

    if equity <= 0:
        return None

    return round(borrowings / equity, 2)


# ==========================================================
# High Leverage Flag
# ==========================================================

def high_leverage_flag(
    debt_equity: Optional[float],
    sector: str
) -> bool:

    if debt_equity is None:
        return False

    if sector == "Financials":
        return False

    return debt_equity > 5


# ==========================================================
# Interest Coverage Ratio
# ==========================================================

def interest_coverage_ratio(
    operating_profit: float,
    other_income: float,
    interest: float
) -> Optional[float]:

    if interest == 0:
        return None

    return round(
        (operating_profit + other_income) / interest,
        2
    )


# ==========================================================
# Interest Coverage Label
# ==========================================================

def interest_coverage_label(
    interest: float
) -> str:

    if interest == 0:
        return "Debt Free"

    return ""


# ==========================================================
# Interest Coverage Warning
# ==========================================================

def interest_coverage_warning(
    icr: Optional[float]
) -> bool:

    if icr is None:
        return False

    return icr < 1.5


# ==========================================================
# Net Debt
# ==========================================================

def net_debt(
    borrowings: float,
    investments: float
) -> float:

    return round(
        borrowings - investments,
        2
    )


# ==========================================================
# Asset Turnover
# ==========================================================

def asset_turnover(
    sales: float,
    total_assets: float
) -> Optional[float]:

    if total_assets <= 0:
        return None

    return round(
        sales / total_assets,
        2
    )