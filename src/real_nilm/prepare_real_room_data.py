# prepare_real_room_data.py
# Scan all devices and phases to find AC-like room

import pandas as pd

print("="*70)
print("SCANNING ALL DEVICES FOR AC SIGNATURE")
print("="*70)

CSV_FILE = "smart_meter_cleaned.csv"

df = pd.read_csv(CSV_FILE, low_memory=False)
df['timestamp'] = pd.to_datetime(df['createdAt'], format='mixed', errors='coerce')
df = df.dropna(subset=['timestamp'])

summary = []

for device in df['deviceId'].unique():
    for phase in df['phase'].unique():
        subset = df[(df['deviceId']==device) & (df['phase']==phase)]
        if len(subset) == 0:
            continue
        
        max_power = subset['power'].max()
        mean_power = subset['power'].mean()
        
        summary.append({
            'deviceId': device,
            'phase': phase,
            'samples': len(subset),
            'max_power': max_power,
            'mean_power': mean_power
        })

summary_df = pd.DataFrame(summary)
summary_df = summary_df.sort_values('max_power', ascending=False)

print(summary_df.head(10))

print("\nLook for max_power > 800W → That is AC room.")
print("="*70)
