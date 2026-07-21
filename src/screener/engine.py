# ==========================================================
# IMPORTS
# ==========================================================

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import pandas as pd
import yaml

from src.screener.data_loader import load_screener_data
from src.screener.filters import apply_filters

# ==========================================================
# PATHS
# ==========================================================

CONFIG = ROOT / "config" / "screener_config.yaml"

# ==========================================================
# START ENGINE
# ==========================================================

print("\n========== NIFTY 100 SCREENER ENGINE ==========\n")

# ==========================================================
# LOAD MASTER DATA
# ==========================================================

print("Loading screener data...\n")

df = load_screener_data()

print("✓ Screener data loaded successfully")

print(f"Rows    : {len(df)}")
print(f"Columns : {len(df.columns)}")

print("\nColumns:")
print(df.columns.tolist())

print("\nPreview:")
print(df.head())

# ==========================================================
# LOAD YAML CONFIGURATION
# ==========================================================

print("\nLoading screener configuration...\n")

with open(CONFIG, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

print("✓ Configuration loaded successfully")

print("\nCurrent Configuration:")
print(config)

# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered_df = apply_filters(df, config)

# ==========================================================
# RESULTS
# ==========================================================

print("\n========== FILTER RESULTS ==========\n")

print(f"Original Records : {len(df)}")
print(f"Filtered Records : {len(filtered_df)}")

print("\nFiltered Preview:")
print(filtered_df.head())

# ==========================================================
# ENGINE COMPLETE
# ==========================================================

print("\n========== SCREENER ENGINE READY ==========")