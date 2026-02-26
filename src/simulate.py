import numpy as np
from scipy.integrate import solve_ivp

from .model import odes


def simulate_to_steady_state(params, t_final=50.0):
    """
    Integrate coverages to (approx) steady state.

    Returns:
      sol: full time solution
      theta_ss: last-time coverages [theta_CO, theta_O, theta_CO2]
      theta_star_ss: empty-site fraction at last time
    """
    y0 = np.array([0.0, 0.0, 0.0], dtype=float)

    def run(t_end):
        t_span = (0.0, float(t_end))
        t_eval = np.linspace(0.0, float(t_end), 800)
        sol = solve_ivp(
            fun=lambda t, y: odes(t, y, params),
            t_span=t_span,
            y0=y0,
            t_eval=t_eval,
            method="BDF",
            rtol=1e-8,
            atol=1e-10,
        )
        if not sol.success:
            raise RuntimeError(f"ODE solver failed: {sol.message}")
        return sol

    # 1) Run once
    sol = run(t_final)

    # 2) Simple steady-state check
    theta_last = sol.y[:, -1]
    dtheta_last = np.array(odes(sol.t[-1], theta_last, params), dtype=float)
    residual = np.max(np.abs(dtheta_last))

    # 3) If not steady, extend once (simple, not fancy)
    if residual > 1e-8:
        sol = run(2.0 * t_final)
        theta_last = sol.y[:, -1]
        dtheta_last = np.array(odes(sol.t[-1], theta_last, params), dtype=float)
        residual = np.max(np.abs(dtheta_last))

    theta_ss = sol.y[:, -1]
    theta_ss = np.clip(theta_ss, 0.0, 1.0)  # avoid tiny negative noise
    theta_star_ss = max(1.0 - float(np.sum(theta_ss)), 0.0)

    return sol, theta_ss, theta_star_ss
