# real_nilm_state_clustering.py
# State-based NILM for low-resolution smart meter

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

print("="*70)
print("REAL NILM - STATE CLUSTERING")
print("="*70)

CSV_FILE = "data/room_phase_1.csv"

df = pd.read_csv(CSV_FILE, low_memory=False)
df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed', errors='coerce')
df = df.dropna(subset=['timestamp'])
df = df.sort_values('timestamp').reset_index(drop=True)

power_values = df['power'].values.reshape(-1, 1)

# Try clustering into 4 states
kmeans = KMeans(n_clusters=4, random_state=42)
df['state'] = kmeans.fit_predict(power_values)

centroids = sorted(kmeans.cluster_centers_.flatten())

print("\nDetected Power States (W):")
for c in centroids:
    print(round(c, 2))

# Plot with states
plt.figure(figsize=(12,5))
plt.scatter(df['timestamp'], df['power'], c=df['state'], s=5)
plt.title("Power States Clustering")
plt.xlabel("Time")
plt.ylabel("Power (W)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("\nState clustering complete.")
print("="*70)
