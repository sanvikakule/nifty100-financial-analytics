from pathlib import Path
import pandas as pd
import logging

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
        "companies":"companies_clean.csv",
        "profitandloss":"profitandloss_clean.csv",
        "balancesheet":"balancesheet_clean.csv",
        "cashflow":"cashflow_clean.csv",
        "analysis":"analysis_clean.csv",
        "financial_ratios":"financial_ratios_clean.csv",
    }
    data={}
    for k,v in files.items():
        data[k]=pd.read_csv(PROCESSED_FOLDER / v)
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
    save_validation_report()
    print_summary()

if __name__=="__main__":
    main()
