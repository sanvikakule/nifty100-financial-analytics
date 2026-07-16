import pandas as pd
from pathlib import Path

processed = Path("data/processed")

files = [
    "documents_clean.csv",
    "peer_groups_clean.csv",
    "prosandcons_clean.csv",
    "sectors_clean.csv",
    "stock_prices_clean.csv"
]

for file in files:
    print("\n" + "="*70)
    print(file)

    df = pd.read_csv(processed / file)

    print("Shape :", df.shape)
    print("Columns:")
    print(df.columns.tolist())

    print("\nFirst 3 rows:")
    print(df.head(3))