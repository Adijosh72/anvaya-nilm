from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import time

INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "anvaya-token"
INFLUX_ORG = "anvaya"
INFLUX_BUCKET = "nilm"

client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)

write_api = client.write_api(write_options=SYNCHRONOUS)

print("🚀 Writing dummy 1 Hz aggregate power data to InfluxDB...")

power_series = [120, 120, 120, 350, 360, 355, 120, 120, 120]

for power in power_series:
    point = (
        Point("aggregate_power_v1")   # 👈 NEW measurement
        .field("power", float(power))
    )

    write_api.write(
        bucket=INFLUX_BUCKET,
        org=INFLUX_ORG,
        record=point
    )

    print(f"✅ Written power = {power} W")
    time.sleep(1)

print("🎉 Done writing data successfully")
