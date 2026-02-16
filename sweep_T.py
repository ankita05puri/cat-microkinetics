import numpy as np
import matplotlib.pyplot as plt

from src.simulate import simulate_to_steady_state
from src.model import rates


def run_sweep_T(params_base, T_values, t_final=80.0):
    """Return TOF array for a temperature sweep."""
    tofs = []
    for T in T_values:
        params = dict(params_base)
        params["T"] = float(T)

        sol, theta_ss, theta_star_ss = simulate_to_steady_state(params, t_final=t_final)
        r1, r2, r3, r4 = rates(theta_ss, params)
        tofs.append(float(r4))
    return np.array(tofs)


def fit_arrhenius(T_values, tofs):
    """
    Fit ln(TOF) vs 1/T and return:
    invT, lnTOF, slope m, intercept b, Ea_app (eV), Ea_app (kJ/mol)
    """
    tofs = np.array(tofs)
    mask = tofs > 0
    T_fit = T_values[mask]
    tof_fit = tofs[mask]

    invT = 1.0 / T_fit
    lnTOF = np.log(tof_fit)

    m, b = np.polyfit(invT, lnTOF, 1)

    kB_eV_per_K = 8.617333262e-5
    Ea_app_eV = -m * kB_eV_per_K
    Ea_app_kJmol = Ea_app_eV * 96.485

    return invT, lnTOF, m, b, Ea_app_eV, Ea_app_kJmol


def compare_barrier_attribution_for_regime(base_params, T_values, pco_value, delta_e=0.05):
    """
    For a given PCO, compute:
    - baseline Ea_app
    - Ea_app shifts when bumping E2f, E3f, E4f by +delta_e
    Save a compare plot for that regime.
    """
    params_regime = dict(base_params)
    params_regime["PCO"] = float(pco_value)

    cases = [
        ("baseline", {}),
        (f"E2f +{delta_e:.2f} (O2 dissociation)", {"E2f": params_regime["E2f"] + delta_e}),
        (f"E3f +{delta_e:.2f} (surface rxn)", {"E3f": params_regime["E3f"] + delta_e}),
        (f"E4f +{delta_e:.2f} (CO2 desorp)", {"E4f": params_regime["E4f"] + delta_e}),
    ]

    # plot compare: ln(TOF) vs 1/T with fit lines
    plt.figure()
    results = {}

    for label, overrides in cases:
        p = dict(params_regime)
        p.update(overrides)

        tofs = run_sweep_T(p, T_values)
        invT, lnTOF, m, b, Ea_eV, Ea_kJ = fit_arrhenius(T_values, tofs)

        results[label] = {"Ea_eV": Ea_eV, "Ea_kJmol": Ea_kJ}

        # data + fit
        plt.plot(invT, lnTOF, marker="o", linestyle="none", label=f"{label} data")
        xline = np.linspace(invT.min(), invT.max(), 200)
        plt.plot(xline, m * xline + b, linestyle="-", label=f"{label} fit (Ea={Ea_eV:.3f} eV)")

    plt.xlabel("1/T (1/K)")
    plt.ylabel("ln(TOF)")
    plt.title(f"Arrhenius compare (PCO={pco_value}): ln(TOF) vs 1/T")
    plt.legend(fontsize=8)
    plt.tight_layout()

    safe_pco = str(pco_value).replace(".", "p")
    outpath = f"figures/lnTOF_vs_invT_compare_PCO{safe_pco}.png"
    plt.savefig(outpath, dpi=300)
    plt.close()

    # Summary numbers for table
    Ea0 = results["baseline"]["Ea_eV"]
    summary = {
        "PCO": pco_value,
        "Ea_app_baseline_eV": Ea0,
        "dEa_E2f_eV": results[f"E2f +{delta_e:.2f} (O2 dissociation)"]["Ea_eV"] - Ea0,
        "dEa_E3f_eV": results[f"E3f +{delta_e:.2f} (surface rxn)"]["Ea_eV"] - Ea0,
        "dEa_E4f_eV": results[f"E4f +{delta_e:.2f} (CO2 desorp)"]["Ea_eV"] - Ea0,
        "plot": outpath,
    }

    return summary


def main():
    # ---- Base parameters (keep aligned with your project) ----
    base_params = {
        "PCO": 1.0,   # will be overridden per regime
        "PO2": 0.2,
        "PCO2": 0.0,

        "A": 1e3,  # 1/s

        # Activation energies (eV)
        "E1f": 0.35, "E1r": 0.60,
        "E2f": 0.55, "E2r": 1.00,
        "E3f": 0.70, "E3r": 0.90,
        "E4f": 0.70, "E4r": 1.20,
    }

    T_values = np.linspace(400, 900, 26)
    delta_e = 0.05

    # ---- Optional: keep baseline TOF vs T figure at PCO=1.0 ----
    tofs_baseline = run_sweep_T(base_params, T_values)
    plt.figure()
    plt.plot(T_values, tofs_baseline, marker="o")
    plt.xlabel("Temperature (K)")
    plt.ylabel("Steady-state TOF (net r4)")
    plt.title("TOF vs Temperature (Arrhenius microkinetics) — baseline")
    plt.tight_layout()
    plt.savefig("figures/tof_vs_T.png", dpi=300)
    plt.close()
    print("Saved: figures/tof_vs_T.png")

    # ---- Session 6: two regimes ----
    regimes = [0.1, 2.0]  # low CO, high CO

    summaries = []
    for pco in regimes:
        s = compare_barrier_attribution_for_regime(
            base_params=base_params,
            T_values=T_values,
            pco_value=pco,
            delta_e=delta_e,
        )
        summaries.append(s)
        print(f"Saved: {s['plot']}")

    # ---- Print a compact comparison table ----
    print("\nSession 6 summary (Ea_app attribution by regime):")
    print("PCO    Ea_app(eV)   ΔEa(E2f)    ΔEa(E3f)    ΔEa(E4f)")
    for s in summaries:
        print(
            f"{s['PCO']:<4}   "
            f"{s['Ea_app_baseline_eV']:<9.4f} "
            f"{s['dEa_E2f_eV']:+.4f}     "
            f"{s['dEa_E3f_eV']:+.4f}     "
            f"{s['dEa_E4f_eV']:+.4f}"
        )


if __name__ == "__main__":
    main()