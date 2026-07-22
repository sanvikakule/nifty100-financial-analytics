import sqlite3

conn = sqlite3.connect("data/db/nifty100.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

print("Tables:")
for table in cursor.fetchall():
    print("-", table[0])

conn.close()