import sqlite3
from pathlib import Path

# ==========================================================
# PROJECT PATHS
# ==========================================================

ROOT = Path(__file__).resolve().parents[2]

DATABASE = ROOT / "data" / "db" / "nifty100.db"

# ==========================================================
# CONNECT DATABASE
# ==========================================================

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# ==========================================================
# TABLES TO VERIFY
# ==========================================================

tables = [
    "companies",
    "sectors",
    "prosandcons",
    "peer_groups",
    "analysis",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios",
    "documents",
    "stock_prices",
    "market_cap",
]

print("\n" + "=" * 60)
print("NIFTY100 DATABASE VERIFICATION")
print("=" * 60)

total_rows = 0

for table in tables:

    try:

        cursor.execute(f"SELECT COUNT(*) FROM {table}")

        count = cursor.fetchone()[0]

        total_rows += count

        print(f"✓ {table:<20} {count:>8} rows")

    except Exception as e:

        print(f"✗ {table:<20} ERROR")

        print(e)

print("=" * 60)
print(f"Total Tables : {len(tables)}")
print(f"Total Rows   : {total_rows:,}")

# ==========================================================
# LIST ALL TABLES
# ==========================================================

print("\nTables Present:")

cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
)

for table in cursor.fetchall():

    print(f"• {table[0]}")

conn.close()

print("\nDatabase verification completed successfully.")
print("=" * 60)