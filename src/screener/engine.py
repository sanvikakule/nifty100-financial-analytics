# ==========================================================
# NIFTY 100 SCREENER ENGINE
# ==========================================================

# ==========================================================
# SETTINGS
# ==========================================================

USE_PRESET = True
PRESET_NAME = "quality_compounder"

# ==========================================================
# IMPORTS
# ==========================================================

import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from src.screener.data_loader import load_screener_data
from src.screener.filters import apply_filters
from src.screener.presets import run_preset
from src.screener.ranking import top_companies
from src.screener.validator import validate_dataframe
from src.visualization.radar_chart import generate_radar_chart
from src.reports.excel_report import export_excel_report
from src.utils.logger import logger

# ==========================================================
# PATHS
# ==========================================================

CONFIG = ROOT / "config" / "screener_config.yaml"

# ==========================================================
# MAIN ENGINE
# ==========================================================

def main():

    logger.info("=" * 60)
    logger.info("NIFTY 100 Screener Engine Started")

    print("\n========== NIFTY 100 SCREENER ENGINE ==========\n")

    # ======================================================
    # LOAD DATA
    # ======================================================

    print("Loading screener data...\n")

    df = load_screener_data()

    validate_dataframe(df)

    logger.info(f"Loaded {len(df)} companies.")

    print("✓ Screener data loaded successfully")
    print("✓ Data validation passed.\n")

    print(f"Rows    : {len(df)}")
    print(f"Columns : {len(df.columns)}")

    print("\nPreview:\n")

    print(
        df[
            [
                "company_id",
                "company_name",
                "return_on_equity_pct",
                "debt_to_equity",
                "market_cap_crore",
            ]
        ].head()
    )

    # ======================================================
    # LOAD CONFIG
    # ======================================================

    print("\nLoading screener configuration...\n")

    with open(CONFIG, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if "filters" not in config:
        raise ValueError("Invalid screener configuration.")

    logger.info("Configuration loaded successfully.")

    print("✓ Configuration loaded successfully")

    print("\nCurrent Configuration:\n")
    print(config)

    # ======================================================
    # RUN SCREENER
    # ======================================================

    if USE_PRESET:

        print(f"\nRunning Preset Screener : {PRESET_NAME}\n")

        filtered_df = run_preset(
            df,
            PRESET_NAME
        )

    else:

        print("\nRunning Custom YAML Screener\n")

        filtered_df = apply_filters(
            df,
            config
        )

    logger.info(f"Filtered companies : {len(filtered_df)}")

    # ======================================================
    # VALIDATE RESULTS
    # ======================================================

    if filtered_df.empty:
        raise ValueError(
            "No companies matched the selected filters."
        )

    # ======================================================
    # RESULTS
    # ======================================================

    print("\n========== FILTER RESULTS ==========\n")

    print(f"Original Records : {len(df)}")
    print(f"Filtered Records : {len(filtered_df)}")

    print("\nFiltered Preview:\n")
    print(filtered_df.head())

    # ======================================================
    # TOP 10
    # ======================================================

    print("\n========== TOP 10 COMPANIES ==========\n")

    top10 = top_companies(filtered_df)

    print(
        top10[
            [
                "quality_rank",
                "company_id",
                "company_name",
                "composite_quality_score",
            ]
        ]
    )

    # ======================================================
    # RADAR CHART
    # ======================================================

    print("\nGenerating Radar Chart...\n")

    company1 = top10.iloc[0]["company_id"]
    company2 = top10.iloc[1]["company_id"]

    generate_radar_chart(
        filtered_df,
        company1,
        company2
    )

    logger.info(
        f"Radar chart generated for {company1} vs {company2}"
    )

    # ======================================================
    # EXCEL REPORT
    # ======================================================

    print("\nGenerating Excel Report...\n")

    export_excel_report(filtered_df)

    logger.info("Excel report generated successfully.")

    # ======================================================
    # COMPLETE
    # ======================================================

    print("\n========== SCREENER ENGINE READY ==========\n")

    logger.info("Engine completed successfully.")
    logger.info("=" * 60)


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":

    try:
        main()

    except Exception as e:

        logger.exception("Engine failed.")

        print("\n❌ ERROR")
        print("=" * 50)
        print(e)
        print("=" * 50)