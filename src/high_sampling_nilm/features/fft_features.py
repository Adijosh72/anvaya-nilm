# fft_features.py

import numpy as np
from high_sampling_nilm.simulator.config import SAMPLING_RATE


def compute_fft(signal):

    N = len(signal)
    fft_vals = np.fft.fft(signal)
    fft_freq = np.fft.fftfreq(N, 1 / SAMPLING_RATE)

    return fft_freq, np.abs(fft_vals)


def dominant_frequencies(signal, top_n=5):

    freq, mag = compute_fft(signal)

    idx = np.argsort(mag)[-top_n:]

    return freq[idx], mag[idx]