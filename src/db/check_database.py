import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATABASE = ROOT / "data" / "db" / "nifty100.db"

conn = sqlite3.connect(DATABASE)

cursor = conn.cursor()

tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "financial_ratios"
]

print("\n========== DATABASE SUMMARY ==========\n")

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"{table:<20}: {count} rows")

conn.close()