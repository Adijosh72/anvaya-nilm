import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Dummy aggregate signal (from Influx read earlier)
# -----------------------------
aggregate_power = np.array([
    120, 120, 120, 350, 360, 355, 120, 120, 120
])

WINDOW_SIZE = 6
BASELINE = 120.0

X = []
y_true = []

# -----------------------------
# Sliding windows + target
# -----------------------------
for i in range(len(aggregate_power) - WINDOW_SIZE + 1):
    window = aggregate_power[i:i + WINDOW_SIZE]
    X.append(window)

    midpoint = window[WINDOW_SIZE // 2]
    appliance_power = max(0, midpoint - BASELINE)
    y_true.append(appliance_power)

X = np.array(X)
y_true = np.array(y_true)

# -----------------------------
# "Seq2Point-style" inference
# (rule-based placeholder)
# -----------------------------
y_pred = []

for window in X:
    midpoint = window[WINDOW_SIZE // 2]
    y_pred.append(max(0, midpoint - BASELINE))

y_pred = np.array(y_pred)

# -----------------------------
# Plot
# -----------------------------
plt.figure()
plt.plot(y_true, label="True Appliance Power", marker="o")
plt.plot(y_pred, label="Predicted Appliance Power", linestyle="--", marker="x")
plt.legend()
plt.title("Seq2Point-style NILM Output (Sanity Check)")
plt.xlabel("Window index")
plt.ylabel("Power (W)")
plt.tight_layout()
plt.show()

