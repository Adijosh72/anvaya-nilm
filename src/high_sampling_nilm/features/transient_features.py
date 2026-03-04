# transient_features.py

import numpy as np


def startup_peak(signal):

    return np.max(np.abs(signal))


def startup_decay_constant(signal, sampling_rate):

    peak = startup_peak(signal)

    threshold = peak / np.e

    for i in range(len(signal)):
        if abs(signal[i]) <= threshold:
            return i / sampling_rate

    return None