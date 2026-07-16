from pathlib import Path
import pandas as pd
import logging
from pathlib import Path
import pandas as pd
import re

ROOT = Path(__file__).resolve().parents[2]
PROCESSED_FOLDER = ROOT / "data" / "processed"
OUTPUT_FOLDER = ROOT / "output"
LOG_FOLDER = ROOT / "logs"

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
LOG_FOLDER.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_FOLDER / "validator.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

validation_failures = []

def load_data():

    files = {

        "companies": "companies_clean.csv",

        "profitandloss": "profitandloss_clean.csv",

        "balancesheet": "balancesheet_clean.csv",

        "cashflow": "cashflow_clean.csv",

        "analysis": "analysis_clean.csv",

        "financial_ratios": "financial_ratios_clean.csv",

        "documents": "documents_clean.csv",

        "stock_prices": "stock_prices_clean.csv",

        "market_cap": "market_cap_clean.csv",

        "peer_groups": "peer_groups_clean.csv",

        "prosandcons": "prosandcons_clean.csv",

        "sectors": "sectors_clean.csv"

    }

    data = {}

    for table, file in files.items():

        data[table] = pd.read_csv(PROCESSED_FOLDER / file)

    return data

def add_failure(rule,file_name,severity,message):
    validation_failures.append({"Rule":rule,"File":file_name,"Severity":severity,"Message":message})

def print_dataset_summary(data):
    print("\n========== DATASETS LOADED ==========\n")
    for n,df in data.items():
        print(f"{n:<20} Rows : {len(df):<6} Columns : {len(df.columns)}")

def validate_dq01_primary_key(data):
    print("\nRunning DQ-01 : Primary Key Validation")
    tables={"companies":"id","profitandloss":"id","balancesheet":"id","cashflow":"id","analysis":"id","financial_ratios":"id"}
    for t,pk in tables.items():
        df=data[t]
        if pk not in df.columns:
            add_failure("DQ-01",t,"CRITICAL",f"Missing {pk}")
            print(f"FAIL : {t}")
            continue
        dup=df[df.duplicated(subset=[pk],keep=False)]
        if dup.empty:
            print(f"PASS : {t}")
        else:
            print(f"FAIL : {t}")
            add_failure("DQ-01",t,"CRITICAL",f"{len(dup)} duplicate PK rows")

def validate_dq02_composite_key(data):
    print("\nRunning DQ-02 : Composite Key Validation")
    for t in ["profitandloss","balancesheet","cashflow","financial_ratios"]:
        df=data[t]
        # Check only fully identical rows
        dup = df[df.duplicated(keep=False)]
        if dup.empty:
            print(f"PASS : {t}")
        else:
            print(f"FAIL : {t}")
            add_failure(
                 "DQ-02",
                   t,
                  "WARNING",
            f"{len(dup)} completely duplicate rows found"
                 )

def validate_dq03_foreign_key(data):
    print("\nRunning DQ-03 : Foreign Key Validation")
    # Build the list of valid company names
    keys = set(
        data["companies"]["id"]
        .astype(str)
        .str.upper()
        .str.strip()
        .str.replace(r"\s+", "", regex=True)
         )
    print("\nFirst 10 Company IDs from companies table:")
    print(list(keys)[:10])  
    for t in ["profitandloss","balancesheet","cashflow","analysis","financial_ratios"]:
        df=data[t].copy()
        df["company_id"] = (
           df["company_id"]
          .astype(str)
          .str.upper()
          .str.strip()
          .str.replace(r"\s+", "", regex=True)
          )
        
        print("\nFirst 10 company_id values from", t)
        print(df["company_id"].head(10).tolist())
        invalid=df[~df["company_id"].isin(keys)]
        if invalid.empty:
          print(f"PASS : {t}")
        else:
          print(f"FAIL : {t}")

          print("\nUnmatched company_id values:")
          print(sorted(invalid["company_id"].dropna().unique())[:20])

          add_failure(
            "DQ-03",
            t,
            "WARNING",
            f"{len(invalid)} unmatched company_id values"
           )
          
def validate_dq04_positive_sales(data):

    print("\nRunning DQ-04 : Positive Sales Validation")

    df = data["profitandloss"]

    invalid = df[df["sales"] < 0]

    if invalid.empty:

        print("PASS")

    else:

        print("FAIL")

        add_failure(
            "DQ-04",
            "profitandloss",
            "WARNING",
            f"{len(invalid)} negative sales values"
        )

