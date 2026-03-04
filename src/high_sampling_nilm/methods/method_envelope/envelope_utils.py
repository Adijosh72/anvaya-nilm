# envelope_utils.py

import numpy as np
from scipy.signal import butter, filtfilt, hilbert


def bandpass_filter(signal, lowcut, highcut, fs, order=4):

    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq

    b, a = butter(order, [low, high], btype='band')
    filtered = filtfilt(b, a, signal)

    return filtered


def compute_envelope(signal):

    analytic_signal = hilbert(signal)
    envelope = np.abs(analytic_signal)

    return envelope


def envelope_energy(envelope):

    return np.mean(envelope ** 2)