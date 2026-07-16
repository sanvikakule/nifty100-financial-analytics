import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from src.analytics.ratios import *


def test_net_profit_margin():

    assert net_profit_margin(200, 1000) == 20.00


def test_net_profit_margin_zero_sales():

    assert net_profit_margin(200, 0) is None


def test_operating_profit_margin():

    assert operating_profit_margin(300, 1000) == 30.00


def test_opm_cross_check():

    assert opm_matches_source(30.2, 30.0)


def test_opm_cross_check_fail():

    assert not opm_matches_source(35, 30)


def test_roe():

    assert return_on_equity(200, 500, 500) == 20.00


def test_negative_equity():

    assert return_on_equity(200, -100, -50) is None


def test_roce():

    assert return_on_capital_employed(
        300,
        500,
        500,
        1000
    ) == 15.00


def test_roa():

    assert return_on_assets(200, 1000) == 20.00


def test_roa_zero_assets():

    assert return_on_assets(200, 0) is None