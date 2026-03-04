# run_hybrid_method.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from high_sampling_nilm.methods.method_hybrid.hybrid_utils import (
    steady_state_health
)


WINDOW_SEC = 1
STEP_SEC = 0.5


def load_signal(filename):

    base_dir = os.path.dirname(__file__)
    simulator_path = os.path.join(base_dir, "..", "..", "simulator", filename)
    simulator_path = os.path.abspath(simulator_path)

    df = pd.read_csv(simulator_path)

    return df["time"].values, df["Ia"].values


def sliding_hybrid_health(time, signal, fs):

    window_samples = int(WINDOW_SEC * fs)
    step_samples = int(STEP_SEC * fs)

    health = []
    t_axis = []

    for start in range(0, len(signal) - window_samples, step_samples):

        segment = signal[start:start + window_samples]

        h = steady_state_health(segment, fs)

        if h is None:
            continue

        health.append(h)
        t_axis.append(time[start])

    return np.array(t_axis), np.array(health)


def evaluate(healthy, fault):

    print("\n--- Hybrid Health Metrics ---")
    print("Healthy Mean:", np.mean(healthy))
    print("Fault Mean:", np.mean(fault))
    print("Separation Gap:", np.mean(healthy) - np.mean(fault))
    print("Healthy Std:", np.std(healthy))
    print("Fault Std:", np.std(fault))


if __name__ == "__main__":

    time_h, signal_h = load_signal("healthy_5khz.csv")
    time_f, signal_f = load_signal("bearing_fault_5khz.csv")

    fs = int(len(time_h) / time_h[-1])

    t_h, health_h = sliding_hybrid_health(time_h, signal_h, fs)
    t_f, health_f = sliding_hybrid_health(time_f, signal_f, fs)

    evaluate(health_h, health_f)

    plt.figure(figsize=(10,5))
    plt.plot(t_h, health_h, label="Healthy")
    plt.plot(t_f, health_f, label="Fault", alpha=0.7)
    plt.legend()
    plt.xlabel("Time (s)")
    plt.ylabel("Hybrid Health Index")
    plt.title("Hybrid Envelope + FFT Health Index")
    plt.show()