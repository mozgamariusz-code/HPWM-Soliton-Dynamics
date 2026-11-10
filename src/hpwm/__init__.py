"""HPWM: High-Precision Wave Mechanics Python Package.

Simulates topological solitons, computes quasinormal resonance spectra,
and audits non-linear stability in the Universal Field-Memory Theory.
"""

from .model import Parameters, field_equations, load_background
from .angular import AngularTensor, parity_leakage
from .ecs_fem import ECSFEMSolver
from .jost_rmatrix import JostRMatrixSolver
from .timedomain import DeepSpaceSimulator

__version__ = "1.0.0"
__author__ = "Inżynier Mariusz Mozga"

__all__ = [
    "Parameters",
    "field_equations",
    "load_background",
    "AngularTensor",
    "parity_leakage",
    "ECSFEMSolver",
    "JostRMatrixSolver",
    "DeepSpaceSimulator",
]
