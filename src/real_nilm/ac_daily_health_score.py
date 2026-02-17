# ac_daily_health_score.py
# AC Daily Health Score + Anomaly Detection (Robust Version)

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

print("="*70)
print("AC DAILY HEALTH SCORE & ANOMALY DETECTION")
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

AC_STATE = 2  # Identified earlier

df['delta_sec'] = df['timestamp'].diff().dt.total_seconds()
df['delta_sec'] = df['delta_sec'].fillna(0)

df['date'] = df['timestamp'].dt.date

daily_results = []

for date, group in df.groupby('date'):

    group = group.reset_index(drop=True)

    if len(group) < 2:
        continue

    segments = []
    current_state = group.iloc[0]['state_rank']
    duration = 0

    for i in range(1, len(group)):
        if group.iloc[i]['state_rank'] == current_state:
            duration += group.iloc[i]['delta_sec']
        else:
            segments.append({
                "state": current_state,
                "duration_sec": duration
            })
            current_state = group.iloc[i]['state_rank']
            duration = group.iloc[i]['delta_sec']

    if len(segments) == 0:
        continue

    segments_df = pd.DataFrame(segments)

    if 'state' not in segments_df.columns:
        continue

    ac_segments = segments_df[segments_df['state'] == AC_STATE]

    if len(ac_segments) == 0:
        continue

    cycles = len(ac_segments)
    avg_runtime = ac_segments['duration_sec'].mean() / 60
    short_cycles = len(ac_segments[ac_segments['duration_sec'] < 120])
    short_cycle_pct = (short_cycles / cycles) * 100

    ac_power = group[group['state_rank'] == AC_STATE]['power']
    power_std = ac_power.std()

    # ---- Health Score ----
    score = 100

    if short_cycle_pct > 30:
        score -= 20

    if cycles > 25:
        score -= 15

    if avg_runtime < 3:
        score -= 15

    if power_std > 300:
        score -= 10

    anomaly = "Normal"

    if score < 70:
        anomaly = "⚠️ Needs Attention"
    if score < 50:
        anomaly = "🔴 High Risk"

    daily_results.append({
        "date": date,
        "cycles": cycles,
        "avg_runtime_min": round(avg_runtime, 2),
        "short_cycle_%": round(short_cycle_pct, 2),
        "power_std": round(power_std, 2),
        "health_score": score,
        "status": anomaly
    })

daily_df = pd.DataFrame(daily_results)

print("\nDaily AC Health Summary:")
print(daily_df)

print("="*70)
