# ==========================================================
# RADAR CHART COMPARISON
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


METRICS = [
    "return_on_equity_pct",
    "operating_profit_margin_pct",
    "interest_coverage",
    "asset_turnover",
    "free_cash_flow_cr",
    "debt_to_equity",
]


def normalize(values):
    """
    Normalize values between 0 and 1.
    """
    values = np.array(values, dtype=float)

    minimum = values.min()
    maximum = values.max()

    if minimum == maximum:
        return np.ones_like(values)

    return (values - minimum) / (maximum - minimum)


def generate_radar_chart(df, company1, company2):

    c1 = df[df["company_id"] == company1.upper()]
    c2 = df[df["company_id"] == company2.upper()]

    if c1.empty or c2.empty:
        raise ValueError("Company not found.")

    c1 = c1.iloc[0]
    c2 = c2.iloc[0]

    values1 = [c1[m] for m in METRICS]
    values2 = [c2[m] for m in METRICS]

    # Normalize each metric across the two companies
    normalized1 = []
    normalized2 = []

    for i , metric in enumerate(METRICS):
        pair = normalize([values1[i], values2[i]])
         # Reverse Debt-to-Equity because lower is better
        if metric == "debt_to_equity":
            pair = 1 - pair

        normalized1.append(pair[0])
        normalized2.append(pair[1])

    angles = np.linspace(
        0,
        2 * np.pi,
        len(METRICS),
        endpoint=False
    )

    angles = np.concatenate((angles, [angles[0]]))

    normalized1.append(normalized1[0])
    normalized2.append(normalized2[0])

    fig, ax = plt.subplots(
        figsize=(8, 8),
        subplot_kw=dict(polar=True)
    )

    ax.plot(
        angles,
        normalized1,
        linewidth=2,
        label=company1.upper()
    )

    ax.fill(
        angles,
        normalized1,
        alpha=0.25
    )

    ax.plot(
        angles,
        normalized2,
        linewidth=2,
        label=company2.upper()
    )

    ax.fill(
        angles,
        normalized2,
        alpha=0.25
    )

    labels = [
    "ROE",
    "OP Margin",
    "Interest",
    "Asset Turnover",
    "FCF",
    "Debt/Equity"
]
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    ax.set_title(
        f"{company1.upper()} vs {company2.upper()}",
        fontsize=15,
        pad=20
    )

    ax.legend(
        loc="upper right",
        bbox_to_anchor=(1.2, 1.1)
    )

    output_dir = Path(__file__).parent / "charts"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / f"{company1}_{company2}.png"

    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Radar chart saved to: {output_file}")