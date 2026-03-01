# event_detection.py

import numpy as np
from sklearn.cluster import KMeans


def detect_ramps(df, min_steps=2, threshold_ratio=0.03):
    """
    Detect cumulative ramp-up and ramp-down events.
    min_steps = minimum consecutive rising/falling steps.
    threshold_ratio = minimum cumulative ramp as % of max power.
    """

    df["delta_p"] = df["power"].diff().fillna(0)

    max_power = df["power"].max()
    threshold = max_power * threshold_ratio

    ramps = []
    i = 1

    while i < len(df) - min_steps:

        # Detect ramp up
        if df["delta_p"].iloc[i] > 0:

            start = i
            cumulative = df["delta_p"].iloc[i]
            steps = 1

            j = i + 1
            while j < len(df) and df["delta_p"].iloc[j] > 0:
                cumulative += df["delta_p"].iloc[j]
                steps += 1
                j += 1

            if steps >= min_steps and cumulative > threshold:
                ramps.append({
                    "index": start,
                    "type": "ON",
                    "magnitude": cumulative
                })

            i = j

        # Detect ramp down
        elif df["delta_p"].iloc[i] < 0:

            start = i
            cumulative = abs(df["delta_p"].iloc[i])
            steps = 1

            j = i + 1
            while j < len(df) and df["delta_p"].iloc[j] < 0:
                cumulative += abs(df["delta_p"].iloc[j])
                steps += 1
                j += 1

            if steps >= min_steps and cumulative > threshold:
                ramps.append({
                    "index": start,
                    "type": "OFF",
                    "magnitude": cumulative
                })

            i = j

        else:
            i += 1

    ramps_df = df.iloc[[r["index"] for r in ramps]].copy()
    ramps_df["event_type"] = [r["type"] for r in ramps]
    ramps_df["magnitude"] = [r["magnitude"] for r in ramps]

    return ramps_df


def cluster_ramps(ramps_df, n_clusters=3):

    if len(ramps_df) < n_clusters:
        ramps_df["cluster"] = 0
        return ramps_df, None

    features = ramps_df[["magnitude"]]

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    ramps_df["cluster"] = kmeans.fit_predict(features)

    cluster_summary = (
        ramps_df
        .groupby("cluster")
        .agg(
            mean_magnitude=("magnitude", "mean"),
            count=("magnitude", "count")
        )
        .reset_index()
    )

    return ramps_df, cluster_summary