def validate_dq05_tax_percentage(data):

    print("\nRunning DQ-05 : Tax Percentage Validation")

    df = data["profitandloss"]

    
    invalid = df[
    df["tax_percentage"].notna() &
    (
        (df["tax_percentage"] < 0) |
        (df["tax_percentage"] > 100)
    )
   ]

    if invalid.empty:

        print("PASS")

    else:

        print("FAIL")

        add_failure(
            "DQ-05",
            "profitandloss",
            "WARNING",
            f"{len(invalid)} invalid tax percentages"
        )

def validate_dq06_year(data):

    print("\nRunning DQ-06 : Year Validation")

    tables = [

        "profitandloss",

        "balancesheet",

        "cashflow",

        "financial_ratios",

        "documents",

        "market_cap"

    ]

    for table in tables:

        df = data[table]

        invalid = df[
            (df["year"] < 2000) |
            (df["year"] > 2035)
        ]

        if invalid.empty:

            print(f"PASS : {table}")

        else:

            print(f"FAIL : {table}")

            add_failure(
                "DQ-06",
                table,
                "WARNING",
                f"{len(invalid)} invalid years"
            )

def validate_dq07_websites(data):

    print("\nRunning DQ-07 : Website URL Validation")

    df = data["companies"]

    invalid = df[
        df["website"].notna() &
        (~df["website"].str.startswith("http"))
    ]

    if invalid.empty:
        print("PASS")
    else:
        print("FAIL")
        add_failure(
            "DQ-07",
            "companies",
            "WARNING",
            f"{len(invalid)} invalid website URLs"
        )

def validate_dq08_documents(data):

    print("\nRunning DQ-08 : Annual Report URL Validation")

    df = data["documents"]

    invalid = df[
        df["annual_report"].notna() &
        (~df["annual_report"].str.startswith("http"))
    ]

    if invalid.empty:
        print("PASS")
    else:
        print("FAIL")
        add_failure(
            "DQ-08",
            "documents",
            "WARNING",
            f"{len(invalid)} invalid report URLs"
        )

def validate_dq09_stock_prices(data):

    print("\nRunning DQ-09 : Stock Price Duplicate Check")

    df = data["stock_prices"]

    dup = df[df.duplicated(subset=["company_id", "date"])]

    if dup.empty:
        print("PASS")
    else:
        print("FAIL")
        add_failure(
            "DQ-09",
            "stock_prices",
            "WARNING",
            f"{len(dup)} duplicate stock price records"
        )

def validate_dq10_market_cap(data):

    print("\nRunning DQ-10 : Market Cap Validation")

    df = data["market_cap"]

    invalid = df[df["market_cap_crore"] < 0]

    if invalid.empty:
        print("PASS")
    else:
        print("FAIL")
        add_failure(
            "DQ-10",
            "market_cap",
            "WARNING",
            f"{len(invalid)} negative market cap values"
        )

               
def save_validation_report():
    out=OUTPUT_FOLDER/"validation_failures.csv"
    pd.DataFrame(validation_failures).to_csv(out,index=False)
    print(f"\nValidation report saved to:\n{out}")

def print_summary():
    crit=sum(1 for x in validation_failures if x["Severity"]=="CRITICAL")
    warn=sum(1 for x in validation_failures if x["Severity"]=="WARNING")
    print("\n"+"="*60)
    print("DATA QUALITY SUMMARY")
    print("="*60)
    print(f"Total Findings : {len(validation_failures)}")
    print(f"Critical Issues : {crit}")
    print(f"Warnings        : {warn}")

    if len(validation_failures) == 0:
      print("\nAll Data Quality Checks PASSED")
    else:
      print("\nValidation Completed with Findings")

def main():
    print("\n========== DATA VALIDATION ==========\n")
    data=load_data()
    print_dataset_summary(data)
    validate_dq01_primary_key(data)
    validate_dq02_composite_key(data)
    validate_dq03_foreign_key(data)
    validate_dq04_positive_sales(data)
    validate_dq05_tax_percentage(data)
    validate_dq06_year(data)
    validate_dq07_websites(data)
    validate_dq08_documents(data)
    validate_dq09_stock_prices(data)
    validate_dq10_market_cap(data)
    save_validation_report()
    print_summary()

if __name__=="__main__":
    main()
