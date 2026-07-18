import sqlite3
import pandas as pd

conn = sqlite3.connect("data/db/nifty100.db")

tables = pd.read_sql("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name;
""", conn)

print("\nDatabase Tables:\n")
print(tables)

conn.close()