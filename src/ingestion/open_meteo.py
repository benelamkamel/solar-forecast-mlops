"""Download archived weather forecasts from Open-Meteo for Normandy cities."""
import time
from pathlib import Path

import pandas as pd
import requests

URL = "https://historical-forecast-api.open-meteo.com/v1/forecast"

# GPS coordinates (latitude, longitude) of the 4 cities
CITIES = {
    "caen": (49.18, -0.37),
    "rouen": (49.44, 1.10),
    "cherbourg": (49.64, -1.62),
    "alencon": (48.43, 0.09),
}

# V1 variables: solar radiation, cloud cover, temperature
VARIABLES = ["shortwave_radiation", "cloud_cover", "temperature_2m"]


def download_city(name: str, lat: float, lon: float, start: str, end: str) -> pd.DataFrame:
    """Download hourly weather for one city and one period."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start,
        "end_date": end,
        "hourly": ",".join(VARIABLES),
        "timezone": "GMT",  # UTC, same as the RTE data
    }
    response = requests.get(URL, params=params, timeout=120)
    response.raise_for_status()

    df = pd.DataFrame(response.json()["hourly"])
    df["time"] = pd.to_datetime(df["time"], utc=True)
    df["city"] = name
    return df


def download_all(start_year: int = 2022, end_date: str = "2026-08-31",
                 out_dir: str = "data/raw") -> Path:
    """Download all cities, year by year, and save one Parquet file."""
    frames = []
    for name, (lat, lon) in CITIES.items():
        for year in range(start_year, int(end_date[:4]) + 1):
            start = f"{year}-01-01"
            end = min(f"{year}-12-31", end_date)
            print(f"{name}: {start} -> {end}")
            frames.append(download_city(name, lat, lon, start, end))
            time.sleep(1)  # be polite with the free API

    data = pd.concat(frames, ignore_index=True)

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    file_path = out_path / "open_meteo_normandie.parquet"
    data.to_parquet(file_path, index=False)
    print(f"Done: {file_path} ({len(data)} rows)")
    return file_path


if __name__ == "__main__":
    download_all()