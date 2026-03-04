# analyze_dataset.py

import pandas as pd
import numpy as np
import os

from high_sampling_nilm.features.rms_features import compute_rms
from high_sampling_nilm.features.fft_features import dominant_frequencies
from high_sampling_nilm.features.thd_features import compute_thd
from high_sampling_nilm.features.transient_features import startup_peak


def analyze_file(filename):

    # Get current file directory
    base_dir = os.path.dirname(__file__)

    # Build absolute path to simulator folder
    simulator_path = os.path.join(base_dir, "..", "simulator", filename)
    simulator_path = os.path.abspath(simulator_path)

    df = pd.read_csv(simulator_path)

    Ia = df["Ia"].values

    print("\nAnalyzing:", filename)

    print("RMS Current:", compute_rms(Ia))

    print("THD:", compute_thd(Ia))

    freqs, mags = dominant_frequencies(Ia)

    print("Dominant Frequencies:", freqs)

    print("Startup Peak:", startup_peak(Ia))


if __name__ == "__main__":

    analyze_file("healthy_5khz.csv")
    analyze_file("bearing_fault_5khz.csv")