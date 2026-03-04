# run_vmd.py (Final Structured Version)

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from high_sampling_nilm.methods.method_vmd.vmd_utils import perform_vmd, compute_mode_energies


WINDOW_SEC = 1
STEP_SEC = 0.5
K_MODES = 5


def load_signal(filename):

    base_dir = os.path.dirname(__file__)
    simulator_path = os.path.join(base_dir, "..", "..", "simulator", filename)
    simulator_path = os.path.abspath(simulator_path)

    df = pd.read_csv(simulator_path)

    return df["time"].values, df["Ia"].values


def sliding_vmd_health(time, signal, sampling_rate):

    window_samples = int(WINDOW_SEC * sampling_rate)
    step_samples = int(STEP_SEC * sampling_rate)

    health_index = []
    time_axis = []

    for start in range(0, len(signal) - window_samples, step_samples):

        segment = signal[start:start + window_samples]

        modes, _ = perform_vmd(segment, K=K_MODES)

        energies = compute_mode_energies(modes)
        total_energy = np.sum(energies)

        if total_energy == 0:
            continue

        energy_ratios = energies / total_energy

        high_freq_energy = np.sum(energy_ratios[-2:])
        health_score = 1 - high_freq_energy

        health_index.append(health_score)
        time_axis.append(time[start])

    return np.array(time_axis), np.array(health_index)


def evaluate_separation(healthy, fault):

    healthy_mean = np.mean(healthy)
    fault_mean = np.mean(fault)

    healthy_std = np.std(healthy)
    fault_std = np.std(fault)

    separation_gap = healthy_mean - fault_mean

    print("\n--- VMD Health Metrics ---")
    print("Healthy Mean:", healthy_mean)
    print("Fault Mean:", fault_mean)
    print("Healthy Std:", healthy_std)
    print("Fault Std:", fault_std)
    print("Separation Gap:", separation_gap)

    return separation_gap


def analyze_dataset(filename):

    print("\nAnalyzing:", filename)

    time, signal = load_signal(filename)
    sampling_rate = int(len(time) / time[-1])

    t_axis, health = sliding_vmd_health(time, signal, sampling_rate)

    return t_axis, health


if __name__ == "__main__":

    t_h, health_h = analyze_dataset("healthy_5khz.csv")
    t_f, health_f = analyze_dataset("bearing_fault_5khz.csv")

    evaluate_separation(health_h, health_f)

    plt.figure(figsize=(10, 5))
    plt.plot(t_h, health_h, label="Healthy")
    plt.plot(t_f, health_f, label="Fault", alpha=0.7)
    plt.xlabel("Time (s)")
    plt.ylabel("Health Index")
    plt.legend()
    plt.title("Sliding Window VMD Health Index")
    plt.show()