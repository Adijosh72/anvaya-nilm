# fft_utils.py

import numpy as np


def compute_fft(signal, fs):

    N = len(signal)
    fft_vals = np.fft.fft(signal)
    freqs = np.fft.fftfreq(N, 1/fs)

    return freqs, np.abs(fft_vals)


def band_energy(freqs, magnitude, f_center, bandwidth=5):

    idx = np.where(
        (freqs >= f_center - bandwidth) &
        (freqs <= f_center + bandwidth)
    )[0]

    return np.sum(magnitude[idx] ** 2)


def harmonic_energy_features(signal, fs):

    freqs, mag = compute_fft(signal, fs)

    total_energy = np.sum(mag ** 2)

    # Fundamental
    fundamental = band_energy(freqs, mag, 50)

    # Harmonics
    h3 = band_energy(freqs, mag, 150)
    h5 = band_energy(freqs, mag, 250)

    # Sideband around 50Hz ± 180Hz (bearing mod freq)
    sideband1 = band_energy(freqs, mag, 50 + 180)
    sideband2 = band_energy(freqs, mag, 50 - 180)

    harmonic_sum = h3 + h5 + sideband1 + sideband2

    if total_energy == 0:
        return 0

    ratio = harmonic_sum / total_energy

    return ratio