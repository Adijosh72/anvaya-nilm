# real_ac_health_analysis.py
# AC Health & Anomaly Detection

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

print("="*70)
print("AC HEALTH & ANOMALY ANALYSIS")
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

# AC state identified previously as state_rank 2
AC_STATE = 2

df['delta_sec'] = df['timestamp'].diff().dt.total_seconds()
df['delta_sec'] = df['delta_sec'].fillna(0)

# Identify AC segments
segments = []
current_state = df.iloc[0]['state_rank']
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

# Filter AC segments
ac_segments = segments_df[segments_df['state'] == AC_STATE]

if len(ac_segments) == 0:
    print("No AC segments found.")
    exit()

avg_runtime = ac_segments['duration_sec'].mean()
median_runtime = ac_segments['duration_sec'].median()
short_cycles = ac_segments[ac_segments['duration_sec'] < 120]
long_cycles = ac_segments[ac_segments['duration_sec'] > 3600]

print("\nAC Cycle Statistics:")
print(f"Total AC Cycles: {len(ac_segments)}")
print(f"Average Runtime: {round(avg_runtime/60,2)} minutes")
print(f"Median Runtime: {round(median_runtime/60,2)} minutes")

print(f"\nShort Cycles (<2 min): {len(short_cycles)}")
print(f"Long Cycles (>60 min): {len(long_cycles)}")

# Power stability check
ac_power_values = df[df['state_rank']==AC_STATE]['power']
power_std = ac_power_values.std()
power_mean = ac_power_values.mean()

print("\nAC Power Stability:")
print(f"Mean Power: {round(power_mean,2)} W")
print(f"Power Std Dev: {round(power_std,2)} W")

if power_std > 500:
    print("⚠️ High power variation detected.")
else:
    print("Power variation within normal range.")

print("="*70)
