from influxdb_client import InfluxDBClient
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Config
# -----------------------------
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "anvaya-token"
INFLUX_ORG = "anvaya"
INFLUX_BUCKET = "nilm"
MEASUREMENT = "hotel_12room_v1"

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
query_api = client.query_api()

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

df["delta"] = df["power"].diff()

ON_THRESHOLD = 2000
OFF_THRESHOLD = -2000

event_indices = df[
    (df["delta"] > ON_THRESHOLD) |
    (df["delta"] < OFF_THRESHOLD)
].index.tolist()

print("Detected events:", event_indices)

PRE = 5
POST = 5

windows = []

for idx in event_indices:
    start = max(0, idx - PRE)
    end = min(len(df), idx + POST + 1)
    window = df["power"].iloc[start:end].values
    windows.append(window)

plt.figure()
for w in windows:
    plt.plot(w)

plt.title("Event-Centric Windows (Hotel)")
plt.tight_layout()
plt.show()

