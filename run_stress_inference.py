import pandas as pd
from influxdb_client import InfluxDBClient

INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "anvaya-token"
INFLUX_ORG = "anvaya"
INFLUX_BUCKET = "nilm"

# -----------------------------
# Read from Influx
# -----------------------------

client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)

query_api = client.query_api()

query = f'''
from(bucket: "{INFLUX_BUCKET}")
  |> range(start: -7d)
  |> filter(fn: (r) => r._measurement == "room_sim_24h_v1")
  |> filter(fn: (r) => r._field == "power")
'''

result = query_api.query_data_frame(query)

if result.empty:
    raise RuntimeError("No data found")

df = result[["_time", "_value"]].rename(
    columns={"_time": "time", "_value": "power"}
)

df = df.sort_values("time")

print(f"Loaded samples: {len(df)}")

# -----------------------------
# Event Detection
# -----------------------------

df["delta"] = df["power"].diff()

ON_THRESHOLD = 400
OFF_THRESHOLD = -400

events = df[
    (df["delta"] > ON_THRESHOLD) |
    (df["delta"] < OFF_THRESHOLD)
]

print(f"Total detected events: {len(events)}")

# -----------------------------
# Classification
# -----------------------------

def classify(delta):
    delta = abs(delta)

    if delta > 1500:
        return "Kettle"
    elif 800 < delta < 1500:
        return "AC"
    elif 100 < delta < 400:
        return "Fridge"
    else:
        return "Unknown"

events["appliance"] = events["delta"].apply(classify)

print("\nEvent Distribution:")
print(events["appliance"].value_counts())
