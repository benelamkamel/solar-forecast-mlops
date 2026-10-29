"""Plot the solar production of Normandy on a summer day."""
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_parquet("data/raw/eco2mix_normandie.parquet")
df["date_heure"] = pd.to_datetime(df["date_heure"], utc=True)
df["local_time"] = df["date_heure"].dt.tz_convert("Europe/Paris")

day = df[df["local_time"].dt.date == pd.Timestamp("2025-06-21").date()]
day = day.sort_values("local_time")
print("Points for this day:", len(day))

plt.figure(figsize=(10, 5))
plt.plot(day["local_time"], day["solaire"], marker="o")
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M", tz="Europe/Paris"))
plt.title("Solar production in Normandy - 21 June 2025")
plt.xlabel("Local time (Paris)")
plt.ylabel("Production (MW)")
plt.grid(True)
plt.tight_layout()
plt.show()