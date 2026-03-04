# hybrid_utils.py

import numpy as np
from high_sampling_nilm.methods.method_envelope.envelope_utils import (
    bandpass_filter,
    compute_envelope,
    envelope_energy
)
from high_sampling_nilm.methods.method_fft_harmonic.fft_utils import (
    harmonic_energy_features
)
from high_sampling_nilm.methods.method_startup_transient.startup_utils import (
    detect_startup,
    startup_peak
)


LOWCUT = 150
HIGHCUT = 1200


def steady_state_health(segment, fs):

    total_energy = np.mean(segment ** 2)

    # Skip near-zero windows
    if total_energy < 1e-6:
        return None

    # Envelope component
    filtered = bandpass_filter(segment, LOWCUT, HIGHCUT, fs)
    envelope = compute_envelope(filtered)
    env_ratio = envelope_energy(envelope) / total_energy

    # Harmonic component
    harm_ratio = harmonic_energy_features(segment, fs)

    # Weighted fusion (Envelope stronger)
    health = 1 - (0.6 * env_ratio + 0.4 * harm_ratio)

    return health


def startup_health(time, signal, fs):

    idx = detect_startup(time, signal)

    if idx is None:
        return 1

    window = int(0.5 * fs)
    segment = signal[idx:idx + window]

    peak = startup_peak(segment)

    baseline_peak = 130
    peak_ratio = abs(peak - baseline_peak) / baseline_peak

    return 1 - peak_ratio