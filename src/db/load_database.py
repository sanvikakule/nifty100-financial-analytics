import sqlite3
from pathlib import Path
import pandas as pd

# ==========================================================
# PROJECT PATHS
# ==========================================================

ROOT = Path(__file__).resolve().parents[2]

DATABASE = ROOT / "data" / "db" / "nifty100.db"
PROCESSED = ROOT / "data" / "processed"

# ==========================================================
# CONNECT DATABASE
# ==========================================================

conn = sqlite3.connect(DATABASE)

print("\n========== Loading Data into SQLite ==========\n")

# ==========================================================
# FILES TO LOAD
# ==========================================================

tables = {
    "companies": "companies_clean.csv",
    "profitandloss": "profitandloss_clean.csv",
    "balancesheet": "balancesheet_clean.csv",
    "cashflow": "cashflow_clean.csv",
    "analysis": "analysis_clean.csv",
    "financial_ratios": "financial_ratios_clean.csv"
}

# ==========================================================
# LOAD EACH CSV
# ==========================================================

for table, file in tables.items():

    path = PROCESSED / file

    print(f"Loading {file}...")

    df = pd.read_csv(path)

    df.to_sql(
        table,
        conn,
        if_exists="append",
        index=False
    )

    print(f"✓ {table} loaded ({len(df)} rows)")

# ==========================================================
# CLOSE CONNECTION
# ==========================================================

conn.commit()
conn.close()

print("\n===================================")
print("All tables loaded successfully.")
print("Database Ready!")
print("===================================")