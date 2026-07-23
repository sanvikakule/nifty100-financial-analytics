import pandas as pd

df = pd.read_csv("outputs/peer_comparison.csv")

print(df.columns.tolist())
print()
print(df.head())