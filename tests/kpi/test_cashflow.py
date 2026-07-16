import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from src.analytics.cashflow_kpis import *


def test_free_cash_flow():

    assert free_cash_flow(1000, -300) == 700


def test_cfo_quality():

    assert cfo_quality_score(1200, 1000) == "High Quality"


def test_cfo_moderate():

    assert cfo_quality_score(700, 1000) == "Moderate"


def test_cfo_risk():

    assert cfo_quality_score(200, 1000) == "Accrual Risk"


def test_capex_asset_light():

    assert capex_intensity(-20, 1000) == "Asset Light"


def test_capex_moderate():

    assert capex_intensity(-50, 1000) == "Moderate"


def test_capex_high():

    assert capex_intensity(-120, 1000) == "Capital Intensive"


def test_fcf_conversion():

    assert fcf_conversion(700, 1000) == 70


def test_pattern():

    assert capital_allocation_pattern(
        100,
        -50,
        -30
    ) == "Reinvestor"