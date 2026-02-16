import copy
import numpy as np
import matplotlib.pyplot as plt

from src.simulate import simulate_to_steady_state
from src.model import rates


def compute_tof(params):
    sol, theta_ss, theta_star_ss = simulate_to_steady_state(params, t_final=80.0)
    r1, r2, r3, r4 = rates(theta_ss, params)
    tof = r4
    return tof


def main():
    # Baseline parameters (use SAME as run_baseline.py)
    base_params = {
        "PCO": 1.0,
        "PO2": 0.2,
        "PCO2": 0.0,

        "T": 600.0,
        "A": 1e3,

        "E1f": 0.35, "E1r": 0.60,
        "E2f": 0.55, "E2r": 1.00,
        "E3f": 0.70, "E3r": 0.90,
        "E4f": 0.70, "E4r": 1.20,
    }

    # Finite difference perturbation
    delta_E = 0.01  # eV

    # kB in eV/K (same system as your Arrhenius)
    kB = 8.617333262e-5

    tof_base = compute_tof(base_params)
    if tof_base <= 0:
        raise ValueError(f"Baseline TOF must be > 0 for log; got {tof_base}")

    ln_tof_base = np.log(tof_base)

    steps = ["E1f", "E2f", "E3f", "E4f"]
    labels = {
        "E1f": "CO adsorption",
        "E2f": "O2 dissociation",
        "E3f": "Surface reaction",
        "E4f": "CO2 desorption",
    }

    drc_vals = {}

    for step in steps:
        params_new = copy.deepcopy(base_params)
        params_new[step] = params_new[step] - delta_E  # lower barrier slightly

        tof_new = compute_tof(params_new)
        if tof_new <= 0:
            raise ValueError(f"Perturbed TOF must be > 0 for log; {step} gave {tof_new}")

        ln_tof_new = np.log(tof_new)

        # DRC_i ≈ (d ln TOF) / ( - dEa / (kB*T) )
        drc = (ln_tof_new - ln_tof_base) / (delta_E / (kB * base_params["T"]))

        drc_vals[labels[step]] = drc

    # Print results
    print("Baseline TOF:", tof_base)
    print("DRC results:")
    for k, v in drc_vals.items():
        print(f"  {k:15s}: {v: .3f}")

    # Plot bar chart
    names = list(drc_vals.keys())
    values = [drc_vals[n] for n in names]

    plt.figure()
    plt.bar(names, values)
    plt.axhline(0.0)
    plt.ylabel("Degree of Rate Control (DRC)")
    plt.title("Degree of Rate Control at Baseline Conditions")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig("figures/drc_barplot.png", dpi=300)
    plt.close()

    print("Saved: figures/drc_barplot.png")


if __name__ == "__main__":
    main()