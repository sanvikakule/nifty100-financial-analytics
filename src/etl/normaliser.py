import re
import pandas as pd


def normalize_column_names(df):
    """
    Standardize column names.
    Example:
    Net Profit (%) -> net_profit
    """
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("%", "", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace("/", "_", regex=False)
    )
    return df


def normalize_text(df):
    """
    Remove extra spaces from text columns.
    """
    for col in df.select_dtypes(include="object").columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )
    return df


def normalize_ticker(df):
    """
    Standardize ticker column if it exists.
    """
    possible_columns = ["ticker", "symbol", "stock_symbol"]

    for col in possible_columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.upper()
                .str.replace(".NS", "", regex=False)
                .str.strip()
            )

    return df


def normalize_year(df):
    """
    Convert FY22, FY2022 etc. into 2022.
    """
    possible_columns = ["year", "fy", "financial_year"]

    for col in possible_columns:

        if col in df.columns:

            def clean_year(x):

                if pd.isna(x):
                    return x

                x = str(x).upper().replace("FY", "").strip()

                match = re.search(r"\d{4}", x)

                if match:
                    return int(match.group())

                match = re.search(r"\d{2}", x)

                if match:
                    return int("20" + match.group())

                return x

            df[col] = df[col].apply(clean_year)

    return df


def normalize_numeric(df):
    """
    Clean numeric columns by removing commas, currency symbols,
    percentages and converting values to numeric.
    """

    for col in df.columns:

        if df[col].dtype == object:

            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("₹", "", regex=False)
                .str.replace("%", "", regex=False)
                .str.replace("Cr", "", regex=False)
                .str.replace("cr", "", regex=False)
                .str.strip()
            )

            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df
    