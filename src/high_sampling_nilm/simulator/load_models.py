# load_models.py

import numpy as np
from config import *
from motor_models import induction_motor_current


def heater_current(t, on_time):

    if t < on_time:
        return 0, 0, 0

    I = HEATER_POWER / (np.sqrt(3) * LINE_VOLTAGE)

    w = 2 * np.pi * FREQUENCY

    Ia = I * np.sin(w * t)
    Ib = I * np.sin(w * t - 2*np.pi/3)
    Ic = I * np.sin(w * t + 2*np.pi/3)

    return Ia, Ib, Ic


def pump_current(t, start_time, fault=False):

    return induction_motor_current(
        t,
        start_time,
        PUMP_POWER,
        PUMP_PF,
        fault=False
    )