import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from influxdb_client import InfluxDBClient
from vmdpy import VMD

st.set_page_config(layout="wide")
st.title("Anvaya AI Operator – Hotel Simulation")

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

if df.empty:
    st.warning("No data found.")
    st.stop()

# Aggregate Plot
st.subheader("Aggregate Hotel Load")
fig1, ax1 = plt.subplots()
ax1.plot(df["time"], df["power"])
st.pyplot(fig1)

# Event Detection
df["delta"] = df["power"].diff()
ON_THRESHOLD = 2000
OFF_THRESHOLD = -2000

events = df[
    (df["delta"] > ON_THRESHOLD) |
    (df["delta"] < OFF_THRESHOLD)
]

st.subheader("Detected Events")
st.write(events[["time", "delta"]])

# Event Windows
PRE = 5
POST = 5

windows = []

for idx in events.index:
    start = max(0, idx - PRE)
    end = min(len(df), idx + POST + 1)
    window = df["power"].iloc[start:end].values
    windows.append(window)

st.subheader("Event-Centric Windows")
fig2, ax2 = plt.subplots()
for w in windows:
    ax2.plot(w)
st.pyplot(fig2)

# VMD (first window only)
if len(windows) > 0:
    signal = windows[0]

    u, _, _ = VMD(signal, 2000, 0., 3, 0, 1, 1e-7)

    st.subheader("VMD Decomposition (First Event)")
    fig3, ax3 = plt.subplots()
    for k in range(3):
        ax3.plot(u[k])
    ax3.plot(signal, '--')
    st.pyplot(fig3)
