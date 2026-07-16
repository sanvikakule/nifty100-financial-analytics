import sqlite3
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATABASE = ROOT / "data" / "db" / "nifty100.db"

conn = sqlite3.connect(DATABASE)

tables = [
    "profitandloss",
    "balancesheet",
    "cashflow"
]

for table in tables:

    print(f"\n========== {table.upper()} ==========")

    query = f"""
    SELECT company_id,
           year,
           COUNT(*) AS total
    FROM {table}
    GROUP BY company_id, year
    HAVING COUNT(*) > 1
    """

    df = pd.read_sql(query, conn)

    print(df)

conn.close()