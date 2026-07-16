"""
==========================================================
NIFTY100 Financial Analytics
Sprint 2 - Day 08
Profitability Ratio Engine
==========================================================
"""

from typing import Optional


# ==========================================================
# Net Profit Margin
# Formula:
# (Net Profit / Sales) * 100
# ==========================================================

def net_profit_margin(net_profit: float, sales: float) -> Optional[float]:

    if sales is None or sales == 0:
        return None

    return round((net_profit / sales) * 100, 2)


# ==========================================================
# Operating Profit Margin
# Formula:
# (Operating Profit / Sales) * 100
# ==========================================================

def operating_profit_margin(
    operating_profit: float,
    sales: float
) -> Optional[float]:

    if sales is None or sales == 0:
        return None

    return round((operating_profit / sales) * 100, 2)


# ==========================================================
# OPM Cross Check
# ==========================================================

def opm_matches_source(
    calculated_opm: float,
    source_opm: float,
    tolerance: float = 1.0
) -> bool:

    if calculated_opm is None or source_opm is None:
        return False

    return abs(calculated_opm - source_opm) <= tolerance


# ==========================================================
# Return on Equity (ROE)
# Formula:
# Net Profit / (Equity + Reserves)
# ==========================================================

def return_on_equity(
    net_profit: float,
    equity_capital: float,
    reserves: float
) -> Optional[float]:

    capital = equity_capital + reserves

    if capital <= 0:
        return None

    return round((net_profit / capital) * 100, 2)


# ==========================================================
# Return on Capital Employed
# Formula:
# EBIT / (Equity + Reserves + Borrowings)
# ==========================================================

def return_on_capital_employed(
    ebit: float,
    equity_capital: float,
    reserves: float,
    borrowings: float
) -> Optional[float]:

    capital = equity_capital + reserves + borrowings

    if capital <= 0:
        return None

    return round((ebit / capital) * 100, 2)


# ==========================================================
# Return on Assets
# Formula:
# Net Profit / Total Assets
# ==========================================================

def return_on_assets(
    net_profit: float,
    total_assets: float
) -> Optional[float]:

    if total_assets <= 0:
        return None

    return round((net_profit / total_assets) * 100, 2)