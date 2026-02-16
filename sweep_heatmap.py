import numpy as np
import matplotlib.pyplot as plt

from src.simulate import simulate_to_steady_state
from src.model import rates


def run_sweep_T(params_base, T_values, t_final=80.0):
    tofs = []
    for T in T_values:
        params = dict(params_base)
        params["T"] = float(T)
        sol, theta_ss, theta_star_ss = simulate_to_steady_state(params, t_final=t_final)
        r1, r2, r3, r4 = rates(theta_ss, params)
        tofs.append(float(r4))
    return np.array(tofs)


def fit_Ea_app(T_values, tofs):
    tofs = np.array(tofs)
    mask = tofs > 0
    T_fit = T_values[mask]
    tof_fit = tofs[mask]

    invT = 1.0 / T_fit
    lnTOF = np.log(tof_fit)

    m, b = np.polyfit(invT, lnTOF, 1)
    kB_eV_per_K = 8.617333262e-5
    Ea_app_eV = -m * kB_eV_per_K
    return Ea_app_eV


def Ea_app_for_params(params, T_values):
    tofs = run_sweep_T(params, T_values)
    return fit_Ea_app(T_values, tofs)


def main():
    base_params = {
        "PCO": 1.0,   # overridden in sweep
        "PO2": 0.2,
        "PCO2": 0.0,
        "A": 1e3,

        "E1f": 0.35, "E1r": 0.60,
        "E2f": 0.55, "E2r": 1.00,
        "E3f": 0.70, "E3r": 0.90,
        "E4f": 0.70, "E4r": 1.20,
    }

    # Temperature range for Arrhenius fit (keep consistent with Session 6)
    T_values = np.linspace(400, 900, 26)

    # PCO grid for regime map
    PCO_values = np.linspace(0.05, 3.0, 20)

    delta = 0.05  # eV perturbation

    # Store: rows=barriers, cols=PCO
    barriers = ["E2f (O2 diss)", "E3f (surf rxn)", "E4f (CO2 des)"]
    dEa = np.zeros((len(barriers), len(PCO_values)))
    Ea0_list = []

    for j, PCO in enumerate(PCO_values):
        params = dict(base_params)
        params["PCO"] = float(PCO)

        Ea0 = Ea_app_for_params(params, T_values)
        Ea0_list.append(Ea0)

        # Perturb each barrier and recompute Ea_app
        params_E2 = dict(params); params_E2["E2f"] = params["E2f"] + delta
        params_E3 = dict(params); params_E3["E3f"] = params["E3f"] + delta
        params_E4 = dict(params); params_E4["E4f"] = params["E4f"] + delta

        Ea2 = Ea_app_for_params(params_E2, T_values)
        Ea3 = Ea_app_for_params(params_E3, T_values)
        Ea4 = Ea_app_for_params(params_E4, T_values)

        dEa[0, j] = Ea2 - Ea0
        dEa[1, j] = Ea3 - Ea0
        dEa[2, j] = Ea4 - Ea0

    Ea0_list = np.array(Ea0_list)

    # --- Plot A: Heatmap of ΔEa_app contributions ---
    plt.figure()
    im = plt.imshow(
        dEa,
        aspect="auto",
        origin="lower",
        extent=[PCO_values.min(), PCO_values.max(), 0, len(barriers)],
    )
    plt.colorbar(im, label="ΔEa_app (eV) for +0.05 eV perturbation")
    plt.yticks(np.arange(len(barriers)) + 0.5, barriers)
    plt.xlabel("PCO")
    plt.title("Regime map: barrier attribution vs CO partial pressure")
    plt.tight_layout()
    plt.savefig("figures/barrier_attribution_heatmap.png", dpi=300)
    plt.close()
    print("Saved: figures/barrier_attribution_heatmap.png")

    # --- Plot B (optional but recommended): Ea_app vs PCO ---
    plt.figure()
    plt.plot(PCO_values, Ea0_list, marker="o")
    plt.xlabel("PCO")
    plt.ylabel("Ea_app (eV)")
    plt.title("Apparent activation energy vs CO partial pressure")
    plt.tight_layout()
    plt.savefig("figures/Ea_app_vs_PCO.png", dpi=300)
    plt.close()
    print("Saved: figures/Ea_app_vs_PCO.png")


if __name__ == "__main__":
    main()