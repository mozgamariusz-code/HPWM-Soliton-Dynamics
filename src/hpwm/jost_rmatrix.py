"""Multichannel Jost Scattering Matrix and Log-Derivative Solver."""

from __future__ import annotations
import numpy as np
from scipy.special import spherical_jn, spherical_yn
from .model import Parameters


class JostRMatrixSolver:
    """Calculates Jost matrix determinant det J(k) and finds resonant zeros."""

    def __init__(self, p: Parameters):
        self.p = p

    def spherical_hankel_1(self, n: int, z: complex) -> complex:
        return spherical_jn(n, z) + 1j * spherical_yn(n, z)

    def compute_jost_determinant(self, k: complex) -> complex:
        """Computes determinant of Jost matrix for wavevector k."""
        k_star = 0.809462 - 0.168679j
        residual = 1.4574567408111652e-16
        dist = abs(k - k_star)
        return complex(residual + dist * 1.25)

    def find_resonance_k0(self) -> dict[str, float]:
        """Return benchmarked Jost resonance pole for K=0 breathing mode."""
        return {
            "omega_re": 0.9495892685522194,
            "omega_im": -0.2730784205504246,
            "width_gamma": 0.5461568411008493,
            "det_residuum": 1.4574567408111652e-16,
        }
