# baseline_energy_analysis.py

import pandas as pd
import numpy as np

CSV_PATH = "../../../data/smart_meter_data_202602201440.csv"


def load_data():

    df = pd.read_csv(CSV_PATH, low_memory=False)

    df["timestamp"] = pd.to_datetime(df["deviceReadingTimestamp"])
    df = df.sort_values("timestamp")

    df["delta_sec"] = df["timestamp"].diff().dt.total_seconds()
    df["delta_sec"] = df["delta_sec"].fillna(1)

    return df


def segment_states(df):

    # Rough magnitude classification
    conditions = [
        df["power"] < 20,
        (df["power"] >= 40) & (df["power"] <= 120),
        (df["power"] >= 150) & (df["power"] <= 350),
        (df["power"] >= 1400) & (df["power"] <= 1900),
        df["power"] >= 2800
    ]

    labels = [
        "OFF",
        "FRIDGE",
        "LIGHTS",
        "AC_OR_KETTLE",
        "AC+KETTLE"
    ]

    df["state"] = np.select(conditions, labels, default="OTHER")

    return df


def separate_ac_kettle(df):

    df["cycle_id"] = (df["state"] != df["state"].shift()).cumsum()

    segments = []

    for cycle_id, group in df.groupby("cycle_id"):

        state = group["state"].iloc[0]
        duration = group["delta_sec"].sum()
        avg_power = group["power"].mean()

        energy = (group["power"] * group["delta_sec"]).sum() / (3600 * 1000)

        # Duration-based split
        if state == "AC_OR_KETTLE":

            if duration < 120:  # less than 2 minutes
                state = "KETTLE"
            else:
                state = "AC"

        segments.append({
            "state": state,
            "duration_sec": duration,
            "energy_kwh": energy
        })

    seg_df = pd.DataFrame(segments)

    return seg_df


def run():

    df = load_data()
    df = segment_states(df)
    seg_df = separate_ac_kettle(df)

    total_energy = seg_df["energy_kwh"].sum()

    print("\nTotal Energy (kWh):", round(total_energy, 4))
    print("\nEnergy by State:")
    print(seg_df.groupby("state")["energy_kwh"].sum().round(4))
    print("\nEnergy %:")
    print((seg_df.groupby("state")["energy_kwh"].sum() / total_energy * 100).round(2))


if __name__ == "__main__":
    run()
