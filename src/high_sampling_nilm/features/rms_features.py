# rms_features.py

import numpy as np


def compute_rms(signal):

    return np.sqrt(np.mean(signal ** 2))


def sliding_rms(signal, window_size):

    rms_values = []

    for i in range(0, len(signal) - window_size, window_size):
        window = signal[i:i+window_size]
        rms_values.append(compute_rms(window))

    return np.array(rms_values)