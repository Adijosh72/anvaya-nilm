import numpy as np
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import random
import time

# -----------------------------
# Influx Config
# -----------------------------
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "anvaya-token"
INFLUX_ORG = "anvaya"
INFLUX_BUCKET = "nilm"

MEASUREMENT = "hotel_12room_v1"   # NEW measurement (clean dataset)

client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)

write_api = client.write_api(write_options=SYNCHRONOUS)

# -----------------------------
# Simulation Parameters
# -----------------------------
SAMPLES = 100
BASE_LOAD = 3000  # lighting, kitchen standby, servers etc (W)

ROOM_AC_POWER = 1500  # 1.5 kW per room AC
NUM_ROOMS = 12

COMMON_HVAC_POWER = 12000  # 17 ton ~12kW realistic electrical
HEAT_PUMP_POWER = 4000

# -----------------------------
# State variables
# -----------------------------
room_states = [0] * NUM_ROOMS
hvac_on = False
heat_pump_on = False

print("Simulating hotel load...")

for t in range(SAMPLES):

    total_power = BASE_LOAD

    # -----------------------------
    # Room AC behavior (random staggered usage)
    # -----------------------------
    for i in range(NUM_ROOMS):

        # Randomly toggle some ACs
        if random.random() < 0.05:
            room_states[i] = 1 - room_states[i]

        if room_states[i] == 1:
            total_power += ROOM_AC_POWER

    # -----------------------------
    # Common HVAC active during "11am-1pm"
    # We'll simulate that between sample 30–70
    # -----------------------------
    if 30 <= t <= 70:
        hvac_on = True
    else:
        hvac_on = False

    if hvac_on:
        total_power += COMMON_HVAC_POWER

    # -----------------------------
    # Heat Pump cycling
    # -----------------------------
    if random.random() < 0.1:
        heat_pump_on = 1 - heat_pump_on

    if heat_pump_on:
        total_power += HEAT_PUMP_POWER

    # -----------------------------
    # Add realistic noise (+/- 2%)
    # -----------------------------
    noise = np.random.normal(0, total_power * 0.02)
    total_power += noise

    # -----------------------------
    # Write to Influx
    # -----------------------------
    point = (
        Point(MEASUREMENT)
        .field("power", float(total_power))
    )

    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)

print("✅ 100-sample hotel dataset written successfully.")
