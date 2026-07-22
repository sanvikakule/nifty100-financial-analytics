import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DATABASE = "data/db/nifty100.db"
OUTPUT_DIR = "outputs/radar_charts"

os.makedirs(OUTPUT_DIR, exist_ok=True)

METRICS = [
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "return_on_equity_pct",
    "interest_coverage",
    "asset_turnover",
    "earnings_per_share"
]


def load_data():
    conn = sqlite3.connect(DATABASE)

    ratios = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    peers = pd.read_sql(
        "SELECT company_id, peer_group_name FROM peer_groups",
        conn
    )

    conn.close()

    df = ratios.merge(peers, on="company_id", how="inner")

    return df


def normalize(series):
    series = series.fillna(0)

    mn = series.min()
    mx = series.max()

    if mn == mx:
        return pd.Series(
            [50] * len(series),
            index=series.index
        )

    return ((series - mn) / (mx - mn)) * 100


def create_radar(company, year, df):

    company_row = df[
        (df.company_id == company) &
        (df.year == year)
    ]

    if company_row.empty:
        return

    peer_group = company_row.iloc[0]["peer_group_name"]

    peer_df = df[
        (df.peer_group_name == peer_group) &
        (df.year == year)
    ].copy()

    company_values = []
    peer_values = []

    for metric in METRICS:

        peer_df[metric] = peer_df[metric].fillna(0)

        normalized = normalize(peer_df[metric])

        peer_df["normalized"] = normalized

        company_value = peer_df.loc[
            peer_df.company_id == company,
            "normalized"
        ]

        if company_value.empty:
            company_values.append(0)
        else:
            company_values.append(float(company_value.iloc[0]))

        peer_values.append(float(normalized.mean()))

    labels = [
        "Net\nProfit",
        "Operating\nMargin",
        "ROE",
        "Interest\nCoverage",
        "Asset\nTurnover",
        "EPS"
    ]

    N = len(labels)

    angles = np.linspace(
        0,
        2 * np.pi,
        N,
        endpoint=False
    ).tolist()

    angles += angles[:1]

    company_values += company_values[:1]
    peer_values += peer_values[:1]

    fig, ax = plt.subplots(
        figsize=(7, 7),
        subplot_kw={"polar": True}
    )

    ax.plot(
        angles,
        company_values,
        linewidth=2,
        label=company
    )

    ax.fill(
        angles,
        company_values,
        alpha=0.25
    )

    ax.plot(
        angles,
        peer_values,
        linewidth=2,
        linestyle="--",
        label="Peer Average"
    )

    ax.fill(
        angles,
        peer_values,
        alpha=0.10
    )

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10)

    ax.set_ylim(0, 100)

    plt.title(
        f"{company} vs Peer Average ({year})",
        fontsize=14,
        pad=20
    )

    plt.legend(loc="upper right")

    plt.tight_layout()

    filename = os.path.join(
        OUTPUT_DIR,
        f"{company}_{year}.png"
    )

    plt.savefig(
        filename,
        dpi=150
    )

    plt.close()


def main():

    df = load_data()

    latest_year = df["year"].max()

    companies = (
        df[df["year"] == latest_year][
            ["company_id", "year"]
        ]
        .drop_duplicates()
        .values
    )

    print(f"\nLatest Year : {latest_year}")
    print(f"Companies   : {len(companies)}\n")

    count = 0

    for company, year in companies:

        print(f"Generating {company}...")

        create_radar(company, year, df)

        count += 1

    print("\n--------------------------------")

    print(f"Generated {count} radar charts.")

    print(f"Saved in : {OUTPUT_DIR}")

    print("--------------------------------")


if __name__ == "__main__":
    main()