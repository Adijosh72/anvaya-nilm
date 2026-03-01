# appliance_signatures.py

def auto_label_ramp_clusters(cluster_summary):

    labels = {}

    sorted_clusters = cluster_summary.sort_values("mean_magnitude").reset_index(drop=True)

    if len(sorted_clusters) == 1:
        labels[sorted_clusters.iloc[0]["cluster"]] = "UNKNOWN"
        return labels

    # Largest ramp → AC
    labels[sorted_clusters.iloc[-1]["cluster"]] = "AC"

    if len(sorted_clusters) >= 2:
        labels[sorted_clusters.iloc[-2]["cluster"]] = "KETTLE"

    if len(sorted_clusters) >= 3:
        labels[sorted_clusters.iloc[0]["cluster"]] = "FRIDGE"

    return labels
