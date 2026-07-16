import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from src.analytics.leverage import *


def test_debt_to_equity():

    assert debt_to_equity(500, 500, 500) == 0.50


def test_debt_free():

    assert debt_to_equity(0, 500, 500) == 0.0


def test_negative_equity():

    assert debt_to_equity(500, -200, -100) is None


def test_high_leverage():

    assert high_leverage_flag(6.2, "Industrials")


def test_financial_sector():

    assert not high_leverage_flag(8.0, "Financials")


def test_interest_coverage():

    assert interest_coverage_ratio(
        500,
        100,
        200
    ) == 3.00


def test_interest_zero():

    assert interest_coverage_ratio(
        500,
        100,
        0
    ) is None


def test_interest_label():

    assert interest_coverage_label(0) == "Debt Free"


def test_net_debt():

    assert net_debt(
        1000,
        200
    ) == 800.00


def test_asset_turnover():

    assert asset_turnover(
        1000,
        500
    ) == 2.00


def test_asset_turnover_zero():

    assert asset_turnover(
        1000,
        0
    ) is None