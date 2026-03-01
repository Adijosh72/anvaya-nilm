# utils.py

import pandas as pd


def load_data(csv_path):

    df = pd.read_csv(csv_path, low_memory=False)

    # Universal timestamp handling
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

    return df


def compute_total_energy(df):

    return (df["power"] * df["delta_sec"]).sum() / (3600 * 1000)
