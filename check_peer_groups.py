import sqlite3
import pandas as pd

conn = sqlite3.connect("data/db/nifty100.db")

peer = pd.read_sql("SELECT company_id FROM peer_groups", conn)
ratios = pd.read_sql("SELECT DISTINCT company_id FROM financial_ratios", conn)

missing = sorted(set(ratios["company_id"]) - set(peer["company_id"]))

print("Companies in financial_ratios:", len(ratios))
print("Companies in peer_groups:", len(peer))
print("Missing companies:", len(missing))
print("\nMissing companies:")
print(missing)

conn.close()