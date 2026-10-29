"""Download RTE eCO2mix regional data (production by source, every 30 min)."""
from pathlib import Path

import requests

# Address of the RTE open data API (dataset: consolidated regional data since 2021)
URL = (
    "https://odre.opendatasoft.com/api/explore/v2.1/catalog/"
    "datasets/eco2mix-regional-cons-def/exports/parquet"
)


def download_region(region: str = "Normandie", out_dir: str = "data/raw") -> Path:
    """Download the data of one region and save it as a Parquet file."""
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    file_path = out_path / f"eco2mix_{region.lower()}.parquet"

    params = {
        "where": f'libelle_region="{region}"',  # keep only our region
        "timezone": "UTC",                       # same time reference everywhere
    }

    print(f"Downloading {region} data... (may take a few minutes)")
    response = requests.get(URL, params=params, timeout=900)
    response.raise_for_status()
    file_path.write_bytes(response.content)
    print(f"Done: {file_path}")
    return file_path


if __name__ == "__main__":
    download_region()