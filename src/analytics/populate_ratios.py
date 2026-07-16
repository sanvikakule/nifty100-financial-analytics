import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import sqlite3
import pandas as pd

from src.analytics.ratios import *
from src.analytics.leverage import *
from src.analytics.cagr import *
from src.analytics.cashflow_kpis import *

DATABASE = ROOT / "data" / "db" / "nifty100.db"

# ==========================================================
# CONNECT
# ==========================================================

conn = sqlite3.connect(DATABASE)

print("\n========== POPULATING FINANCIAL RATIOS ==========\n")

# ==========================================================
# LOAD TABLES
# ==========================================================

profit = pd.read_sql(
    "SELECT * FROM profitandloss",
    conn
)

balance = pd.read_sql(
    "SELECT * FROM balancesheet",
    conn
)

cash = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

# ==========================================================
# MERGE TABLES
# ==========================================================

# Merge Profit & Loss + Balance Sheet
df1 = profit.merge(
    balance,
    on=["company_id", "year"],
    how="inner",
    suffixes=("_pl", "_bs")
)

print("\nProfit + Balance")
print(df1.shape)
print(
    "Duplicates:",
    df1.duplicated(subset=["company_id", "year"]).sum()
)

# Merge with Cash Flow
df2 = df1.merge(
    cash,
    on=["company_id", "year"],
    how="inner"
)

print("\nFinal Merge")
print(df2.shape)
print(
    "Duplicates:",
    df2.duplicated(subset=["company_id", "year"]).sum()
)

df = df2

# ==========================================================
# REMOVE DUPLICATES
# ==========================================================

profit = profit.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)

balance = balance.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)

cash = cash.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)

print("Duplicates removed.")
print("Profit & Loss :", len(profit))
print("Balance Sheet :", len(balance))
print("Cash Flow     :", len(cash))

print(df.shape)

print("\nCalculating Net Profit Margin...")

df["net_profit_margin_pct"] = df.apply(
    lambda row: net_profit_margin(
        row["net_profit"],
        row["sales"]
    ),
    axis=1
)

print("Calculating Operating Profit Margin...")

df["operating_profit_margin_pct"] = df.apply(
    lambda row: operating_profit_margin(
        row["operating_profit"],
        row["sales"]
    ),
    axis=1
)

print("Calculating Return on Equity...")

df["return_on_equity_pct"] = df.apply(
    lambda row: return_on_equity(
        row["net_profit"],
        row["equity_capital"],
        row["reserves"]
    ),
    axis=1
)

print("Calculating ROCE...")

df["ebit"] = (
    df["operating_profit"] +
    df["other_income"]
)

df["roce"] = df.apply(
    lambda row: return_on_capital_employed(
        row["ebit"],
        row["equity_capital"],
        row["reserves"],
        row["borrowings"]
    ),
    axis=1
)


print("Calculating Return on Assets...")

df["roa"] = df.apply(
    lambda row: return_on_assets(
        row["net_profit"],
        row["total_assets"]
    ),
    axis=1
)

print("Calculating Debt-to-Equity...")

df["debt_to_equity"] = df.apply(
    lambda row: debt_to_equity(
        row["borrowings"],
        row["equity_capital"],
        row["reserves"]
    ),
    axis=1
)

print("Calculating Interest Coverage...")

df["interest_coverage"] = df.apply(
    lambda row: interest_coverage_ratio(
        row["operating_profit"],
        row["other_income"],
        row["interest"]
    ),
    axis=1
)

print("Calculating Asset Turnover...")

df["asset_turnover"] = df.apply(
    lambda row: asset_turnover(
        row["sales"],
        row["total_assets"]
    ),
    axis=1
)

print("Calculating Net Debt...")

df["net_debt"] = df.apply(
    lambda row: net_debt(
        row["borrowings"],
        row["investments"]
    ),
    axis=1
)

print("Calculating Free Cash Flow...")

df["free_cash_flow"] = df.apply(
    lambda row: free_cash_flow(
        row["operating_activity"],
        row["investing_activity"]
    ),
    axis=1
)

print("Calculating CFO Quality...")

df["cfo_quality"] = df.apply(
    lambda row: cfo_quality_score(
        row["operating_activity"],
        row["net_profit"]
    ),
    axis=1
)

print("Calculating CapEx Intensity...")

df["capex_intensity"] = df.apply(
    lambda row: capex_intensity(
        row["investing_activity"],
        row["sales"]
    ),
    axis=1
)

print("Calculating FCF Conversion...")

df["fcf_conversion"] = df.apply(
    lambda row: fcf_conversion(
        row["free_cash_flow"],
        row["operating_profit"]
    ),
    axis=1
)

print("Calculating Capital Allocation Pattern...")

df["capital_allocation"] = df.apply(
    lambda row: capital_allocation_pattern(
        row["operating_activity"],
        row["investing_activity"],
        row["financing_activity"]
    ),
    axis=1
)

print("\n========== LEVERAGE & CASH FLOW KPIs ==========\n")

print(
    df[
        [
            "company_id",
            "year",
            "debt_to_equity",
            "interest_coverage",
            "asset_turnover",
            "net_debt",
            "free_cash_flow",
            "cfo_quality",
            "capex_intensity",
            "fcf_conversion",
            "capital_allocation"
        ]
    ].head(10)
)

print(
    "\nDuplicate Company-Year:",
    df.duplicated(
        subset=["company_id", "year"]
    ).sum()
)