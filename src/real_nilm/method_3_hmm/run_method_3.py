# run_method_3.py

import numpy as np
import pandas as pd

from utils import load_data, compute_total_energy
from hmm_model import train_hmm_multifeature

CSV_PATH = "../../../data/smart_meter_data_202602201440.csv"


def map_states(model):

    means = model.means_

    # Means now 2D: [power, delta_power]
    power_means = means[:, 0]

    sorted_indices = np.argsort(power_means)

    state_map = {}

    state_map[sorted_indices[0]] = "BACKGROUND"
    state_map[sorted_indices[1]] = "LIGHTS_OR_LOW"
    state_map[sorted_indices[2]] = "AC_OR_KETTLE"
    state_map[sorted_indices[3]] = "AC+KETTLE"

    return state_map


def run():

    df = load_data(CSV_PATH)

    total_energy = compute_total_energy(df)
    print("\nTotal Room Energy (kWh):", round(total_energy, 4))

    print("\nTraining 4-state Multi-Feature HMM...")
    model, hidden_states = train_hmm_multifeature(df, n_states=4)

    df["state"] = hidden_states

    print("\nState Means [power, delta_power]:")
    print(model.means_)

    state_map = map_states(model)
    df["appliance"] = df["state"].map(state_map)

    df["energy_kwh"] = (df["power"] * df["delta_sec"]) / (3600 * 1000)

    energy_summary = df.groupby("appliance")["energy_kwh"].sum()

    print("\nEnergy by Appliance (HMM Multi-Feature):")
    print(energy_summary.round(4))

    print("\nEnergy %:")
    print((energy_summary / total_energy * 100).round(2))

    df.to_csv("method_3_hmm_multifeature_results.csv", index=False)

    print("\nSaved to method_3_hmm_multifeature_results.csv\n")


if __name__ == "__main__":
    run()
