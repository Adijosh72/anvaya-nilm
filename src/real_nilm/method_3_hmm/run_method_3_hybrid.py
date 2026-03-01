# run_method_3_hybrid.py

import numpy as np
import pandas as pd

from utils import load_data, compute_total_energy
from hmm_model import train_hmm


CSV_PATH = "../../../data/smart_meter_data_202602201440.csv"


# -----------------------------
# 1️⃣ Train 2-State HMM (AC vs Non-AC)
# -----------------------------
def detect_ac(df):

    model, hidden_states = train_hmm(df["power"], n_states=2)

    df["hmm_state"] = hidden_states

    means = model.means_.flatten()
    ac_state = np.argmax(means)

    df["AC_ON"] = df["hmm_state"] == ac_state

    return df


# -----------------------------
# 2️⃣ Spike Detector (Kettle)
# -----------------------------
def detect_spikes(df, delta_threshold=800, max_duration_sec=120):

    df["delta_power"] = df["power"].diff().fillna(0)

    spike_indices = df.index[np.abs(df["delta_power"]) > delta_threshold]

    kettle_mask = np.zeros(len(df), dtype=bool)

    for idx in spike_indices:

        start = idx

        i = start
        duration = 0

        while i < len(df) and df["power"].iloc[i] > 1000:
            duration += df["delta_sec"].iloc[i]
            i += 1

            if duration > max_duration_sec:
                break

        if duration <= max_duration_sec:
            kettle_mask[start:i] = True

    df["KETTLE_ON"] = kettle_mask

    return df


# -----------------------------
# 3️⃣ Energy Breakdown
# -----------------------------
def compute_energy(df):

    df["energy_kwh"] = (df["power"] * df["delta_sec"]) / (3600 * 1000)

    total_energy = df["energy_kwh"].sum()

    ac_energy = df[df["AC_ON"] & ~df["KETTLE_ON"]]["energy_kwh"].sum()
    kettle_energy = df[df["KETTLE_ON"]]["energy_kwh"].sum()
    background_energy = total_energy - ac_energy - kettle_energy

    return total_energy, ac_energy, kettle_energy, background_energy


# -----------------------------
# Main
# -----------------------------
def run():

    df = load_data(CSV_PATH)

    total_energy = compute_total_energy(df)
    print("\nTotal Room Energy (kWh):", round(total_energy, 4))

    print("\nDetecting AC using HMM...")
    df = detect_ac(df)

    print("Detecting kettle spikes...")
    df = detect_spikes(df)

    total_energy, ac_energy, kettle_energy, background_energy = compute_energy(df)

    print("\nHybrid NILM Energy Breakdown:")
    print("AC Energy (kWh):", round(ac_energy, 4))
    print("Kettle Energy (kWh):", round(kettle_energy, 4))
    print("Background Energy (kWh):", round(background_energy, 4))

    print("\nEnergy %:")
    print("AC %:", round(ac_energy / total_energy * 100, 2))
    print("Kettle %:", round(kettle_energy / total_energy * 100, 2))
    print("Background %:", round(background_energy / total_energy * 100, 2))

    df.to_csv("method_3_hybrid_results.csv", index=False)

    print("\nSaved to method_3_hybrid_results.csv\n")


if __name__ == "__main__":
    run()
