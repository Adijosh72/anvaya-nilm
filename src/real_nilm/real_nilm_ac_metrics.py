# real_nilm_ac_metrics.py
# Compute AC runtime, cycles, and energy from clustered states

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

print("="*70)
print("REAL NILM - AC RUNTIME & ENERGY METRICS")
print("="*70)

CSV_FILE = "data/room_phase_1.csv"

# Load data
df = pd.read_csv(CSV_FILE, low_memory=False)
df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed', errors='coerce')
df = df.dropna(subset=['timestamp'])
df = df.sort_values('timestamp').reset_index(drop=True)

# Cluster into 4 states
kmeans = KMeans(n_clusters=4, random_state=42)
df['state'] = kmeans.fit_predict(df[['power']])

centroids = kmeans.cluster_centers_.flatten()
state_order = np.argsort(centroids)

# Map states to sorted order
state_map = {state_order[i]: i for i in range(len(state_order))}
df['state_rank'] = df['state'].map(state_map)

# Print states
print("\nDetected States (sorted):")
for i in range(len(state_order)):
    print(f"State {i}: {round(centroids[state_order[i]],2)} W")

# Based on earlier result:
# AC plateau ≈ 2891W → usually state_rank = 2
AC_STATE = 2

# Compute time difference
df['delta_sec'] = df['timestamp'].diff().dt.total_seconds()
df['delta_sec'] = df['delta_sec'].fillna(0)

# AC runtime
ac_runtime_seconds = df[df['state_rank']==AC_STATE]['delta_sec'].sum()
ac_runtime_hours = ac_runtime_seconds / 3600

# AC mean power
ac_power_mean = centroids[state_order[AC_STATE]]

# AC energy
ac_energy_kwh = (ac_runtime_seconds * ac_power_mean) / (3600 * 1000)

# Total room energy
total_energy_kwh = (df['power'] * df['delta_sec']).sum() / (3600 * 1000)

# Count AC cycles (0 → AC_STATE transitions)
cycles = 0
for i in range(1, len(df)):
    if df.iloc[i-1]['state_rank'] != AC_STATE and df.iloc[i]['state_rank'] == AC_STATE:
        cycles += 1

print("\n" + "-"*50)
print(f"AC Mean Power: {round(ac_power_mean,2)} W")
print(f"AC Runtime: {round(ac_runtime_hours,2)} hours")
print(f"AC Energy: {round(ac_energy_kwh,2)} kWh")
print(f"Total Room Energy: {round(total_energy_kwh,2)} kWh")

if total_energy_kwh > 0:
    print(f"AC Contribution: {round((ac_energy_kwh/total_energy_kwh)*100,2)} %")

print(f"AC Cycles Detected: {cycles}")
print("-"*50)

print("\nAC NILM METRICS COMPLETE")
print("="*70)
