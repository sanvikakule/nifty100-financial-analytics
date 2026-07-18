import sqlite3
import pandas as pd

conn = sqlite3.connect("data/db/nifty100.db")

tables = [
    "financial_ratios",
    "profitandloss",
    "market_cap",
    "companies",
    "peer_groups"
]

for table in tables:
    print("\n" + "=" * 70)
    print(table.upper())
    print("=" * 70)

    df = pd.read_sql(f"SELECT * FROM {table} LIMIT 5", conn)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nSample Data:")
    print(df)

conn.close()