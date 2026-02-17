import numpy as np
import matplotlib.pyplot as plt
from vmdpy import VMD

# -----------------------------
# Example event-centric windows
# (copied from previous step)
# -----------------------------
event_windows = [
    np.array([120, 120, 120, 350, 360, 355, 120]),
    np.array([350, 360, 355, 120, 120, 120, 120])
]

# -----------------------------
# VMD Parameters
# -----------------------------
alpha = 2000       # bandwidth constraint
tau = 0.            # noise tolerance
K = 3               # number of modes
DC = 0
init = 1
tol = 1e-7

# -----------------------------
# Apply VMD to each event window
# -----------------------------
for idx, signal in enumerate(event_windows):
    u, u_hat, omega = VMD(
        signal,
        alpha,
        tau,
        K,
        DC,
        init,
        tol
    )

    plt.figure(figsize=(8, 4))
    for k in range(K):
        plt.plot(u[k], label=f"Mode {k+1}")

    plt.plot(signal, '--', color='black', label="Original", alpha=0.6)
    plt.title(f"VMD Decomposition - Event {idx+1}")
    plt.xlabel("Samples")
    plt.ylabel("Power (W)")
    plt.legend()
    plt.tight_layout()
    plt.show()
