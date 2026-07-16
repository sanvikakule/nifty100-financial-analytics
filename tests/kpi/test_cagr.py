import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from src.analytics.cagr import *


def test_normal_cagr():

    value, flag = calculate_cagr(
        100,
        200,
        5
    )

    assert flag == "OK"

    assert value is not None


def test_zero_base():

    value, flag = calculate_cagr(
        0,
        100,
        5
    )

    assert value is None

    assert flag == "ZERO_BASE"


def test_turnaround():

    value, flag = calculate_cagr(
        -100,
        100,
        5
    )

    assert flag == "TURNAROUND"


def test_decline_to_loss():

    value, flag = calculate_cagr(
        100,
        -100,
        5
    )

    assert flag == "DECLINE_TO_LOSS"


def test_both_negative():

    value, flag = calculate_cagr(
        -100,
        -200,
        5
    )

    assert flag == "BOTH_NEGATIVE"


def test_invalid_period():

    value, flag = calculate_cagr(
        100,
        200,
        0
    )

    assert flag == "INVALID_PERIOD"


def test_revenue_cagr():

    value, flag = revenue_cagr(
        100,
        300,
        5
    )

    assert flag == "OK"


def test_pat_cagr():

    value, flag = pat_cagr(
        200,
        500,
        5
    )

    assert flag == "OK"


def test_eps_cagr():

    value, flag = eps_cagr(
        10,
        25,
        5
    )

    assert flag == "OK"


def test_sufficient_data():

    assert has_sufficient_data(10, 5)


def test_insufficient_data():

    assert not has_sufficient_data(3, 5)