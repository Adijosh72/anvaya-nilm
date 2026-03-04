# thd_features.py

import numpy as np
from high_sampling_nilm.simulator.config import FREQUENCY, SAMPLING_RATE


def compute_thd(signal):

    N = len(signal)
    fft_vals = np.fft.fft(signal)
    fft_mag = np.abs(fft_vals)

    freq = np.fft.fftfreq(N, 1 / SAMPLING_RATE)

    # Fundamental index
    fundamental_idx = np.argmin(np.abs(freq - FREQUENCY))
    fundamental_mag = fft_mag[fundamental_idx]

    # Harmonics (2x to 10x)
    harmonic_power = 0
    for h in range(2, 10):
        idx = np.argmin(np.abs(freq - h * FREQUENCY))
        harmonic_power += fft_mag[idx] ** 2

    thd = np.sqrt(harmonic_power) / fundamental_mag

    return thd