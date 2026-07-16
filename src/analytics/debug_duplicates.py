import sqlite3
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATABASE = ROOT / "data" / "db" / "nifty100.db"

conn = sqlite3.connect(DATABASE)

profit = pd.read_sql("SELECT * FROM profitandloss", conn)
balance = pd.read_sql("SELECT * FROM balancesheet", conn)

conn.close()

profit = profit.drop_duplicates(subset=["company_id", "year"], keep="first")
balance = balance.drop_duplicates(subset=["company_id", "year"], keep="first")

merged = profit.merge(
    balance,
    on=["company_id", "year"],
    how="inner",
    suffixes=("_pl", "_bs")
)

dup = merged[
    merged.duplicated(
        subset=["company_id", "year"],
        keep=False
    )
]

print(dup[
    [
        "company_id",
        "year"
    ]
].sort_values(
    ["company_id", "year"]
))

print("\nTotal duplicates:", len(dup))