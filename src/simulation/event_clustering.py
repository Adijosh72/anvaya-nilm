from influxdb_client import InfluxDBClient
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from vmdpy import VMD
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

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

# -----------------------------
# Extract Event-Centric Windows
# -----------------------------
PRE = 5
POST = 5

windows = []

for idx in event_indices:
    start = max(0, idx - PRE)
    end = min(len(df), idx + POST + 1)
    window = df["power"].iloc[start:end].values
    windows.append(window)

# -----------------------------
# Extract VMD Features
# -----------------------------
features = []

for w in windows:
    if len(w) < 6:
        continue

    u, _, _ = VMD(w, 2000, 0., 3, 0, 1, 1e-7)
    feat = [np.mean(np.abs(mode)) for mode in u]
    features.append(feat)

features = np.array(features)

if len(features) < 2:
    print("Not enough events for clustering.")
    exit()

# -----------------------------
# KMeans Clustering
# -----------------------------
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(features)

print("Cluster assignments:", labels)

# -----------------------------
# PCA Visualization
# -----------------------------
pca = PCA(n_components=2)
reduced = pca.fit_transform(features)

plt.figure()
for i in range(len(reduced)):
    plt.scatter(reduced[i, 0], reduced[i, 1])
    plt.text(reduced[i, 0], reduced[i, 1], str(labels[i]))

plt.title("Event Clusters (VMD Feature Space)")
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.tight_layout()
plt.show()
