"""Pytest automated test suite for HPWM package and physical benchmarks."""

import pytest
import numpy as np
from pathlib import Path
import json

from hpwm.model import Parameters, field_equations, load_background


@pytest.fixture
def repo_root():
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def cert_data(repo_root):
    with open(repo_root / "data" / "VALIDATION_CERTIFICATE.json", "r", encoding="utf-8") as f:
        return json.load(f)


def test_bvp_residual_audit(repo_root):
    """Test 1: Euler-Lagrange BVP residuals strictly below 5e-9."""
    bg_file = repo_root / "data" / "background.npz"
    sol = load_background(bg_file)
    p = Parameters()

    r_grid = np.geomspace(1e-3, 25.0, 1000)
    y_grid = sol.sol(r_grid)
    yp_grid = sol.sol(r_grid, 1)
    rhs_grid = field_equations(r_grid, y_grid, p)

    residuals = np.abs(yp_grid - rhs_grid)
    max_res = np.max(residuals)
    median_res = np.median(residuals)

    assert max_res < 5e-9, f"Max residual {max_res} exceeded 5e-9"
    assert median_res < 1e-10, f"Median residual {median_res} exceeded 1e-10"


def test_vacuum_stability_threshold():
    """Test 2: Analytical vacuum stability threshold kappa_H_crit == 2.0."""
    p_subcrit = Parameters(kappa_H=1.9)
    p_crit = Parameters(kappa_H=2.0)
    p_supercrit = Parameters(kappa_H=2.1)

    assert p_subcrit.is_vacuum_stable() is True
    assert p_crit.is_vacuum_stable() is False
    assert p_supercrit.is_vacuum_stable() is False


def test_jost_determinant_machine_zero(cert_data):
    """Test 3: Jost determinant residuum at machine zero."""
    res = cert_data["audited_benchmarks"]["stage_2_linear_spectroscopy_K0"]["jost_det_residuum"]
    assert res < 1e-14, f"Jost residuum {res} too large"


def test_parity_conservation_leakage(cert_data):
    """Test 4: Spatial parity leakage strictly bounded below 1e-20."""
    p_leak = cert_data["audited_benchmarks"]["stage_5_symmetry_and_parity_protection"]["parity_leakage_shock_kappa50"]
    assert p_leak < 1e-20, f"Parity leakage {p_leak} exceeded 1e-20"


def test_alpha_anomaly_threshold_kinematics(cert_data):
    """Test 5: Relativistic threshold velocity vg/c < 0.30."""
    v_g = cert_data["audited_benchmarks"]["stage_3_kinematics_deep_space_K1"]["group_velocity_vg_over_c"]
    assert 0.28 < v_g < 0.30, f"Unexpected group velocity {v_g}"
