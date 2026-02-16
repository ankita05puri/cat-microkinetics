cat-microkinetics

CO oxidation microkinetic model linking surface energetics to catalytic performance.

⸻

Overview

This project implements a microkinetic model for heterogeneous CO oxidation on a catalytic surface.

The objective is to connect elementary reaction energetics to macroscopic catalytic performance (turnover frequency, TOF) under varying thermodynamic conditions.

The framework demonstrates how activation barriers, site competition, and surface coverage dynamics collectively determine catalytic activity and poisoning behavior.

⸻

Reaction Network

The following elementary steps are modeled:
	1.	CO(g) + * ⇌ CO*
	2.	O₂(g) + 2* ⇌ 2O*
	3.	CO* + O* ⇌ CO₂*
	4.	CO₂* ⇌ CO₂(g) + *

Where:
	•		•	represents an empty surface site
	•	θ_CO, θ_O, θ_CO2, and θ_* represent fractional surface coverages

⸻

Model Structure
	•	Ordinary differential equations (ODEs) describe the time evolution of surface coverages.
	•	Steady state is obtained via numerical time integration.
	•	Net catalytic rate (TOF) is defined as the steady-state net rate of CO₂ formation (r₄).
	•	Parameter sweeps are performed over gas-phase conditions (PCO, temperature).

This creates a mechanistic pipeline from microscopic energetics to macroscopic observables:

activation barriers → rate constants → coverage redistribution → steady-state TOF

⸻

Arrhenius Kinetics Extension

The model was extended from fixed rate constants to Arrhenius-based kinetics:

k = A \exp(-E_a / k_B T)

Each elementary step now depends explicitly on activation energy and temperature.

Temperature sweeps reveal exponential sensitivity of TOF to barrier heights and enable extraction of an apparent activation energy (Ea_app) from Arrhenius-style plots:

\ln(\text{TOF}) \text{ vs } 1/T

⸻

Apparent Activation Energy & Barrier Attribution

Ea_app was obtained from linear fitting of ln(TOF) vs 1/T.

To determine which elementary barrier controls Ea_app, individual forward activation energies were perturbed by +0.05 eV (one at a time), and Ea_app was recomputed.

At baseline conditions:
	•	Increasing E2f (O₂ dissociation) shifts Ea_app by ~0.05 eV
	•	Increasing E3f (surface reaction) shifts Ea_app by ~0.10 eV
	•	Increasing E4f (CO₂ desorption) shifts Ea_app by ~0.10 eV

This demonstrates that Ea_app is an emergent system-level quantity rather than the largest single microscopic barrier.

⸻
Regime-Dependent Barrier Attribution

Barrier sensitivity was evaluated under two CO partial pressure regimes:
PCO	Ea_app (eV)	ΔE2f	ΔE3f	ΔE4f
0.1	1.60	+0.069	+0.073	+0.086
2.0	1.37	+0.050	+0.105	+0.105

At low CO pressure, multiple barriers contribute comparably to Ea_app, indicating mixed kinetic control under oxygen-accessible conditions.

At high CO pressure, sensitivity shifts toward the surface reaction and CO₂ desorption steps, while O₂ dissociation becomes less influential. This reflects CO-induced site blocking and redistribution of kinetic control.

These results show that the dominant kinetic barrier is condition-dependent and emerges from coverage dynamics rather than intrinsic surface energetics alone.

⸻

Key Results

1. Catalytic Performance Curve (TOF vs PCO)

The TOF vs PCO sweep reveals three regimes:
	•	Low PCO: Surface mostly free → rate limited by CO adsorption
	•	Intermediate PCO: Balanced θ_CO and θ_O → maximum activity
	•	High PCO: Surface saturated with CO* → oxygen adsorption suppressed → CO poisoning

This nonlinear behavior emerges from site competition and coverage coupling.

⸻

2. Surface Coverage Analysis

Coverage vs PCO shows:
	•	Increasing PCO increases θ_CO
	•	θ_* decreases as CO occupies surface sites
	•	O₂ adsorption becomes suppressed at high CO pressure

Catalytic performance is governed by surface availability and kinetic competition, not solely intrinsic rate constants.
