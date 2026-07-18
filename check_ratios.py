import sqlite3
import pandas as pd

conn = sqlite3.connect("data/db/nifty100.db")

# Total rows
query = "SELECT COUNT(*) AS total_rows FROM financial_ratios;"
print(pd.read_sql(query, conn))

# Duplicate company-year combinations
query = """
SELECT company_id,
       year,
       COUNT(*) AS duplicate_count
FROM financial_ratios
GROUP BY company_id, year
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;
"""

duplicates = pd.read_sql(query, conn)

print("\nDuplicate Company-Year Records:")
print(duplicates.head(20))

print("\nTotal Duplicate Keys:", len(duplicates))

conn.close()