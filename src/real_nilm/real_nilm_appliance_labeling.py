# real_nilm_appliance_labeling.py
# Automatic appliance labeling based on power + duration

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

print("="*70)
print("REAL NILM - MULTI-APPLIANCE LABELING")
print("="*70)

CSV_FILE = "data/room_phase_1.csv"

df = pd.read_csv(CSV_FILE, low_memory=False)
df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed', errors='coerce')
df = df.dropna(subset=['timestamp'])
df = df.sort_values('timestamp').reset_index(drop=True)

# Cluster states
kmeans = KMeans(n_clusters=4, random_state=42)
df['state'] = kmeans.fit_predict(df[['power']])

centroids = kmeans.cluster_centers_.flatten()
state_order = np.argsort(centroids)
state_map = {state_order[i]: i for i in range(len(state_order))}
df['state_rank'] = df['state'].map(state_map)

# Compute durations
df['delta_sec'] = df['timestamp'].diff().dt.total_seconds()
df['delta_sec'] = df['delta_sec'].fillna(0)

# Identify AC state (highest frequent long duration state)
AC_STATE = 2  # based on previous analysis

# Label appliances
def label_state(row):
    state = row['state_rank']
    power = row['power']
    
    if state == 0:
        return "Idle"
    elif state == AC_STATE:
        return "AC"
    elif power > 4000:
        return "Heavy Appliance"
    elif power > 1500:
        return "Medium Appliance"
    else:
        return "Other"

df['appliance'] = df.apply(label_state, axis=1)

# Compute energy by appliance
df['energy_kwh'] = (df['power'] * df['delta_sec']) / (3600 * 1000)

energy_summary = df.groupby('appliance')['energy_kwh'].sum()

print("\nEnergy Contribution by Appliance (kWh):")
print(energy_summary)

print("\nEnergy Contribution Percentage:")
total_energy = energy_summary.sum()
for app, val in energy_summary.items():
    print(f"{app}: {round((val/total_energy)*100,2)} %")

print("="*70)
