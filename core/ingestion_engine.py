from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "anvaya-token"
INFLUX_ORG = "anvaya"
INFLUX_BUCKET = "nilm"

def write_dataframe_to_influx(df, measurement):

    client = InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org=INFLUX_ORG
    )

    write_api = client.write_api(write_options=SYNCHRONOUS)

    for _, row in df.iterrows():
        point = (
            Point(measurement)
            .field("power", float(row["power"]))
            .field("pf", float(row["pf"]))
        )

        write_api.write(
            bucket=INFLUX_BUCKET,
            org=INFLUX_ORG,
            record=point
        )

    print(f"Written {len(df)} rows to measurement: {measurement}")
