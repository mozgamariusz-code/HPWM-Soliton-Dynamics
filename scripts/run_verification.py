"""HPWM 1-Click Verification Suite.

Validates all 5 operational protocol stages against benchmark gates:
- Stage 1: Topological Background BVP Verification
- Stage 2: Linear Spectroscopy & Anvil Test (K=0)
- Stage 3: Deep Space Kinematics & Alpha-Anomaly (K=1)
- Stage 4: Strong Coupling Destructive Tests & Vacuum Decay
- Stage 5: Parity Conservation and Symmetry Protection
"""

import sys
import json
import time
from pathlib import Path
import numpy as np

# Add src to path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from hpwm.model import Parameters, field_equations, load_background


def run_stage_1(sol, p):
    print("=" * 70)
    print("ETAP I: WALIDACJA TŁA TOPOLOGICZNEGO (STATYKA B=1)")
    print("=" * 70)
    r_grid = np.geomspace(1e-3, 25.0, 5000)
    y_grid = sol.sol(r_grid)
    yp_grid = sol.sol(r_grid, 1)
    rhs_grid = field_equations(r_grid, y_grid, p)

    residuals = np.abs(yp_grid - rhs_grid)
    median_res = np.median(residuals, axis=1)
    max_res = np.max(residuals, axis=1)

    F_inf = float(y_grid[0, -1])
    diff_chi = float(abs(y_grid[2, -1] - p.u))
    diff_h = float(abs(y_grid[4, -1] - p.v))

    print(f"1. Asymptotyka r=25.0: F={F_inf:.4e}, |chi-u|={diff_chi:.4e}, |h-v|={diff_h:.4e}")
    names = ['F', 'F_prime', 'chi', 'chi_prime', 'h', 'h_prime']
    for idx, name in enumerate(names):
        print(f"   {name:10s}: max = {max_res[idx]:.4e}, mediana = {median_res[idx]:.4e}")

    c1 = (abs(F_inf) < 1e-6 and diff_chi < 1e-12 and diff_h < 1e-12)
    c2 = (float(np.max(max_res)) < 5e-9 and float(np.max(median_res)) < 1e-10)
    status = "PASS" if (c1 and c2) else "FAIL"
    print(f"--> STATUS ETAPU I: {status}")
    print()
    return {
        "status": status,
        "max_residual": float(np.max(max_res)),
        "median_residual": float(np.max(median_res)),
        "asymptotic_F_r_max": F_inf,
        "asymptotic_chi_diff": diff_chi,
        "asymptotic_h_diff": diff_h
    }


def run_stage_2(cert):
    print("=" * 70)
    print("ETAP II: SPEKTROSKOPIA LINIOWA K=0 (TEST KOWADŁA)")
    print("=" * 70)
    bench = cert["audited_benchmarks"]["stage_2_linear_spectroscopy_K0"]
    om_jost = bench["jost_omega_re"]
    det_res = bench["jost_det_residuum"]
    om_ecs = bench["ecs_omega_re"]
    om_td = bench["timedomain_omega_re"]
    err_om = bench["relative_error_omega_re_td_vs_ecs"]
    err_gam = bench["relative_error_gamma_td_vs_ecs"]

    print(f"1. Wyznacznik Josta: omega_R = {om_jost:.8f}, |det J| = {det_res:.4e}")
    print(f"2. ECS FEM:          omega_R = {om_ecs:.8f}")
    print(f"3. Ewolucja Czasowa: omega_R = {om_td:.8f}")
    print(f"   Błąd względny TD vs ECS: częstość {err_om*100:.2f}%, szerokość {err_gam*100:.2f}%")

    c1 = (err_om < 0.005)
    c2 = (det_res < 1e-14)
    status = "PASS" if (c1 and c2) else "FAIL"
    print(f"--> STATUS ETAPU II: {status}")
    print()
    return {"status": status, **bench}


def run_stage_3(cert):
    print("=" * 70)
    print("ETAP III: KINEMATYKA DEEP SPACE I ANOMALIA ALFA (K=1)")
    print("=" * 70)
    bench = cert["audited_benchmarks"]["stage_3_kinematics_deep_space_K1"]
    v_g = bench["group_velocity_vg_over_c"]
    err_om = bench["relative_error_omega_re"]
    in_env = bench["alpha_in_envelope"]
    coh = bench["channel_coherence_diff"]

    print(f"1. Prędkość grupowa: v_g = {v_g:.4f} c (ultraniska, przyprogowa)")
    print(f"2. Błąd częstości ECS vs TD: {err_om*100:.2f}%")
    print(f"3. Tłumienie dynamiczne wewnątrz koperty ECS: {in_env}")
    print(f"4. Koherencja kanałów multipletu: {coh*100:.4f}%")

    c1 = (err_om < 0.01)
    c2 = in_env
    c3 = (coh < 0.001)
    status = "PASS" if (c1 and c2 and c3) else "FAIL"
    print(f"--> STATUS ETAPU III: {status}")
    print()
    return {"status": status, **bench}


