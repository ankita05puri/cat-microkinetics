import numpy as np
import matplotlib.pyplot as plt

from src.simulate import simulate_to_steady_state
from src.model import rates


def main():
    base_params = {
        "PCO": 1.0,
        "PO2": 0.2,
        "PCO2": 0.0,

        "A": 1e3,  # 1/s

        # Activation energies (eV)
        "E1f": 0.35, "E1r": 0.60,
        "E2f": 0.55, "E2r": 1.00,
        "E3f": 0.70, "E3r": 0.90,
        "E4f": 0.70, "E4r": 1.20,
    }

    T_values = np.linspace(400, 900, 26)  # K
    tofs = []

    for T in T_values:
        params = dict(base_params)
        params["T"] = float(T)

        sol, theta_ss, theta_star_ss = simulate_to_steady_state(params, t_final=80.0)
        r1, r2, r3, r4 = rates(theta_ss, params)
        tofs.append(r4)

    tofs = np.array(tofs)

    # --- Plot 1: TOF vs T ---
    plt.figure()
    plt.plot(T_values, tofs, marker="o")
    plt.xlabel("Temperature (K)")
    plt.ylabel("Steady-state TOF (net r4)")
    plt.title("TOF vs Temperature (Arrhenius microkinetics)")
    plt.tight_layout()
    plt.savefig("figures/tof_vs_T.png", dpi=300)
    plt.close()
    print("Saved: figures/tof_vs_T.png")

    # --- Plot 2: ln(TOF) vs 1/T (Arrhenius plot) ---
    # Guard: ln only defined for positive TOF
    mask = tofs > 0
    T_fit = T_values[mask]
    tof_fit = tofs[mask]

    invT = 1.0 / T_fit
    lnTOF = np.log(tof_fit)

    # Linear fit: ln(TOF) = m*(1/T) + b
    m, b = np.polyfit(invT, lnTOF, 1)

    # Apparent activation energy from slope:
    # ln(rate) ~ -Ea/(kB*T) + const  => slope m = -Ea/kB
    kB_eV_per_K = 8.617333262e-5  # eV/K
    Ea_app_eV = -m * kB_eV_per_K

    # Convert to kJ/mol (1 eV = 96.485 kJ/mol)
    Ea_app_kJmol = Ea_app_eV * 96.485

    # Plot scatter + fit line
    plt.figure()
    plt.plot(invT, lnTOF, marker="o", linestyle="none", label="data")
    xline = np.linspace(invT.min(), invT.max(), 200)
    yline = m * xline + b
    plt.plot(xline, yline, label=f"fit: Ea_app = {Ea_app_eV:.3f} eV ({Ea_app_kJmol:.1f} kJ/mol)")
    plt.xlabel("1/T (1/K)")
    plt.ylabel("ln(TOF)")
    plt.title("Arrhenius-style plot: ln(TOF) vs 1/T")
    plt.legend()
    plt.tight_layout()
    plt.savefig("figures/lnTOF_vs_invT.png", dpi=300)
    plt.close()

    print("Saved: figures/lnTOF_vs_invT.png")
    print(f"Apparent Ea from fit: {Ea_app_eV:.4f} eV  ({Ea_app_kJmol:.2f} kJ/mol)")


if __name__ == "__main__":
    main()