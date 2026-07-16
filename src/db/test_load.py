import sqlite3
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

db = ROOT / "data" / "db" / "nifty100.db"
csv = ROOT / "data" / "processed" / "companies_clean.csv"

conn = sqlite3.connect(db)

df = pd.read_csv(csv)

print(df.head())
print(df.columns.tolist())

try:
    df.to_sql(
        "companies",
        conn,
        if_exists="append",
        index=False
    )
    print("SUCCESS")
except Exception as e:
    print(type(e))
    print(repr(e))
    import traceback
    traceback.print_exc()

conn.close()