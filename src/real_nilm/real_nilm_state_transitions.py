# real_nilm_state_transitions.py
# Detect transitions between clustered power states

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

print("="*70)
print("REAL NILM - STATE TRANSITION DETECTION")
print("="*70)

CSV_FILE = "data/room_phase_1.csv"

df = pd.read_csv(CSV_FILE, low_memory=False)
df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed', errors='coerce')
df = df.dropna(subset=['timestamp'])
df = df.sort_values('timestamp').reset_index(drop=True)

# Cluster into 4 states
kmeans = KMeans(n_clusters=4, random_state=42)
df['state'] = kmeans.fit_predict(df[['power']])

# Map states to sorted order
centroids = kmeans.cluster_centers_.flatten()
state_order = np.argsort(centroids)

state_map = {state_order[i]: i for i in range(len(state_order))}
df['state_rank'] = df['state'].map(state_map)

print("\nState centroids (sorted):")
for i in range(len(state_order)):
    print(f"State {i}: {round(centroids[state_order[i]],2)} W")

# Detect transitions
transitions = []

for i in range(1, len(df)):
    prev_state = df.iloc[i-1]['state_rank']
    curr_state = df.iloc[i]['state_rank']
    
    if prev_state != curr_state:
        transitions.append({
            "timestamp": df.iloc[i]['timestamp'],
            "from_state": prev_state,
            "to_state": curr_state
        })

transitions_df = pd.DataFrame(transitions)

print("\nTotal state transitions:", len(transitions_df))
print("\nSample transitions:")
print(transitions_df.head(10))

print("="*70)
