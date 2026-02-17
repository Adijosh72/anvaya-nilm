import pandas as pd

df = pd.read_csv("smart_meter_cleaned.csv", low_memory=False)

# Proper mixed timestamp parsing
df['timestamp'] = pd.to_datetime(
    df['timestamp'],
    format='mixed',
    errors='coerce'
)

# Drop invalid
df = df.dropna(subset=['timestamp'])

# Pick one device + phase
device = df['deviceId'].iloc[0]
phase = df['phase'].iloc[0]

subset = df[(df['deviceId']==device) & (df['phase']==phase)]
subset = subset.sort_values('timestamp')

print("First 20 timestamps:")
print(subset['timestamp'].head(20))

subset['delta'] = subset['timestamp'].diff().dt.total_seconds()

print("\nDelta distribution:")
print(subset['delta'].describe())
