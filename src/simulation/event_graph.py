import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from vmdpy import VMD

# -----------------------------
# Example event windows
# -----------------------------
event_windows = [
    np.array([120, 120, 120, 350, 360, 355, 120]),
    np.array([350, 360, 355, 120, 120, 120, 120])
]

# -----------------------------
# VMD Parameters
# -----------------------------
alpha = 2000
tau = 0.
K = 3
DC = 0
init = 1
tol = 1e-7

# -----------------------------
# Extract VMD features
# -----------------------------
event_features = []

for signal in event_windows:
    u, _, _ = VMD(signal, alpha, tau, K, DC, init, tol)

    # Feature: mean energy of each mode
    features = [np.mean(np.abs(mode)) for mode in u]
    event_features.append(features)

event_features = np.array(event_features)

print("Event Features:")
print(event_features)

# -----------------------------
# Build similarity graph
# -----------------------------
G = nx.Graph()

# Add nodes
for i in range(len(event_features)):
    G.add_node(i)

# Compute similarity (Euclidean distance)
for i in range(len(event_features)):
    for j in range(i+1, len(event_features)):
        distance = np.linalg.norm(event_features[i] - event_features[j])
        similarity = 1 / (1 + distance)
        G.add_edge(i, j, weight=similarity)

print("\nGraph edges with similarity weights:")
for edge in G.edges(data=True):
    print(edge)

# -----------------------------
# Visualize graph
# -----------------------------
pos = nx.spring_layout(G)
edges = G.edges(data=True)

weights = [edge[2]['weight'] * 5 for edge in edges]

plt.figure()
nx.draw(G, pos, with_labels=True, width=weights)
plt.title("Event Similarity Graph")
plt.show()
