from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CSV_FILE = "../data/room_phase_1.csv"

def compute_metrics():
    df = pd.read_csv(CSV_FILE, low_memory=False)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed', errors='coerce')
    df = df.dropna(subset=['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)

    kmeans = KMeans(n_clusters=4, random_state=42)
    df['state'] = kmeans.fit_predict(df[['power']])
    centroids = kmeans.cluster_centers_.flatten()

    state_order = np.argsort(centroids)
    state_map = {state_order[i]: i for i in range(len(state_order))}
    df['state_rank'] = df['state'].map(state_map)

    AC_STATE = 2

    df['delta_sec'] = df['timestamp'].diff().dt.total_seconds().fillna(0)

    ac_runtime_hours = df[df['state_rank'] == AC_STATE]['delta_sec'].sum() / 3600
    ac_mean_power = centroids[state_order[AC_STATE]]
    ac_energy_kwh = (ac_mean_power * ac_runtime_hours) / 1000
    total_energy_kwh = (df['power'] * df['delta_sec']).sum() / (3600 * 1000)
    ac_contribution = (ac_energy_kwh / total_energy_kwh) * 100

    # --- AC Health Score ---
    df['date'] = df['timestamp'].dt.date
    ac_df = df[df['state_rank'] == AC_STATE]

    cycle_count = ((df['state_rank'].shift(1) != AC_STATE) & 
                   (df['state_rank'] == AC_STATE)).sum()

    power_std = ac_df['power'].std()

    health_score = 100
    if power_std > 200:
        health_score -= 20
    if cycle_count > 150:
        health_score -= 15

    status = "Normal"
    if health_score < 70:
        status = "Needs Attention"

    return {
        "ac_runtime_hours": round(ac_runtime_hours, 2),
        "ac_energy_kwh": round(ac_energy_kwh, 2),
        "total_energy_kwh": round(total_energy_kwh, 2),
        "ac_contribution_percent": round(ac_contribution, 2),
        "ac_mean_power": round(ac_mean_power, 2),
        "ac_cycles": int(cycle_count),
        "ac_health_score": int(health_score),
        "ac_status": status
    }

@app.get("/metrics")
def get_metrics():
    return compute_metrics()
@app.get("/timeseries")
def get_timeseries():
    df = pd.read_csv(CSV_FILE, low_memory=False)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed', errors='coerce')
    df = df.dropna(subset=['timestamp'])
    df = df.sort_values('timestamp')

    df['delta_sec'] = df['timestamp'].diff().dt.total_seconds().fillna(0)

    df['hour'] = df['timestamp'].dt.floor('H')

    hourly = df.groupby('hour').apply(
        lambda x: (x['power'] * x['delta_sec']).sum() / (3600 * 1000)
    ).reset_index(name='energy_kwh')

    hourly['hour'] = hourly['hour'].astype(str)

    return hourly.tail(48).to_dict(orient='records')