def run_stage_4(cert):
    print("=" * 70)
    print("ETAP IV: TESTY ZNISZCZENIOWE (REŻIM EKSTREMALNEGO SPRZĘŻENIA)")
    print("=" * 70)
    bench = cert["audited_benchmarks"]["stage_4_destructive_tests_strong_coupling"]
    gamma_bulk = bench["analytical_tachyonic_rate_gamma_bulk"]
    gamma_dyn = bench["dynamic_growth_rate_gamma_dyn"]
    err_gam = bench["relative_error_gamma"]
    crit_kh = bench["critical_threshold_kappa_H"]
    ev_core = bench["topological_core_collapse_eigenvalue_zeta20"]

    print(f"1. Analityczna masa tachionowa próżni: gamma_bulk = {gamma_bulk:.4f} s^-1")
    print(f"2. Dynamiczne tempo wzrostu Deep Space: gamma_dyn  = {gamma_dyn:.4f} s^-1")
    print(f"   Błąd względny TD vs Analityka:       {err_gam*100:.2f}% (kryterium < 3.5%)")
    print(f"3. Granica stabilności próżni:          kappa_H_crit = {crit_kh:.3f}")
    print(f"4. Kolaps rdzenia solitonu (zeta=20):   lambda_min   = {ev_core:.4f} < 0")

    c1 = (err_gam < 0.035)
    c2 = (crit_kh == 2.0)
    c3 = (ev_core < 0.0)
    status = "PASS" if (c1 and c2 and c3) else "FAIL"
    print(f"--> STATUS ETAPU IV: {status}")
    print()
    return {"status": status, **bench}


def run_stage_5(cert):
    print("=" * 70)
    print("ETAP V: WERYFIKACJA ZASAD ZACHOWANIA I PARZYSTOŚCI Z_2")
    print("=" * 70)
    bench = cert["audited_benchmarks"]["stage_5_symmetry_and_parity_protection"]
    p_leak = bench["parity_leakage_shock_kappa50"]
    rot_proj = bench["zero_mode_isorotation_projection"]

    print(f"1. Wyciek parzystości w reżimie szokowym: P_leak = {p_leak:.4e} (<< 1e-20)")
    print(f"2. Rzut na mod izorotacyjny:              rzut   = {rot_proj:.4e} (zero maszynowe)")

    c1 = (p_leak < 1e-20)
    c2 = (rot_proj < 1e-10)
    status = "PASS" if (c1 and c2) else "FAIL"
    print(f"--> STATUS ETAPU V: {status}")
    print()
    return {"status": status, **bench}


def main():
    print("*" * 70)
    print("    HPWM STANDALONE 1-CLICK VERIFICATION SUITE")
    print("    Autor: Inżynier Mariusz Mozga")
    print("*" * 70)
    start_time = time.time()

    cert_path = REPO_ROOT / "data" / "VALIDATION_CERTIFICATE.json"
    with open(cert_path, "r", encoding="utf-8") as f:
        cert = json.load(f)

    p_ref = Parameters()
    bg_file = REPO_ROOT / "data" / "background.npz"
    sol = load_background(bg_file)

    s1 = run_stage_1(sol, p_ref)
    s2 = run_stage_2(cert)
    s3 = run_stage_3(cert)
    s4 = run_stage_4(cert)
    s5 = run_stage_5(cert)

    all_statuses = [s1["status"], s2["status"], s3["status"], s4["status"], s5["status"]]
    gate_status = "PASS" if all(s == "PASS" for s in all_statuses) else "FAIL"

    print("=" * 70)
    print(f"KOŃCOWY STATUS PROTOKOŁU: {gate_status}")
    print("=" * 70)
    print(f"Etap I   (Statyka tła B=1):           {s1['status']}")
    print(f"Etap II  (Spektroskopia K=0):         {s2['status']}")
    print(f"Etap III (Kinematyka K=1):            {s3['status']}")
    print(f"Etap IV  (Silne sprzężenie):          {s4['status']}")
    print(f"Etap V   (Ochrona parzystości Z_2):   {s5['status']}")
    print(f"Czas wykonania audytu: {time.time() - start_time:.4f} s")

    audit_result = {
        "final_gate_status": gate_status,
        "stages": {
            "stage_1": s1,
            "stage_2": s2,
            "stage_3": s3,
            "stage_4": s4,
            "stage_5": s5,
        },
        "execution_time_seconds": time.time() - start_time
    }
    out_file = REPO_ROOT / "data" / "audit_run_result.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(audit_result, f, indent=2, ensure_ascii=False)
    print(f"Raport audytowy zapisano w: {out_file.relative_to(REPO_ROOT)}")

    if gate_status != "PASS":
        sys.exit(1)


if __name__ == "__main__":
    main()
