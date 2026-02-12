import numpy as np
import matplotlib.pyplot as plt

from src.simulate import simulate_to_steady_state
from src.model import rates


def main():
    base_params = {
        "PO2": 0.2,
        "PCO2": 0.0,
        
        "T": 600.0,
        "A": 1e13,
    
        "E1f": 0.20, "E1r": 0.60,
        "E2f": 0.80, "E2r": 1.00,
        "E3f": 0.70, "E3r": 0.90,
        "E4f": 0.40, "E4r": 1.20,
    }

    PCO_values = np.linspace(0.01, 3.0, 40)

    tofs = []
    thetaCO_ss = []
    thetaO_ss = []
    thetastar_ss = []

    for PCO in PCO_values:
        params = dict(base_params)
        params["PCO"] = float(PCO)

        sol, theta_ss, theta_star_ss = simulate_to_steady_state(params, t_final=80.0)

        r1, r2, r3, r4 = rates(theta_ss, params)
        tof = r4

        tofs.append(tof)
        thetaCO_ss.append(theta_ss[0])
        thetaO_ss.append(theta_ss[1])
        thetastar_ss.append(theta_star_ss)

    # Figure 3: TOF vs PCO
    plt.figure()
    plt.plot(PCO_values, tofs, marker="o")
    plt.xlabel("PCO (dimensionless)")
    plt.ylabel("Steady-state TOF (net r4)")
    plt.title("TOF vs CO Partial Pressure")
    plt.tight_layout()
    plt.savefig("figures/tof_vs_pco.png", dpi=300)
    plt.close()

    # Optional diagnostic plot: coverages vs PCO (useful for interpretation)
    plt.figure()
    plt.plot(PCO_values, thetaCO_ss, label="θ_CO")
    plt.plot(PCO_values, thetaO_ss, label="θ_O")
    plt.plot(PCO_values, thetastar_ss, label="θ_*")
    plt.xlabel("PCO (dimensionless)")
    plt.ylabel("Steady-state coverage")
    plt.title("Surface Coverage vs CO Partial Pressure")
    plt.legend()
    plt.tight_layout()
    plt.savefig("figures/coverage_vs_pco.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    main()
