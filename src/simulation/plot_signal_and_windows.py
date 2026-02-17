from influxdb_client import InfluxDBClient
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# InfluxDB Config
# -----------------------------
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "anvaya-token"
INFLUX_ORG = "anvaya"
INFLUX_BUCKET = "nilm"

client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)

query_api = client.query_api()

# -----------------------------
# Read data
# -----------------------------
query = """
from(bucket: "nilm")
  |> range(start: -30m)
  |> filter(fn: (r) => r._measurement == "aggregate_power_v1")
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

# -----------------------------
# Plot aggregate signal
# -----------------------------
plt.figure()
plt.plot(df["time"], df["power"])
plt.xlabel("Time")
plt.ylabel("Power (W)")
plt.title("Aggregate Power (1 Hz)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# -----------------------------
# Sliding window visualisation
# -----------------------------
WINDOW_SIZE = 6
power_values = df["power"].values

plt.figure()
for i in range(len(power_values) - WINDOW_SIZE + 1):
    window = power_values[i:i + WINDOW_SIZE]
    plt.plot(window)

plt.title("Sliding Windows (Each line = 1 window)")
plt.xlabel("Seconds in window")
plt.ylabel("Power (W)")
plt.tight_layout()
plt.show()
