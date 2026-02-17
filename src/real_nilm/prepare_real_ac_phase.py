# prepare_real_ac_phase.py
# Extract specific device + phase for NILM

import pandas as pd

print("="*70)
print("PREPARING SPECIFIC PHASE FOR NILM")
print("="*70)

CSV_FILE = "smart_meter_cleaned.csv"

DEVICE_ID = "0000-FCFB-0ABF-1388"
PHASE = 1   # change between 1,2,3 to test each

df = pd.read_csv(CSV_FILE, low_memory=False)
df['timestamp'] = pd.to_datetime(df['createdAt'], format='mixed', errors='coerce')
df = df.dropna(subset=['timestamp'])

room_df = df[(df['deviceId']==DEVICE_ID) & (df['phase']==PHASE)]
room_df = room_df.sort_values('timestamp').reset_index(drop=True)

print(f"\nDevice: {DEVICE_ID}")
print(f"Phase: {PHASE}")
print(f"Samples: {len(room_df)}")

print("\nPower Stats:")
print(room_df['power'].describe())

room_df.to_csv(f"data/room_phase_{PHASE}.csv", index=False)

print(f"\nSaved to: data/room_phase_{PHASE}.csv")
print("="*70)
