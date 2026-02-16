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
	•	θ_CO, θ_O, θ_CO2, and θ_* represent surface coverages

⸻

Model Structure
	•	Ordinary differential equations (ODEs) describe the time evolution of surface coverages.
	•	Steady state is obtained via numerical time integration.
	•	Net catalytic rate (TOF) is defined as the steady-state net rate of CO₂ formation (r₄).
	•	Parameter sweeps are performed over gas-phase conditions (PCO, temperature).

This creates a full pipeline from microscopic kinetics to macroscopic observables.

⸻

Arrhenius Kinetics Extension

The model was extended from fixed rate constants to Arrhenius-based kinetics:

k = A \exp(-E_a / k_B T)

Each elementary step now depends explicitly on activation energy and temperature.

This connects microscopic barrier heights directly to system-level catalytic performance:

barrier height → rate constant → surface redistribution → steady-state TOF

Temperature sweeps show the expected exponential increase in TOF and enable extraction of an apparent activation energy (Ea_app) from Arrhenius-style plots:

\ln(\text{TOF}) \text{ vs } 1/T

⸻

Apparent Activation Energy & Barrier Attribution

The apparent activation energy (Ea_app) was obtained by linear fitting of ln(TOF) vs 1/T.

To determine which elementary barrier controls Ea_app, individual forward activation energies were perturbed by +0.05 eV (one at a time), and Ea_app was recomputed.

Results show:
	•	Increasing E2f (O₂ dissociation) increases Ea_app by ~0.05 eV
	•	Increasing E3f (surface reaction) increases Ea_app by ~0.10 eV
	•	Increasing E4f (CO₂ desorption) increases Ea_app by ~0.10 eV

This demonstrates that Ea_app is a system-level quantity, not simply the largest single barrier.

Its magnitude depends on:
	•	Which steps control net flux
	•	Surface coverage distribution
	•	Operating regime (temperature and partial pressures)

In this baseline condition, surface reaction and CO₂ desorption contribute more strongly to temperature sensitivity than O₂ dissociation.

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

Catalytic performance is therefore governed by surface availability and kinetic competition, not solely intrinsic rate constants.
