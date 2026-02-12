import numpy as np
import matplotlib.pyplot as plt

from src.simulate import simulate_to_steady_state
from src.model import rates


def main():
    base_params = {
        "PCO": 1.0,
        "PO2": 0.2,
        "PCO2": 0.0,

        "A": 1e13,  # 1/s

        # Activation energies (eV)
        "E1f": 0.20, "E1r": 0.60,
        "E2f": 0.80, "E2r": 1.00,
        "E3f": 0.70, "E3r": 0.90,
        "E4f": 0.40, "E4r": 1.20,
    }

    T_values = np.linspace(400, 900, 26)  # K
    tofs = []

    for T in T_values:
        params = dict(base_params)
        params["T"] = float(T)

        sol, theta_ss, theta_star_ss = simulate_to_steady_state(params, t_final=80.0)
        r1, r2, r3, r4 = rates(theta_ss, params)
        tofs.append(r4)

    plt.figure()
    plt.plot(T_values, tofs, marker="o")
    plt.xlabel("Temperature (K)")
    plt.ylabel("Steady-state TOF (net r4)")
    plt.title("TOF vs Temperature (Arrhenius microkinetics)")
    plt.tight_layout()
    plt.savefig("figures/tof_vs_T.png", dpi=300)
    plt.close()

    print("Saved: figures/tof_vs_T.png")


if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> 8a970ea (Session 4: Arrhenius kinetics + sweeps)
