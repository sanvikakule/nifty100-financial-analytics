import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"

companies = set(
    pd.read_csv(PROCESSED / "companies_clean.csv")["id"]
    .astype(str)
    .str.strip()
)

tables = [
    "prosandcons",
    "analysis",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios",
    "documents",
]

for table in tables:

    df = pd.read_csv(PROCESSED / f"{table}_clean.csv")

    ids = (
        df["company_id"]
        .astype(str)
        .str.strip()
    )

    missing = sorted(set(ids) - companies)

    print("\n" + "=" * 60)
    print(table)

    if missing:
        print(f"Missing company_ids ({len(missing)}):")
        print(missing)
    else:
        print("No missing company_ids")