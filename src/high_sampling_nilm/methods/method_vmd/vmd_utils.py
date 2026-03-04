# vmd_utils.py

import numpy as np
from vmdpy import VMD


def perform_vmd(signal, alpha=2000, tau=0, K=5, DC=0, init=1, tol=1e-7):
    """
    Perform Variational Mode Decomposition
    """

    u, u_hat, omega = VMD(
        signal,
        alpha,
        tau,
        K,
        DC,
        init,
        tol
    )

    return u, omega


def mode_energy(mode):
    return np.sum(mode ** 2)


def compute_mode_energies(modes):
    energies = []
    for mode in modes:
        energies.append(mode_energy(mode))
    return np.array(energies)