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

print("\nDuplicates removed.")
print("Profit & Loss :", len(profit))
print("Balance Sheet :", len(balance))
print("Cash Flow     :", len(cash))

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

print("Calculating Book Value Per Share...")

df["book_value_per_share"] = (
    (df["equity_capital"] + df["reserves"])
    / df["equity_capital"]
).round(2)

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

print("\nAvailable Columns:\n")
print(df.columns.tolist())

print("\n========== LEVERAGE & CASH FLOW KPIs ==========\n")
# ==========================================================
# PREPARE FINAL RATIO DATA
# ==========================================================

print("\n========== FINAL RATIO DATA ==========\n")

# Book Value Per Share
print("Calculating Book Value Per Share...")

df["book_value_per_share"] = (
    (df["equity_capital"] + df["reserves"])
    / df["equity_capital"]
).round(2)

# CapEx (using Investing Activity)
print("Calculating CapEx...")

df["capex_cr"] = df["investing_activity"].abs()

# Final dataframe for database insertion
ratio_df = df[
    [
        "company_id",
        "year",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "return_on_equity_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow",
        "capex_cr",
        "eps",
        "book_value_per_share",
        "dividend_payout",
        "borrowings",
        "operating_activity",
    ]
].copy()

# Rename columns to match SQLite table
ratio_df.rename(
    columns={
        "free_cash_flow": "free_cash_flow_cr",
        "eps": "earnings_per_share",
        "dividend_payout": "dividend_payout_ratio_pct",
        "borrowings": "total_debt_cr",
        "operating_activity": "cash_from_operations_cr",
    },
    inplace=True,
)

# Display summary
print("\nShape:")
print(ratio_df.shape)

print("\nColumns:")
print(ratio_df.columns.tolist())

print("\nPreview:")
print(ratio_df.head(10))

print(
    "\nDuplicate Company-Year:",
    ratio_df.duplicated(
        subset=["company_id", "year"]
    ).sum()
)

# ==========================================================
# INSERT INTO DATABASE
# ==========================================================

ratio_df.to_sql(
    "financial_ratios",
    conn,
    if_exists="append",
    index=False,
)

conn.commit()

print("\n✅ Successfully inserted", len(ratio_df), "records into financial_ratios.")

# ==========================================================
# VERIFY INSERT
# ==========================================================

count = pd.read_sql(
    "SELECT COUNT(*) AS total FROM financial_ratios",
    conn
)

print("\nDatabase Verification:")
print(count)

conn.close()

# ==========================================================
# EXPORT CAPITAL ALLOCATION REPORT
# ==========================================================

from pathlib import Path

OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

capital_df = df[
    [
        "company_id",
        "year",
        "operating_activity",
        "investing_activity",
        "financing_activity",
        "capital_allocation",
    ]
].copy()

capital_file = OUTPUT_DIR / "capital_allocation.csv"

capital_df.to_csv(
    capital_file,
    index=False
)

print(f"\nCapital Allocation report saved to:\n{capital_file}")

# ==========================================================
# GENERATE EDGE CASE LOG
# ==========================================================

REPORT_DIR = ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)

log_file = REPORT_DIR / "ratio_edge_cases.log"

with open(log_file, "w", encoding="utf-8") as f:

    f.write("========== RATIO EDGE CASE REPORT ==========\n\n")

    # Missing values
    f.write("Missing Values\n")
    f.write("------------------------------\n")
    f.write(df.isnull().sum().to_string())
    f.write("\n\n")

    # Negative equity
    negative_equity = df[df["equity_capital"] + df["reserves"] < 0]

    f.write(f"Negative Equity Companies : {len(negative_equity)}\n")

    # Zero Sales
    zero_sales = df[df["sales"] == 0]
    f.write(f"Zero Sales Records : {len(zero_sales)}\n")

    # Zero Operating Profit
    zero_op = df[df["operating_profit"] == 0]
    f.write(f"Zero Operating Profit Records : {len(zero_op)}\n")

    # Zero Interest
    zero_interest = df[df["interest"] == 0]
    f.write(f"Zero Interest Records : {len(zero_interest)}\n")

    # Missing EPS
    missing_eps = df[df["eps"].isna()]
    f.write(f"Missing EPS Records : {len(missing_eps)}\n")

    # Duplicate Company-Year
    duplicates = df.duplicated(subset=["company_id", "year"]).sum()
    f.write(f"Duplicate Company-Year : {duplicates}\n")

print(f"\nEdge case report saved to:\n{log_file}")

# ==========================================================
# GENERATE ANALYTICS SUMMARY REPORT
# ==========================================================

summary_file = REPORT_DIR / "analytics_summary.txt"

with open(summary_file, "w", encoding="utf-8") as f:

    f.write("========== NIFTY 100 ANALYTICS SUMMARY ==========\n\n")

    f.write(f"Total Records Processed        : {len(df)}\n")
    f.write(f"Unique Companies              : {df['company_id'].nunique()}\n")
    f.write(f"Years Covered                 : {int(df['year'].min())} - {int(df['year'].max())}\n\n")

    f.write("========== KPI SUMMARY ==========\n\n")

    f.write(f"Net Profit Margin             : {df['net_profit_margin_pct'].notna().sum()}\n")
    f.write(f"Operating Profit Margin       : {df['operating_profit_margin_pct'].notna().sum()}\n")
    f.write(f"Return on Equity              : {df['return_on_equity_pct'].notna().sum()}\n")
    f.write(f"ROCE                          : {df['roce'].notna().sum()}\n")
    f.write(f"ROA                           : {df['roa'].notna().sum()}\n")
    f.write(f"Debt to Equity                : {df['debt_to_equity'].notna().sum()}\n")
    f.write(f"Interest Coverage             : {df['interest_coverage'].notna().sum()}\n")
    f.write(f"Asset Turnover                : {df['asset_turnover'].notna().sum()}\n")
    f.write(f"Free Cash Flow                : {df['free_cash_flow'].notna().sum()}\n")
    f.write(f"CFO Quality                   : {df['cfo_quality'].notna().sum()}\n")
    f.write(f"Capital Allocation Pattern    : {df['capital_allocation'].notna().sum()}\n\n")

    f.write("========== DATA QUALITY ==========\n\n")

    f.write(f"Duplicate Company-Year        : {df.duplicated(subset=['company_id','year']).sum()}\n")
    f.write(f"Missing Values                : {df.isnull().sum().sum()}\n")
    f.write(f"Negative Equity Records       : {len(df[df['equity_capital'] + df['reserves'] < 0])}\n")
    f.write(f"Zero Sales Records            : {len(df[df['sales'] == 0])}\n")
    f.write(f"Zero Interest Records         : {len(df[df['interest'] == 0])}\n")

print(f"\nAnalytics summary saved to:\n{summary_file}")