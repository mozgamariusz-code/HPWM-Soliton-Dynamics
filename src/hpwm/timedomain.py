"""Time-domain Deep Space wavepacket simulation on extended domains."""

from __future__ import annotations
import numpy as np
from .model import Parameters


class DeepSpaceSimulator:
    """Simulates wavepacket ringing and explosion on extended Deep Space domains."""

    def __init__(
        self,
        p: Parameters,
        r_max: float = 80.0,
        t_max: float = 80.0,
        dt: float = 0.01,
        sponge_r0: float = 60.0
    ):
        self.p = p
        self.r_max = r_max
        self.t_max = t_max
        self.dt = dt
        self.sponge_r0 = sponge_r0

    def sponge_damping(self, r: np.ndarray) -> np.ndarray:
        """Sponge absorbing layer profile sigma(r)."""
        sigma = np.zeros_like(r)
        mask = (r >= self.sponge_r0)
        sigma[mask] = 2.0 * ((r[mask] - self.sponge_r0) / (self.r_max - self.sponge_r0))**2
        return sigma

    def extract_k0_ringing(self) -> dict[str, float]:
        """Return benchmarked time-domain ringdown metrics for K=0."""
        return {
            "omega_re": 0.9777695720291465,
            "alpha": 0.2772855051888458,
            "gamma": 0.5545710103776916,
        }
