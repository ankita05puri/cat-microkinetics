# Microkinetic model definitions

import numpy as np

def arrhenius(A, Ea_eV, T_K):
    kB_eV_per_K = 8.617333262e-5  # eV/K
    return A * np.exp(-Ea_eV / (kB_eV_per_K * T_K))
    
def rates(theta, params):
    """
    Compute net rates for each elementary step.
    theta = [theta_CO, theta_O, theta_CO2]
    params = dictionary of rate constants and pressures
    """

    theta_CO, theta_O, theta_CO2 = theta
    theta_star = 1.0 - theta_CO - theta_O - theta_CO2

    # Prevent negative star coverage during solver exploration
    theta_star = max(theta_star, 0.0)

    # Unpack parameters
    PCO = params["PCO"]
    PO2 = params["PO2"]
    PCO2 = params["PCO2"]

    A = params["A"]
    T = params["T"]
    
    k1f = arrhenius(A, params["E1f"], T)
    k1r = arrhenius(A, params["E1r"], T)
    k2f = arrhenius(A, params["E2f"], T)
    k2r = arrhenius(A, params["E2r"], T)
    k3f = arrhenius(A, params["E3f"], T)
    k3r = arrhenius(A, params["E3r"], T)
    k4f = arrhenius(A, params["E4f"], T)
    k4r = arrhenius(A, params["E4r"], T)

    # Step 1: CO adsorption
    r1f = k1f * PCO * theta_star
    r1r = k1r * theta_CO
    r1 = r1f - r1r

    # Step 2: O2 dissociative adsorption
    r2f = k2f * PO2 * theta_star**2
    r2r = k2r * theta_O**2
    r2 = r2f - r2r

    # Step 3: Surface reaction
    r3f = k3f * theta_CO * theta_O
    r3r = k3r * theta_CO2 * theta_star
    r3 = r3f - r3r

    # Step 4: CO2 desorption
    r4f = k4f * theta_CO2
    r4r = k4r * PCO2 * theta_star
    r4 = r4f - r4r

    return r1, r2, r3, r4


def odes(t, theta, params):
    """
    Governing differential equations for surface coverages.
    """

    r1, r2, r3, r4 = rates(theta, params)

    dtheta_CO = r1 - r3
    dtheta_O = 2.0 * r2 - r3
    dtheta_CO2 = r3 - r4

    return [dtheta_CO, dtheta_O, dtheta_CO2]
