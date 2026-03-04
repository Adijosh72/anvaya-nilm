# generate_3phase_dataset.py

import numpy as np
import pandas as pd

from config import *
from motor_models import three_phase_voltage, induction_motor_current
from load_models import heater_current, pump_current


def generate_dataset(fault=False, filename="healthy_dataset.csv"):

    time = np.linspace(0, DURATION, TOTAL_SAMPLES)

    data = []

    for t in time:

        Va, Vb, Vc = three_phase_voltage(t)

        # HVAC starts at 2s
        Ia_hvac, Ib_hvac, Ic_hvac = induction_motor_current(
            t, start_time=2, rated_power=HVAC_RATED_POWER,
            pf=HVAC_PF, fault=fault
        )

        # Pump starts at 8s
        Ia_pump, Ib_pump, Ic_pump = pump_current(t, start_time=8)

        # Heater turns on at 12s
        Ia_heat, Ib_heat, Ic_heat = heater_current(t, on_time=12)

        Ia = Ia_hvac + Ia_pump + Ia_heat
        Ib = Ib_hvac + Ib_pump + Ib_heat
        Ic = Ic_hvac + Ic_pump + Ic_heat

        Pa = Va * Ia
        Pb = Vb * Ib
        Pc = Vc * Ic

        data.append([
            t, Va, Vb, Vc, Ia, Ib, Ic,
            Pa, Pb, Pc,
            Pa + Pb + Pc
        ])

    columns = [
        "time",
        "Va", "Vb", "Vc",
        "Ia", "Ib", "Ic",
        "Pa", "Pb", "Pc",
        "P_total"
    ]

    df = pd.DataFrame(data, columns=columns)

    df.to_csv(filename, index=False)

    print(f"\nDataset saved as {filename}")


if __name__ == "__main__":

    print("Generating healthy dataset...")
    generate_dataset(fault=False, filename="healthy_5khz.csv")

    print("Generating bearing fault dataset...")
    generate_dataset(fault=True, filename="bearing_fault_5khz.csv")