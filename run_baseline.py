import matplotlib.pyplot as plt

from src.simulate import simulate_to_steady_state
from src.model import rates


def main():
    params = {
        "PCO": 1.0,
        "PO2": 0.2,
        "PCO2": 0.0,
        "k1f": 5.0,  "k1r": 1.0,
        "k2f": 2.0,  "k2r": 0.2,
        "k3f": 1.0,  "k3r": 0.05,
        "k4f": 3.0,  "k4r": 0.0,
    }

    sol, theta_ss, theta_star_ss = simulate_to_steady_state(params)

    theta_CO, theta_O, theta_CO2 = sol.y
    theta_star = 1 - theta_CO - theta_O - theta_CO2

    # Steady-state TOF = net r4 at steady state
    r1, r2, r3, r4 = rates(theta_ss, params)
    tof_ss = r4

    print("Steady-state coverages [θ_CO, θ_O, θ_CO2] =", theta_ss)
    print("Steady-state θ_* =", theta_star_ss)
    print("Steady-state TOF =", tof_ss)

    # Figure: Coverages vs time
    plt.figure()
    plt.plot(sol.t, theta_CO, label="θ_CO")
    plt.plot(sol.t, theta_O, label="θ_O")
    plt.plot(sol.t, theta_CO2, label="θ_CO2")
    plt.plot(sol.t, theta_star, label="θ_*")
    plt.xlabel("time")
    plt.ylabel("coverage")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
