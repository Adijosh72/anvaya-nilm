# run_method_3_semimarkov.py

import numpy as np
import pandas as pd

from utils import load_data, compute_total_energy
from hmm_model import train_hmm_multifeature

CSV_PATH = "../../../data/smart_meter_data_202602201440.csv"


def segment_states(df):
    df["segment_id"] = (df["state"] != df["state"].shift()).cumsum()
    return df


def apply_duration_model(df, model):

    means = model.means_
    power_means = means[:, 0]

    df = segment_states(df)

    appliance_labels = {}

    for seg_id, group in df.groupby("segment_id"):

        state = group["state"].iloc[0]
        mean_power = power_means[state]
        duration = group["delta_sec"].sum()

        # Overlap state
        if mean_power > 2500:
            label = "AC+KETTLE"

        # Low states
        elif mean_power < 300:
            label = "LIGHTS_OR_LOW"

        # Mid states (AC or kettle overlap band)
        else:
            if duration < 120:
                label = "KETTLE"
            elif duration > 300:
                label = "AC"
            else:
                label = "UNKNOWN_MID"

        appliance_labels[seg_id] = label

    df["appliance"] = df["segment_id"].map(appliance_labels)

    return df


def run():

    df = load_data(CSV_PATH)

    total_energy = compute_total_energy(df)
    print("\nTotal Room Energy (kWh):", round(total_energy, 4))

    print("\nTraining 4-state Multi-Feature HMM...")
    model, hidden_states = train_hmm_multifeature(df, n_states=4)

    df["state"] = hidden_states

    print("\nState Means [power, delta_power]:")
    print(model.means_)

    df = apply_duration_model(df, model)

    df["energy_kwh"] = (df["power"] * df["delta_sec"]) / (3600 * 1000)

    energy_summary = df.groupby("appliance")["energy_kwh"].sum()

    print("\nEnergy by Appliance (Semi-Markov HMM):")
    print(energy_summary.round(4))

    print("\nEnergy %:")
    print((energy_summary / total_energy * 100).round(2))

    df.to_csv("method_3_semimarkov_results.csv", index=False)

    print("\nSaved to method_3_semimarkov_results.csv\n")


if __name__ == "__main__":
    run()
