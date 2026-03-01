# hmm_model.py

import numpy as np
from hmmlearn.hmm import GaussianHMM


# ----------------------------
# Single Feature HMM (Power)
# ----------------------------
def train_hmm(power_series, n_states=2):

    model = GaussianHMM(
        n_components=n_states,
        covariance_type="full",
        n_iter=200,
        random_state=42
    )

    X = power_series.values.reshape(-1, 1)

    model.fit(X)

    hidden_states = model.predict(X)

    return model, hidden_states


# ----------------------------
# Multi-Feature HMM (Power + ΔP)
# ----------------------------
def train_hmm_multifeature(df, n_states=4):

    df["delta_power"] = df["power"].diff().fillna(0)

    X = df[["power", "delta_power"]].values

    model = GaussianHMM(
        n_components=n_states,
        covariance_type="full",
        n_iter=300,
        random_state=42
    )

    model.fit(X)

    hidden_states = model.predict(X)

    return model, hidden_states
