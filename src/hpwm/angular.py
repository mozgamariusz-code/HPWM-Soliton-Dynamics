"""Angular momentum grand-spin decomposition and parity channels."""

from __future__ import annotations
import numpy as np
from .model import Parameters


class AngularTensor:
    """Asymptotic centrifugal barriers and channel kinetic tensors."""

    def __init__(self, p: Parameters, K: int):
        self.p = p
        self.K = K

    def centrifugal_barrier_pion(self, r: np.ndarray, channel: str) -> np.ndarray:
        f_inf_sq = self.p.f_vacuum_sq
        if channel == "longitudinal_a":
            # l = K + 1
            return f_inf_sq * (self.K + 1) * (self.K + 2) / (r**2)
        elif channel in ("transverse_electric_b", "transverse_magnetic_c"):
            # l = K
            return f_inf_sq * self.K * (self.K + 1) / (r**2)
        else:
            raise ValueError(f"Unknown channel: {channel}")

    def centrifugal_barrier_scalar(self, r: np.ndarray) -> np.ndarray:
        return self.K * (self.K + 1) / (r**2)


def parity_leakage(
    signal_natural: np.ndarray,
    signal_magnetic_c: np.ndarray
) -> float:
    """Compute parity leakage ratio P_leak = E_unnatural / E_natural."""
    e_unnatural = float(np.sum(np.abs(signal_magnetic_c)**2))
    e_natural = float(np.sum(np.abs(signal_natural)**2))
    if e_natural == 0.0:
        return 0.0
    return e_unnatural / e_natural
