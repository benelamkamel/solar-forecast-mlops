"""First look at the eCO2mix Normandie data."""
import pandas as pd

pd.set_option("display.width", 200)          # wider display in the terminal
pd.set_option("display.max_columns", 50)     # show all columns

df = pd.read_parquet("data/raw/eco2mix_normandie.parquet")

print("Rows, columns:", df.shape)
print("\nColumns:", df.columns.tolist())

df["date_heure"] = pd.to_datetime(df["date_heure"], utc=True)
print("\nPeriod:", df["date_heure"].min(), "->", df["date_heure"].max())

print("\nSolar production (MW):")
print(df["solaire"].describe())