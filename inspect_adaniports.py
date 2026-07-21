import sqlite3
import pandas as pd

conn = sqlite3.connect("data/db/nifty100.db")

df = pd.read_sql("""
SELECT *
FROM profitandloss
WHERE company_id = 'ADANIPORTS'
ORDER BY year;
""", conn)

print(df)

conn.close()