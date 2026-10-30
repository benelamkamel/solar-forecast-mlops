"""First look at the Open-Meteo weather data for Normandy."""
import pandas as pd

pd.set_option("display.width", 200)

df = pd.read_parquet("data/raw/open_meteo_normandie.parquet")

print("Rows, columns:", df.shape)

print("\nRows per city:")
print(df["city"].value_counts())

print("\nPeriod:", df["time"].min(), "->", df["time"].max())

print("\nDuplicated hours:", df.duplicated(["time", "city"]).sum())

print("\nMissing values per column:")
print(df.isna().sum())

print("\nStatistics:")
print(df.describe().round(1))