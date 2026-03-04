# startup_utils.py

import numpy as np


def detect_startup(time, signal, threshold_ratio=2):

    rms = np.sqrt(np.mean(signal**2))
    threshold = threshold_ratio * rms

    for i in range(len(signal)):
        if abs(signal[i]) > threshold:
            return i

    return None


def startup_peak(signal_segment):
    return np.max(np.abs(signal_segment))


def decay_time_constant(signal_segment, fs):

    peak = startup_peak(signal_segment)
    target = peak / np.e

    for i in range(len(signal_segment)):
        if abs(signal_segment[i]) <= target:
            return i / fs

    return None


def transient_energy(signal_segment):
    return np.mean(signal_segment ** 2)