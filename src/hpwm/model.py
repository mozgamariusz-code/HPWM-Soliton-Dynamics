"""Static HPWM background equations, parameters and diagnostics."""

from __future__ import annotations
from dataclasses import asdict, dataclass
from pathlib import Path
from types import SimpleNamespace
import numpy as np
from scipy.interpolate import PPoly


@dataclass(frozen=True)
class Parameters:
    """HPWM theory physical coupling constants and scales."""
    lambda_H: float = 1.0
    lambda_chi: float = 1.0
    kappa_H: float = 0.2
    v: float = 1.0
    u: float = 1.0
    zeta: float = 0.5
    f0_sq: float = 1.0
    e: float = 1.0
    mu_P: float = 0.5

    @property
    def mu_H_sq(self) -> float:
        return self.lambda_H * self.v**2 + 0.5 * self.kappa_H * self.u**2

    @property
    def u0_sq(self) -> float:
        return self.u**2 + 0.5 * self.kappa_H * self.v**2 / self.lambda_chi

    @property
    def delta_vacuum(self) -> float:
        return self.lambda_H * self.lambda_chi - self.kappa_H**2 / 4.0

    @property
    def f_vacuum_sq(self) -> float:
        return self.f0_sq + self.zeta * self.u**2

    def vacuum_mass_matrix(self) -> np.ndarray:
        return np.array(
            [
                [2.0 * self.lambda_H * self.v**2, self.kappa_H * self.u * self.v],
                [self.kappa_H * self.u * self.v, 2.0 * self.lambda_chi * self.u**2],
            ],
            dtype=float,
        )

    def vacuum_mass_eigenvalues(self) -> np.ndarray:
        return np.linalg.eigvalsh(self.vacuum_mass_matrix())

    def is_vacuum_stable(self) -> bool:
        return float(np.min(self.vacuum_mass_eigenvalues())) > 0.0

    def validate(self) -> None:
        if self.lambda_H <= 0 or self.lambda_chi <= 0:
            raise ValueError("Quartic scalar couplings must be positive.")
        if self.e <= 0:
            raise ValueError("The Skyrme coupling e must be positive.")
        if self.f0_sq <= 0:
            raise ValueError("f0_sq must be positive.")
        if self.zeta < 0:
            raise ValueError("This reproducibility scan assumes zeta >= 0.")
        if self.mu_P <= 0:
            raise ValueError("mu_P must be positive for a gapped orientation sector.")
        if self.delta_vacuum <= 0:
            raise ValueError("The mixed scalar vacuum is not a strict local minimum.")
        if np.min(self.vacuum_mass_eigenvalues()) <= 0:
            raise ValueError("The scalar vacuum contains a tachyonic direction.")

    def to_dict(self) -> dict[str, float]:
        data = asdict(self)
        data.update(
            mu_H_sq=self.mu_H_sq,
            u0_sq=self.u0_sq,
            delta_vacuum=self.delta_vacuum,
            f_vacuum_sq=self.f_vacuum_sq,
        )
        return data


def field_equations(r: np.ndarray, y: np.ndarray, p: Parameters) -> np.ndarray:
    """Radial Euler-Lagrange equations for F, chi and h in the B=1 hedgehog ansatz."""
    F, Fp, chi, chip, h, hp = y
    sin_f = np.sin(F)
    cos_f = np.cos(F)
    f_sq = p.f0_sq + p.zeta * chi**2

    coefficient = f_sq * r**2 + 2.0 * sin_f**2 / p.e**2
    coefficient_prime = (
        2.0 * p.zeta * chi * chip * r**2
        + 2.0 * f_sq * r
        + 4.0 * sin_f * cos_f * Fp / p.e**2
    )
    rhs_f = (
        2.0 * f_sq * sin_f * cos_f
        + 2.0 * sin_f * cos_f * Fp**2 / p.e**2
        + 2.0 * sin_f**3 * cos_f / (p.e**2 * r**2)
        + p.mu_P**2 * f_sq * r**2 * sin_f
    )
    F_pp = (rhs_f - coefficient_prime * Fp) / coefficient

    chi_pp = (
        -2.0 * chip / r
        + p.lambda_chi * chi * (chi**2 - p.u0_sq)
        + 0.5 * p.kappa_H * chi * h**2
        + p.zeta * chi * (Fp**2 + 2.0 * sin_f**2 / r**2)
        + 2.0 * p.zeta * p.mu_P**2 * chi * (1.0 - cos_f)
    )

    h_pp = (
        -2.0 * hp / r
        - p.mu_H_sq * h
        + p.lambda_H * h**3
        + 0.5 * p.kappa_H * chi**2 * h
    )

    return np.array([Fp, F_pp, chip, chi_pp, hp, h_pp])


def load_background(npz_path: str | Path) -> SimpleNamespace:
    """Load BVP solution spline construct from an npz file."""
    b = np.load(npz_path)
    spline = PPoly.construct_fast(b["c"], b["x"], axis=int(b["axis"]))
    return SimpleNamespace(sol=spline)
