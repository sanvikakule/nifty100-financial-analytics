import sqlite3
import pandas as pd

conn = sqlite3.connect("data/db/nifty100.db")

tables = [
    "financial_ratios",
    "profitandloss",
    "market_cap"
]

for table in tables:
    print("\n" + "=" * 70)
    print(table.upper())
    print("=" * 70)

    query = f"""
    SELECT
        company_id,
        year,
        COUNT(*) AS duplicate_count
    FROM {table}
    GROUP BY company_id, year
    HAVING COUNT(*) > 1
    ORDER BY duplicate_count DESC;
    """

    duplicates = pd.read_sql(query, conn)

    print(f"Duplicate Keys: {len(duplicates)}")

    if not duplicates.empty:
        print(duplicates.head(20))

conn.close()