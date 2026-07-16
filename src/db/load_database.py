import sqlite3
from pathlib import Path
import pandas as pd

# ==========================================================
# PROJECT PATHS
# ==========================================================

ROOT = Path(__file__).resolve().parents[2]

DATABASE = ROOT / "data" / "db" / "nifty100.db"
PROCESSED = ROOT / "data" / "processed"
OUTPUT = ROOT / "output"

OUTPUT.mkdir(parents=True, exist_ok=True)

# ==========================================================
# TABLES IN LOAD ORDER
# ==========================================================

TABLES = [
    ("companies", "companies_clean.csv"),
    ("sectors", "sectors_clean.csv"),
    ("prosandcons", "prosandcons_clean.csv"),
    ("peer_groups", "peer_groups_clean.csv"),
    ("analysis", "analysis_clean.csv"),
    ("profitandloss", "profitandloss_clean.csv"),
    ("balancesheet", "balancesheet_clean.csv"),
    ("cashflow", "cashflow_clean.csv"),
    ("financial_ratios", "financial_ratios_clean.csv"),
    ("documents", "documents_clean.csv"),
    ("stock_prices", "stock_prices_clean.csv"),
    ("market_cap", "market_cap_clean.csv"),
]

# ==========================================================
# LOAD DATABASE
# ==========================================================

def load_database():

    print("\n========== Loading Database ==========\n")

    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")

    audit = []

    for table, filename in TABLES:

        filepath = PROCESSED / filename

        print(f"Loading {table}...")

        if not filepath.exists():

            print(f"Missing : {filename}")

            audit.append({
                "table": table,
                "rows_loaded": 0,
                "status": "Missing"
            })

            continue

        df = pd.read_csv(filepath)

        try:

            # Remove existing data
            conn.execute(f"DELETE FROM {table}")
            conn.commit()

            # Load fresh data
            df.to_sql(
                table,
                conn,
                if_exists="append",
                index=False,
                 chunksize=500
            )

            print(f"✓ Loaded {len(df)} rows")

            audit.append({
                "table": table,
                "rows_loaded": len(df),
                "status": "Success"
            })

        except Exception as e:

            print(f"❌ {table}")

            print(e)

            audit.append({
                "table": table,
                "rows_loaded": 0,
                "status": "Failed"
            })

    audit_df = pd.DataFrame(audit)

    audit_df.to_csv(
        OUTPUT / "load_audit.csv",
        index=False
    )

    conn.close()

    print("\n=========================================")
    print("Database Loading Completed")
    print("Load Audit Saved")
    print("=========================================")


if __name__ == "__main__":

    load_database()