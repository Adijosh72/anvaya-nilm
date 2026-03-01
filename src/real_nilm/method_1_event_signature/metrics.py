# metrics.py

def compute_energy_between(df, start_idx, end_idx):

    segment = df.iloc[start_idx:end_idx]

    energy_kwh = (
        (segment["power"] * segment["delta_sec"]).sum()
        / (3600 * 1000)
    )

    duration_sec = segment["delta_sec"].sum()

    return energy_kwh, duration_sec
