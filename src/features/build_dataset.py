"""Build the training table: RTE production + Open-Meteo weather, hourly, UTC."""
from pathlib import Path

import pandas as pd

RTE_FILE = "data/raw/eco2mix_normandie.parquet"
WEATHER_FILE = "data/raw/open_meteo_normandie.parquet"
PROCESSED_FILE = "data/processed/training_table.parquet"


def load_production_hourly(path: str = RTE_FILE) -> pd.DataFrame:
    """Load RTE solar production and convert it from 30 min to 1 hour."""
    df = pd.read_parquet(path, columns=["date_heure", "solaire", "tch_solaire"])
    df["date_heure"] = pd.to_datetime(df["date_heure"], utc=True)
    df = df.sort_values("date_heure").set_index("date_heure")

    hourly = df.resample("1h", label="right", closed="right").mean()
    hourly.index.name = "time"
    return hourly


def load_weather_wide(path: str = WEATHER_FILE) -> pd.DataFrame:
    """Load Open-Meteo weather and put the 4 cities side by side."""
    df = pd.read_parquet(path)
    wide = df.pivot(index="time", columns="city")
    wide.columns = [f"{variable}_{city}" for variable, city in wide.columns]
    return wide.sort_index()


def build_training_table() -> pd.DataFrame:
    """Join weather (inputs) and production (target) on the same hours."""
    production = load_production_hourly()
    weather = load_weather_wide()

    # Same date format on both sides: UTC, nanosecond precision
    for df in (production, weather):
        df.index = pd.to_datetime(df.index, utc=True).as_unit("ns")
        df.index.name = "time"

    return weather.join(production, how="inner")


def save_training_table(table: pd.DataFrame, path: str = PROCESSED_FILE) -> Path:
    """Save the training table as a Parquet file."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    table.to_parquet(file_path)
    return file_path


if __name__ == "__main__":
    table = build_training_table()
    print("Rows, columns:", table.shape)
    print("Period:", table.index.min(), "->", table.index.max())
    print("Index type:", table.index.dtype)

    missing = table.isna().sum()
    print("\nColumns with missing values:")
    print(missing[missing > 0])

    print("\n21 June 2025:")
    print(table.loc["2025-06-21 10:00":"2025-06-21 14:00",
                    ["shortwave_radiation_caen", "shortwave_radiation_rouen", "solaire"]])

    file_path = save_training_table(table)
    print(f"\nSaved: {file_path}")