# run_method_1.py

import pandas as pd
import numpy as np
from event_detection import detect_ramps, cluster_ramps
from classification import label_ramps

CSV_PATH = "../../../data/smart_meter_data_202602201440.csv"


def load_data():

    df = pd.read_csv(CSV_PATH, low_memory=False)

    # ---- Handle different timestamp column names ----
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    elif "deviceReadingTimestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["deviceReadingTimestamp"])
    elif "createdAt" in df.columns:
        df["timestamp"] = pd.to_datetime(df["createdAt"])
    else:
        raise ValueError("No valid timestamp column found")

    df = df.sort_values("timestamp")

    df["delta_sec"] = df["timestamp"].diff().dt.total_seconds()
    df["delta_sec"] = df["delta_sec"].fillna(1)

    df["power"] = df["power"].rolling(window=3, center=True).mean()
    df["power"] = df["power"].bfill().ffill()

    return df


def compute_total_energy(df):
    return (df["power"] * df["delta_sec"]).sum() / (3600 * 1000)


def hybrid_ac_detection(df, ramps_df):

    ac_cluster = (
        ramps_df.groupby("cluster")["magnitude"]
        .mean()
        .idxmax()
    )

    ac_ramps = ramps_df[
        (ramps_df["cluster"] == ac_cluster) &
        (ramps_df["event_type"] == "ON")
    ]

    ac_cycles = []

    for on_idx in ac_ramps.index:

        i = on_idx

        while i < len(df) - 1:

            # AC steady region detection
            if df["power"].iloc[i] < 1000:
                break

            i += 1

        end_idx = i

        segment = df.iloc[on_idx:end_idx]

        duration_sec = segment["delta_sec"].sum()
        energy_kwh = (segment["power"] * segment["delta_sec"]).sum() / (3600 * 1000)

        if duration_sec >= 60:
            ac_cycles.append({
                "start_idx": on_idx,
                "end_idx": end_idx,
                "duration_min": duration_sec / 60,
                "energy_kwh": energy_kwh
            })

    return pd.DataFrame(ac_cycles)


def run():

    df = load_data()

    total_room_energy = compute_total_energy(df)
    print("\nTotal Room Energy (kWh):", round(total_room_energy, 4))

    print("\nDetecting ramps...")
    ramps_df = detect_ramps(df)

    print("Clustering ramps...")
    ramps_df, cluster_summary = cluster_ramps(ramps_df)

    print("\nCluster Summary:")
    print(cluster_summary)

    labeled_ramps = label_ramps(ramps_df, cluster_summary)

    print("\nRamp Distribution:")
    print(labeled_ramps["appliance"].value_counts())

    print("\nHybrid AC detection...")
    ac_cycles = hybrid_ac_detection(df, ramps_df)

    if ac_cycles.empty:
        print("No AC cycles detected.")
        return

    ac_energy = ac_cycles["energy_kwh"].sum()

    print("\nAC Energy (kWh):", round(ac_energy, 4))
    print("Average AC Duration (min):", round(ac_cycles["duration_min"].mean(), 2))

    coverage = (ac_energy / total_room_energy) * 100

    print("\nAC Coverage % of Room Energy:", round(coverage, 2), "%")

    ac_cycles.to_csv("method_1_hybrid_ac_results.csv", index=False)

    print("\nSaved to method_1_hybrid_ac_results.csv\n")


if __name__ == "__main__":
    run()
