from pathlib import Path
import pandas as pd
import logging
import time

from normaliser import (
    normalize_column_names,
    normalize_text,
    normalize_ticker,
    normalize_year,
    normalize_numeric,
)

# ==========================================================
# PROJECT PATHS
# ==========================================================

ROOT = Path(__file__).resolve().parents[2]

RAW_FOLDER = ROOT / "data" / "raw"
PROCESSED_FOLDER = ROOT / "data" / "processed"
LOG_FOLDER = ROOT / "logs"

PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)
LOG_FOLDER.mkdir(parents=True, exist_ok=True)

# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(
    filename=LOG_FOLDER / "etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# ==========================================================
# LOAD FILE FUNCTION
# ==========================================================


def load_file(file_path):
    """
    Reads CSV or Excel file.
    """

    if file_path.suffix.lower() == ".csv":
        return pd.read_csv(file_path)

    elif file_path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(file_path)

    else:
        raise Exception("Unsupported file format")


# ==========================================================
# CLEAN DATAFRAME
# ==========================================================


def clean_dataframe(df):
    """
    Apply all normalization functions.
    """

    df = normalize_column_names(df)
    df = normalize_text(df)
    df = normalize_ticker(df)
    df = normalize_year(df)
    df = normalize_numeric(df)

    return df


# ==========================================================
# SAVE FILE
# ==========================================================


def save_dataframe(df, original_file):

    output_name = original_file.stem + "_clean.csv"

    output_path = PROCESSED_FOLDER / output_name

    df.to_csv(output_path, index=False)

    return output_path


# ==========================================================
# MAIN ETL
# ==========================================================


def main():

    print("\n========== ETL LOADER ==========\n")

    logging.info("========== ETL Started ==========")

    files = []

    files.extend(RAW_FOLDER.glob("*.csv"))
    files.extend(RAW_FOLDER.glob("*.xlsx"))
    files.extend(RAW_FOLDER.glob("*.xls"))

    files = sorted(files)

    print(f"Found {len(files)} files.\n")

    success = 0
    failed = 0

    audit_log = []

    for file in files:

        start_time = time.time()

        print("=" * 60)
        print(f"Processing : {file.name}")

        try:

            # ----------------------------------------
            # LOAD
            # ----------------------------------------

            df = load_file(file)

            rows = df.shape[0]
            cols = df.shape[1]

            print(f"Rows    : {rows}")
            print(f"Columns : {cols}")

            logging.info(f"{file.name} loaded successfully")

            # ----------------------------------------
            # CLEAN
            # ----------------------------------------

            df = clean_dataframe(df)

            logging.info(f"{file.name} cleaned")

            # ----------------------------------------
            # SAVE
            # ----------------------------------------

            output_path = save_dataframe(df, file)

            print(f"Saved    : {output_path.name}")

            logging.info(f"{output_path.name} saved")

            processing_time = round(time.time() - start_time, 2)

            audit_log.append({
                "file_name": file.name,
                "rows": rows,
                "columns": cols,
                "status": "Success",
                "processing_time_sec": processing_time,
                "error": ""
            })

            success += 1

        except Exception as e:

            processing_time = round(time.time() - start_time, 2)

            print(f"ERROR : {file.name}")
            print(e)

            logging.error(f"{file.name} : {e}")

            audit_log.append({
                "file_name": file.name,
                "rows": 0,
                "columns": 0,
                "status": "Failed",
                "processing_time_sec": processing_time,
                "error": str(e)
            })

            failed += 1

        print()

    # ----------------------------------------------------
    # SAVE LOAD AUDIT
    # ----------------------------------------------------

    OUTPUT_FOLDER = ROOT / "output"
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    audit_df = pd.DataFrame(audit_log)

    audit_path = OUTPUT_FOLDER / "load_audit.csv"

    audit_df.to_csv(audit_path, index=False)

    logging.info(f"Load audit saved at {audit_path}")

    # ----------------------------------------------------
    # SUMMARY
    # ----------------------------------------------------

    print("=" * 60)

    print("\nETL SUMMARY\n")

    print(f"Processed Successfully : {success}")
    print(f"Failed                 : {failed}")
    print(f"Processed Folder       : {PROCESSED_FOLDER}")
    print(f"Audit File             : {audit_path}")

    logging.info("========== ETL Completed ==========")


# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":
    main()