import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATABASE = ROOT / "data" / "db" / "nifty100.db"

conn = sqlite3.connect(DATABASE)

cursor = conn.cursor()

queries = {
    "Total Companies":
    "SELECT COUNT(*) FROM companies;",

    "Top 5 Companies":
    """
    SELECT company_name, book_value
    FROM companies
    LIMIT 5;
    """,

    "Top Sales":
    """
    SELECT company_id, year, sales
    FROM profitandloss
    ORDER BY sales DESC
    LIMIT 5;
    """,

    "Highest ROE":
    """
    SELECT company_id, return_on_equity_pct
    FROM financial_ratios
    ORDER BY return_on_equity_pct DESC
    LIMIT 5;
    """
}

print("\n========== QUERY RESULTS ==========\n")

for title, query in queries.items():

    print(f"\n{title}")
    print("-" * 40)

    cursor.execute(query)

    rows = cursor.fetchall()

    for row in rows:
        print(row)

conn.close()

print("\nDone.")