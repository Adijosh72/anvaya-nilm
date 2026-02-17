import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# Simulated Room Load (Replace with CSV later)
# --------------------------------------------------

power = []

for t in range(300):  # 5 minutes simulation (future-ready scaling)

    base = 100  # standby

    # TV always on
    base += 120

    # AC cycle (60-240 sec)
    if 60 <= t <= 240:
        base += 1100

    # Kettle spike (120-150 sec)
    if 120 <= t <= 150:
        base += 1800

    # Fridge cycle (every 70 sec)
    if t % 70 < 10:
        base += 180

    power.append(base)

df = pd.DataFrame({
    "time": range(len(power)),
    "power": power
})

# --------------------------------------------------
# Event Detection
# --------------------------------------------------

df["delta"] = df["power"].diff()

ON_THRESHOLD = 300
OFF_THRESHOLD = -300

events = df[
    (df["delta"] > ON_THRESHOLD) |
    (df["delta"] < OFF_THRESHOLD)
].copy()

events["type"] = events["delta"].apply(
    lambda x: "ON" if x > 0 else "OFF"
)

# --------------------------------------------------
# Appliance Classification Rules
# --------------------------------------------------

def classify(delta):
    delta = abs(delta)

    if delta > 1500:
        return "Kettle"
    elif 800 < delta < 1500:
        return "AC"
    elif 100 < delta < 400:
        return "Fridge"
    else:
        return "Unknown"

events["appliance"] = events["delta"].apply(classify)

# --------------------------------------------------
# Pair ON/OFF Events
# --------------------------------------------------

active = {}
energy_records = []

for idx, row in events.iterrows():

    appliance = row["appliance"]
    event_type = row["type"]
    time = row["time"]
    power_level = abs(row["delta"])

    if event_type == "ON":
        active[appliance] = {
            "start_time": time,
            "power": power_level
        }

    elif event_type == "OFF" and appliance in active:

        start_time = active[appliance]["start_time"]
        avg_power = active[appliance]["power"]

        duration = time - start_time
        energy = avg_power * duration / 3600  # Wh

        energy_records.append({
            "appliance": appliance,
            "start": start_time,
            "end": time,
            "duration_sec": duration,
            "estimated_energy_Wh": energy
        })

        del active[appliance]

energy_df = pd.DataFrame(energy_records)

# --------------------------------------------------
# Aggregate Appliance Summary
# --------------------------------------------------

summary = energy_df.groupby("appliance").agg({
    "duration_sec": "sum",
    "estimated_energy_Wh": "sum"
}).reset_index()

print("\n--- Appliance Runtime & Energy Summary ---")
print(summary)

# --------------------------------------------------
# Plot
# --------------------------------------------------

plt.figure()
plt.plot(df["time"], df["power"])
plt.title("Room-Level Appliance Energy Attribution")
plt.xlabel("Time")
plt.ylabel("Power (W)")
plt.show()
