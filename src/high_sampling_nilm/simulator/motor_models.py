    # motor_models.py

import numpy as np
from config import *


# ---------------------------------------------------
# 3-Phase Balanced Voltage Generator
# ---------------------------------------------------
def three_phase_voltage(t):

    w = 2 * np.pi * FREQUENCY

    V_peak = PHASE_VOLTAGE * np.sqrt(2)

    Va = V_peak * np.sin(w * t)
    Vb = V_peak * np.sin(w * t - 2 * np.pi / 3)
    Vc = V_peak * np.sin(w * t + 2 * np.pi / 3)

    return Va, Vb, Vc


# ---------------------------------------------------
# 3-Phase Induction Motor Current Model
# ---------------------------------------------------
def induction_motor_current(
    t,
    start_time,
    rated_power,
    pf,
    fault=False
):

    w = 2 * np.pi * FREQUENCY
    phi = np.arccos(pf)

    # Rated line current
    I_rated = rated_power / (np.sqrt(3) * LINE_VOLTAGE * pf)

    # ---------------------------------------------------
    # If motor not started
    # ---------------------------------------------------
    if t < start_time:
        return 0.0, 0.0, 0.0

    time_since_start = t - start_time

    # ---------------------------------------------------
    # Startup Inrush Model (0–0.6 sec)
    # ---------------------------------------------------
    if time_since_start < 0.6:
        inrush_multiplier = 6 * np.exp(-5 * time_since_start)
    else:
        inrush_multiplier = 1.0

    I_base = I_rated * inrush_multiplier

    # ---------------------------------------------------
    # Healthy Motor Current
    # ---------------------------------------------------
    Ia = I_base * np.sin(w * t - phi)
    Ib = I_base * np.sin(w * t - 2 * np.pi / 3 - phi)
    Ic = I_base * np.sin(w * t + 2 * np.pi / 3 - phi)

    # ---------------------------------------------------
    # Bearing Fault Injection
    # ---------------------------------------------------
    if fault:

        # Bearing defect frequency (sideband region)
        fault_freq = 180  # Hz typical bearing frequency

        # Amplitude modulation
        modulation = 1 + 0.15 * np.sin(2 * np.pi * fault_freq * t)

        # High-frequency vibration component
        high_freq_component = 0.05 * I_base * np.sin(2 * np.pi * 800 * t)

        # 3rd harmonic distortion
        harmonic_3rd = 0.08 * I_base * np.sin(3 * w * t)

        Ia = modulation * Ia + harmonic_3rd + high_freq_component
        Ib = modulation * Ib + harmonic_3rd + high_freq_component
        Ic = modulation * Ic + harmonic_3rd + high_freq_component

    return Ia, Ib, Ic