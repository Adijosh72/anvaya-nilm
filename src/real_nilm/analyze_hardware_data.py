# analyze_hardware_data.py
# Structural validation of real hardware CSV (with timestamp fix)

import pandas as pd
import numpy as np

CSV_FILE = "smart_meter_cleaned.csv"

print("="*70)
print("HARDWARE DATA STRUCTURAL ANALYSIS (TIMESTAMP FIX)")
print("="*70)

df = pd.read_csv(CSV_FILE, low_memory=False)

print(f"\nTotal rows: {len(df):,}")
print("\nColumns:")
print(df.columns.tolist())

print("\nDevices:", df['deviceId'].nunique())
print("Phases:", df['phase'].nunique())

# 🔥 FIX TIMESTAMP PROPERLY

# Check if createdAt is numeric
if pd.api.types.is_numeric_dtype(df['createdAt']):
    # Detect seconds vs milliseconds
    max_val = df['createdAt'].max()

    if max_val > 10**12:
        print("\nDetected millisecond epoch timestamps")
        df['timestamp'] = pd.to_datetime(df['createdAt'], unit='ms')
    else:
        print("\nDetected second epoch timestamps")
        df['timestamp'] = pd.to_datetime(df['createdAt'], unit='s')

else:
    print("\nDetected string timestamps")
    df['timestamp'] = pd.to_datetime(df['createdAt'], errors='coerce')

# Drop invalid timestamps
df = df.dropna(subset=['timestamp'])

df = df.sort_values('timestamp')

print("\nTime range:")
print("Start:", df['timestamp'].min())
print("End  :", df['timestamp'].max())

duration = (df['timestamp'].max() - df['timestamp'].min()).total_seconds()
print("Duration (hours):", round(duration / 3600, 2))

# Sampling interval check per device+phase
print("\nSampling interval stats (seconds):")

df['delta_sec'] = df.groupby(['deviceId', 'phase'])['timestamp'].diff().dt.total_seconds()

print(df['delta_sec'].describe())

print("\nPower stats:")
print(df['power'].describe())

print("\nPer phase power summary:")
print(df.groupby('phase')['power'].describe())

print("\nMissing values:")
print(df[['voltage','current','power','pf']].isnull().sum())

print("\nAnalysis complete.")
