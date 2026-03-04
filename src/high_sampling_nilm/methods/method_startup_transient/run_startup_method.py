# run_startup_method.py

import os
import numpy as np
import pandas as pd

from high_sampling_nilm.methods.method_startup_transient.startup_utils import (
    detect_startup,
    startup_peak,
    decay_time_constant,
    transient_energy
)


ANALYSIS_WINDOW_SEC = 1


def load_signal(filename):

    base_dir = os.path.dirname(__file__)
    simulator_path = os.path.join(base_dir, "..", "..", "simulator", filename)
    simulator_path = os.path.abspath(simulator_path)

    df = pd.read_csv(simulator_path)

    return df["time"].values, df["Ia"].values


def analyze_startup(filename):

    print("\nAnalyzing:", filename)

    time, signal = load_signal(filename)

    fs = int(len(time) / time[-1])

    startup_idx = detect_startup(time, signal)

    if startup_idx is None:
        print("Startup not detected")
        return None

    window_samples = int(ANALYSIS_WINDOW_SEC * fs)

    segment = signal[startup_idx:startup_idx + window_samples]

    peak = startup_peak(segment)
    decay = decay_time_constant(segment, fs)
    energy = transient_energy(segment)

    print("Startup Peak:", peak)
    print("Decay Time Constant (s):", decay)
    print("Transient Energy:", energy)

    return peak, decay, energy


if __name__ == "__main__":

    healthy_metrics = analyze_startup("healthy_5khz.csv")
    fault_metrics = analyze_startup("bearing_fault_5khz.csv")

    print("\n--- Startup Comparison ---")
    print("Healthy:", healthy_metrics)
    print("Fault:", fault_metrics)