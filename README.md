# cat-microkinetics
CO oxidation microkinetic model linking surface energetics to catalytic performance.

Overview

This project implements a microkinetic model for heterogeneous CO oxidation on a catalytic surface.

The objective is to connect elementary surface reaction energetics to macroscopic catalytic performance (turnover frequency, TOF) under varying thermodynamic conditions.

The framework demonstrates how surface coverage dynamics, site competition, and activation barriers collectively determine catalytic activity and poisoning behavior.

⸻

Reaction Network

The following elementary steps are modeled:
	1.	CO(g) + * ⇌ CO*
	2.	O₂(g) + 2* ⇌ 2O*
	3.	CO* + O* ⇌ CO₂*
	4.	CO₂* ⇌ CO₂(g) + *

Where:
	•	* represents an empty surface site
	•	θ_CO, θ_O, θ_CO2, and θ_* represent surface coverages

⸻

Model Structure
	•	Ordinary differential equations (ODEs) describe the time evolution of surface coverages.
	•	Steady state is obtained via numerical integration.
	•	Net catalytic rate (TOF) is defined as the steady-state net rate of CO₂ formation (r₄).
	•	Parameter sweeps are performed over gas-phase conditions (PCO, temperature).

⸻

Session 4 — Temperature-Dependent Kinetics

The model was extended from fixed rate constants to Arrhenius-based kinetics:

k = A · exp(−Ea / kBT)

Each elementary step now depends explicitly on activation energy and temperature.
This connects microscopic barrier heights directly to macroscopic catalytic performance.

Temperature sweeps reveal the exponential sensitivity of TOF to activation energies and highlight how competing elementary steps and surface coverage redistribution govern overall reactivity.

The model now forms a physically grounded pipeline:

energetics → rate constants → surface dynamics → steady-state performance

⸻

Key Results

1. Catalytic Performance Curve (TOF vs PCO)

The TOF vs PCO sweep reveals three regimes:
	•	Low PCO: Surface mostly free → rate limited by CO adsorption
	•	Intermediate PCO: Balanced θ_CO and θ_O → maximum activity
	•	High PCO: Surface saturated with CO* → oxygen adsorption suppressed → CO poisoning

This non-linear behavior emerges from site competition and coverage coupling.

⸻

2. Surface Coverage Analysis

Coverage vs PCO shows:
	•	Increasing PCO increases θ_CO
	•	θ_* decreases as CO occupies surface sites
	•	Oxygen adsorption becomes suppressed at high CO pressure

Catalytic performance is therefore governed by surface availability and kinetic competition, not solely intrinsic rate constants.
