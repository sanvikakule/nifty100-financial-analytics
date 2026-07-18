import sqlite3

conn = sqlite3.connect("data/db/nifty100.db")

cursor = conn.cursor()

cursor.execute("DELETE FROM financial_ratios")

conn.commit()

print("financial_ratios table cleared successfully.")

cursor.execute("SELECT COUNT(*) FROM financial_ratios")
print("Rows after delete:", cursor.fetchone()[0])

conn.close()