# run_fft_method.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from high_sampling_nilm.methods.method_fft_harmonic.fft_utils import harmonic_energy_features


WINDOW_SEC = 1
STEP_SEC = 0.5


def load_signal(filename):

    base_dir = os.path.dirname(__file__)
    simulator_path = os.path.join(base_dir, "..", "..", "simulator", filename)
    simulator_path = os.path.abspath(simulator_path)

    df = pd.read_csv(simulator_path)

    return df["time"].values, df["Ia"].values


def sliding_fft_health(time, signal, fs):

    window_samples = int(WINDOW_SEC * fs)
    step_samples = int(STEP_SEC * fs)

    health = []
    time_axis = []

    for start in range(0, len(signal) - window_samples, step_samples):

        segment = signal[start:start + window_samples]

        harmonic_ratio = harmonic_energy_features(segment, fs)

        health_score = 1 - harmonic_ratio

        health.append(health_score)
        time_axis.append(time[start])

    return np.array(time_axis), np.array(health)


def evaluate(healthy, fault):

    print("\n--- FFT Harmonic Health Metrics ---")

    h_mean = np.mean(healthy)
    f_mean = np.mean(fault)

    print("Healthy Mean:", h_mean)
    print("Fault Mean:", f_mean)
    print("Separation Gap:", h_mean - f_mean)

    print("Healthy Std:", np.std(healthy))
    print("Fault Std:", np.std(fault))


def analyze_dataset(filename):

    print("\nAnalyzing:", filename)

    time, signal = load_signal(filename)
    fs = int(len(time) / time[-1])

    return sliding_fft_health(time, signal, fs)


if __name__ == "__main__":

    t_h, health_h = analyze_dataset("healthy_5khz.csv")
    t_f, health_f = analyze_dataset("bearing_fault_5khz.csv")

    evaluate(health_h, health_f)

    plt.figure(figsize=(10,5))
    plt.plot(t_h, health_h, label="Healthy")
    plt.plot(t_f, health_f, label="Fault", alpha=0.7)
    plt.legend()
    plt.xlabel("Time (s)")
    plt.ylabel("Health Index")
    plt.title("Sliding FFT Harmonic Health Index")
    plt.show()