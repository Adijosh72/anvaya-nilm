# real_nilm_state_duration_analysis.py
# Analyze how long each clustered state lasts

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

print("="*70)
print("REAL NILM - STATE DURATION ANALYSIS")
print("="*70)

CSV_FILE = "data/room_phase_1.csv"

df = pd.read_csv(CSV_FILE, low_memory=False)
df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed', errors='coerce')
df = df.dropna(subset=['timestamp'])
df = df.sort_values('timestamp').reset_index(drop=True)

# Cluster
kmeans = KMeans(n_clusters=4, random_state=42)
df['state'] = kmeans.fit_predict(df[['power']])

centroids = kmeans.cluster_centers_.flatten()
state_order = np.argsort(centroids)
state_map = {state_order[i]: i for i in range(len(state_order))}
df['state_rank'] = df['state'].map(state_map)

# Calculate durations
df['delta_sec'] = df['timestamp'].diff().dt.total_seconds()
df['delta_sec'] = df['delta_sec'].fillna(0)

# Group consecutive same-state segments
segments = []
current_state = df.iloc[0]['state_rank']
start_time = df.iloc[0]['timestamp']
duration = 0

for i in range(1, len(df)):
    if df.iloc[i]['state_rank'] == current_state:
        duration += df.iloc[i]['delta_sec']
    else:
        segments.append({
            "state": current_state,
            "duration_sec": duration
        })
        current_state = df.iloc[i]['state_rank']
        duration = df.iloc[i]['delta_sec']

segments_df = pd.DataFrame(segments)

print("\nState Centroids:")
for i in range(len(state_order)):
    print(f"State {i}: {round(centroids[state_order[i]],2)} W")

print("\nDuration Summary (seconds):")
print(segments_df.groupby("state")["duration_sec"].describe())

print("="*70)
