import pandas as pd

CSV_FILE = "smart_meter_data_202602141620.csv"
OUTPUT_FILE = "smart_meter_cleaned.csv"

print("="*70)
print("CLEANING HARDWARE DATA")
print("="*70)

df = pd.read_csv(CSV_FILE, low_memory=False)

# Parse timestamp
df['timestamp'] = pd.to_datetime(df['createdAt'], errors='coerce')

print("Before cleaning:", len(df))

# Keep only realistic timestamps (2025 onward)
df = df[df['timestamp'] >= "2025-01-01"]

print("After removing corrupted timestamps:", len(df))

df = df.sort_values(['deviceId','phase','timestamp'])

df.to_csv(OUTPUT_FILE, index=False)

print("\nSaved cleaned file:", OUTPUT_FILE)
