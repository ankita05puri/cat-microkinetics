import numpy as np
from scipy.integrate import solve_ivp

from .model import odes


def simulate_to_steady_state(params, t_final=50.0):
    """
    Runs the ODE system and returns:
    - sol: full time solution
    - theta_ss: steady-state coverages [theta_CO, theta_O, theta_CO2]
    - theta_star_ss: empty-site fraction at steady state
    """

    # Initial coverages
    y0 = np.array([0.0, 0.0, 0.0], dtype=float)  # [theta_CO, theta_O, theta_CO2]

    t_span = (0.0, t_final)
    t_eval = np.linspace(0.0, t_final, 800)

    sol = solve_ivp(
        fun=lambda t, y: odes(t, y, params),
        t_span=t_span,
        y0=y0,
        t_eval=t_eval,
        method="BDF",   # stiff-friendly solver
        rtol=1e-8,
        atol=1e-10,
    )

    theta_ss = sol.y[:, -1]
    theta_star_ss = 1.0 - theta_ss[0] - theta_ss[1] - theta_ss[2]

    return sol, theta_ss, theta_star_ss
