from influxdb_client import InfluxDBClient
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# InfluxDB Config
# -----------------------------
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "anvaya-token"
INFLUX_ORG = "anvaya"
INFLUX_BUCKET = "nilm"
MEASUREMENT = "hotel_12room_v1"

client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)

query_api = client.query_api()

# -----------------------------
# Query latest dataset
# -----------------------------
query = f"""
from(bucket: "{INFLUX_BUCKET}")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "{MEASUREMENT}")
  |> filter(fn: (r) => r._field == "power")
  |> sort(columns: ["_time"])
"""

tables = query_api.query(query)

records = []
for table in tables:
    for row in table.records:
        records.append({
            "time": row.get_time(),
            "power": row.get_value()
        })

df = pd.DataFrame(records)

if df.empty:
    raise RuntimeError("No data found for hotel_12room_v1")

# -----------------------------
# Event Detection
# -----------------------------
df["delta"] = df["power"].diff()

ON_THRESHOLD = 2000
OFF_THRESHOLD = -2000

on_events = df[df["delta"] > ON_THRESHOLD]
off_events = df[df["delta"] < OFF_THRESHOLD]

print("\nON Events:")
print(on_events[["time", "delta"]])

print("\nOFF Events:")
print(off_events[["time", "delta"]])

# -----------------------------
# Plot
# -----------------------------
plt.figure()
plt.plot(df["time"], df["power"], label="Aggregate Power")

plt.scatter(on_events["time"], on_events["power"],
            marker="^", s=100, label="ON")

plt.scatter(off_events["time"], off_events["power"],
            marker="v", s=100, label="OFF")

plt.legend()
plt.xticks(rotation=45)
plt.title("Hotel Event Detection")
plt.tight_layout()
plt.show()

