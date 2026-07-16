import sqlite3
from pathlib import Path

DATABASE = Path("data/db/nifty100.db")


def test_database_exists():
    assert DATABASE.exists()


def test_database_connection():
    conn = sqlite3.connect(DATABASE)
    conn.close()


def test_companies_table_exists():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name='companies'
    """)

    assert cursor.fetchone() is not None
    conn.close()


def test_total_tables():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM sqlite_master
        WHERE type='table'
    """)

    total = cursor.fetchone()[0]

    assert total == 12

    conn.close()


def test_companies_row_count():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM companies")

    assert cursor.fetchone()[0] == 92

    conn.close()


def test_stock_price_row_count():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM stock_prices")

    assert cursor.fetchone()[0] == 5520

    conn.close()


def test_market_cap_row_count():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM market_cap")

    assert cursor.fetchone()[0] == 552

    conn.close()


def test_profit_loss_not_empty():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM profitandloss")

    assert cursor.fetchone()[0] > 0

    conn.close()