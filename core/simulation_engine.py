import pandas as pd
import random

def simulate_room_24h(samples=5000):

    power = []
    pf_values = []

    # Appliance states
    ac_remaining = 0
    kettle_remaining = 0
    fridge_remaining = 0
    tv_on = False

    for t in range(samples):

        total_power = 80  # standby
        total_pf = 0.98

        # ----------------------------
        # Random TV usage (evening bias)
        # ----------------------------
        if 2000 < t < 3500:
            tv_on = True
        else:
            if random.random() < 0.01:
                tv_on = not tv_on

        if tv_on:
            total_power += 120

        # ----------------------------
        # AC logic
        # ----------------------------
        if ac_remaining <= 0 and random.random() < 0.01:
            ac_remaining = random.randint(200, 600)

        if ac_remaining > 0:
            total_power += 1100 + random.normalvariate(0, 30)
            total_pf = min(total_pf, 0.88)
            ac_remaining -= 1

        # ----------------------------
        # Kettle logic (short burst)
        # ----------------------------
        if kettle_remaining <= 0 and random.random() < 0.003:
            kettle_remaining = random.randint(60, 120)

        if kettle_remaining > 0:
            total_power += 1800 + random.normalvariate(0, 20)
            total_pf = min(total_pf, 0.99)
            kettle_remaining -= 1

        # ----------------------------
        # Fridge cycling
        # ----------------------------
        if fridge_remaining <= 0 and random.random() < 0.02:
            fridge_remaining = random.randint(40, 100)

        if fridge_remaining > 0:
            total_power += 180
            total_pf = min(total_pf, 0.85)
            fridge_remaining -= 1

        # ----------------------------
        # Add noise
        # ----------------------------
        total_power += random.normalvariate(0, 10)

        power.append(total_power)
        pf_values.append(total_pf)

    df = pd.DataFrame({
        "timestamp": range(len(power)),
        "power": power,
        "pf": pf_values
    })

    return df
