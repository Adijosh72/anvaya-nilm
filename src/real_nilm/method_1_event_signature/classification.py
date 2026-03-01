# classification.py

from appliance_signatures import auto_label_ramp_clusters


def label_ramps(ramps_df, cluster_summary):

    if cluster_summary is None:
        ramps_df["appliance"] = "UNKNOWN"
        return ramps_df

    label_map = auto_label_ramp_clusters(cluster_summary)
    ramps_df["appliance"] = ramps_df["cluster"].map(label_map)

    return ramps_df
