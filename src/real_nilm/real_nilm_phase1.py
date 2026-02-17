# real_nilm_phase1.py
# Real NILM event detection on Phase 1 (Room with high spikes)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("="*70)
print("REAL NILM - PHASE 1 (PROFESSIONAL VERSION)")
print("="*70)

CSV_FILE = "data/room_phase_1.csv"
THRESHOLD = 60   # Correct threshold for 15-second resolution

# Load data
df = pd.read_csv(CSV_FILE, low_memory=False)

# Parse timestamp safely
df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed', errors='coerce')
df = df.dropna(subset=['timestamp'])

df = df.sort_values('timestamp').reset_index(drop=True)

print(f"\nLoaded {len(df)} samples")

print("\nPower Stats:")
print(df['power'].describe())

# Remove large time gaps (>5 minutes)
df['delta_sec'] = df['timestamp'].diff().dt.total_seconds()
df = df[(df['delta_sec'].isna()) | (df['delta_sec'] < 300)]
df = df.reset_index(drop=True)

# Calculate power step changes
df['delta'] = df['power'].diff()

# Show delta distribution
print("\nDelta percentiles:")
print(np.percentile(abs(df['delta'].dropna()), [50, 75, 90, 95, 99]))

# Event detection
events = []

for i in range(1, len(df)):
    delta = df.iloc[i]['delta']
    
    if delta > THRESHOLD:
        events.append({
            'timestamp': df.iloc[i]['timestamp'],
            'type': 'ON',
            'delta': delta,
            'power_after': df.iloc[i]['power']
        })
        
    elif delta < -THRESHOLD:
        events.append({
            'timestamp': df.iloc[i]['timestamp'],
            'type': 'OFF',
            'delta': abs(delta),
            'power_after': df.iloc[i]['power']
        })

events_df = pd.DataFrame(events)

print("\n" + "-"*50)
print(f"Total Events Detected: {len(events_df)}")
print(f"ON Events:  {len(events_df[events_df['type']=='ON'])}")
print(f"OFF Events: {len(events_df[events_df['type']=='OFF'])}")
print("-"*50)

if len(events_df) > 0:
    print("\nSample Events:")
    print(events_df.head(10).to_string(index=False))

# Plot power signal
plt.figure()
plt.plot(df['timestamp'], df['power'])
plt.title("Phase 1 Real Power Signal")
plt.xlabel("Time")
plt.ylabel("Power (W)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("\nPhase 1 NILM Detection Complete.")
print("="*70)
