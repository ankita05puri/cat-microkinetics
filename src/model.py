"""
Microkinetic model: CO oxidation (mean-field) on a single site type.

State variables:
    theta = [theta_CO, theta_O, theta_CO2]
Site balance:
    theta_* = 1 - sum(theta)

Elementary steps (net rates returned by rates()):
  1) CO(g) + * <-> CO*
  2) O2(g) + 2* <-> 2O*
  3) CO* + O* <-> CO2* + *
  4) CO2* <-> CO2(g) + *

Notes / assumptions:
- Mean-field (no lateral interactions)
- Pressures can be dimensionless or in bar/atm, but must be consistent with prefactors A
- By default we allow a shared prefactor A, but step-specific prefactors are supported
"""

from __future__ import annotations

import numpy as np

K_B_EV_PER_K = 8.617333262e-5  # eV/K


def arrhenius(A: float, Ea_eV: float, T_K: float) -> float:
    """Arrhenius rate constant k = A * exp(-Ea / (kB*T))."""
    if T_K <= 0:
        raise ValueError("Temperature must be > 0 K.")
    return A * np.exp(-Ea_eV / (K_B_EV_PER_K * T_K))


def _theta_star(theta: np.ndarray) -> float:
    """Compute vacant site fraction theta_*."""
    return 1.0 - float(np.sum(theta))


def rates(theta, params):
    """
    Compute net rates (r1, r2, r3, r4) for the elementary steps.

    Parameters expected in `params`:
        PCO, PO2, PCO2 : floats
        T : temperature in K
        E1f,E1r,E2f,E2r,E3f,E3r,E4f,E4r : activation energies in eV
        A : default prefactor (1/s) (used if step-specific prefactors not provided)

    Optional:
        A1,A2,A3,A4 : step-specific prefactors (override A for each step)
    """
    theta = np.asarray(theta, dtype=float)
    theta_CO, theta_O, theta_CO2 = theta
    theta_star = _theta_star(theta)

    # Guardrails: keep model physically meaningful
    if theta_star < -1e-8:
        # This means the ODE solver stepped into an unphysical region.
        # Better to fail loudly than to silently clip and hide a bug.
        raise ValueError(
            f"Unphysical coverages: theta_* = {theta_star:.3e}. "
            "Check initial conditions / solver tolerances / parameter set."
        )
    theta_star = max(theta_star, 0.0)  # small numerical noise tolerance

    # Unpack operating conditions
    PCO = float(params["PCO"])
    PO2 = float(params["PO2"])
    PCO2 = float(params["PCO2"])
    T = float(params["T"])

    # Prefactors: allow step-specific overrides
    A_default = float(params["A"])
    A1 = float(params.get("A1", A_default))
    A2 = float(params.get("A2", A_default))
    A3 = float(params.get("A3", A_default))
    A4 = float(params.get("A4", A_default))

    # Rate constants (Arrhenius)
    k1f = arrhenius(A1, float(params["E1f"]), T)
    k1r = arrhenius(A1, float(params["E1r"]), T)

    k2f = arrhenius(A2, float(params["E2f"]), T)
    k2r = arrhenius(A2, float(params["E2r"]), T)

    k3f = arrhenius(A3, float(params["E3f"]), T)
    k3r = arrhenius(A3, float(params["E3r"]), T)

    k4f = arrhenius(A4, float(params["E4f"]), T)
    k4r = arrhenius(A4, float(params["E4r"]), T)

    # Step 1: CO adsorption/desorption
    r1f = k1f * PCO * theta_star
    r1r = k1r * theta_CO
    r1 = r1f - r1r

    # Step 2: O2 dissociative adsorption/recombination
    r2f = k2f * PO2 * (theta_star ** 2)
    r2r = k2r * (theta_O ** 2)
    r2 = r2f - r2r

    # Step 3: Surface reaction
    r3f = k3f * theta_CO * theta_O
    r3r = k3r * theta_CO2 * theta_star
    r3 = r3f - r3r

    # Step 4: CO2 desorption/readsorption
    r4f = k4f * theta_CO2
    r4r = k4r * PCO2 * theta_star
    r4 = r4f - r4r

    return r1, r2, r3, r4


def odes(t, theta, params):
    """
    ODE system for surface coverages.

    d(theta_CO)/dt  = r1 - r3
    d(theta_O)/dt   = 2*r2 - r3
    d(theta_CO2)/dt = r3 - r4
    """
    r1, r2, r3, r4 = rates(theta, params)

    dtheta_CO = r1 - r3
    dtheta_O = 2.0 * r2 - r3
    dtheta_CO2 = r3 - r4

    return [dtheta_CO, dtheta_O, dtheta_CO2]
