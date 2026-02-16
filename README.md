cat-microkinetics

CO Oxidation Microkinetic Model: From Surface Energetics to Regime-Dependent Catalytic Performance

⸻

Overview

This project implements a physics-based microkinetic model for heterogeneous CO oxidation on a catalytic surface.

The objective is to connect elementary reaction energetics to macroscopic catalytic performance (turnover frequency, TOF) under varying gas-phase conditions.

The framework demonstrates how:
	•	Activation barriers
	•	Surface site competition
	•	Coverage redistribution
	•	Operating conditions

collectively determine catalytic activity, poisoning behavior, and apparent activation energy.

This model establishes a complete computational pipeline:

Barrier heights → Rate constants → Surface dynamics → Steady-state performance

⸻

Reaction Network

The following elementary steps are modeled:
	1.	CO(g) + * ⇌ CO*
	2.	O₂(g) + 2* ⇌ 2O*
	3.	CO* + O* ⇌ CO₂*
	4.	CO₂* ⇌ CO₂(g) + *

Where:
	•		•	represents an empty surface site
	•	θ_CO, θ_O, θ_CO₂, θ_* represent surface coverages

The model explicitly enforces site balance:
θ_CO + θ_O + θ_CO₂ + θ_* = 1

⸻

Mathematical Formulation
	•	Surface coverages evolve according to ordinary differential equations (ODEs).
	•	Steady state is obtained via numerical integration.
	•	Net catalytic rate (TOF) is defined as the steady-state net rate of CO₂ formation (r₄).

All rate constants follow Arrhenius form:

k = A · exp(−Ea / (kB T))

Each elementary step is therefore temperature-dependent and barrier-controlled.

⸻

Results

1. Catalytic Performance vs CO Partial Pressure

The TOF vs PCO sweep reveals three kinetic regimes:
	•	Low PCO: Surface largely free → oxygen chemistry active
	•	Intermediate PCO: Balanced CO* and O* → maximum activity
	•	High PCO: CO* saturation → O₂ adsorption suppressed → CO poisoning

The volcano-like response arises purely from site competition and coverage coupling.

⸻

2. Surface Coverage Redistribution

Coverage analysis shows:
	•	Increasing PCO increases θ_CO
	•	θ_* decreases due to site occupation
	•	O₂ adsorption becomes suppressed at high CO

Catalytic performance is governed by surface availability, not only intrinsic rate constants.

⸻

3. Temperature Dependence and Apparent Activation Energy

Temperature sweeps produce:
	•	TOF vs T (exponential sensitivity)
	•	Arrhenius-style plots: ln(TOF) vs 1/T
	•	Extraction of apparent activation energy (Ea_app)

Key insight:

Ea_app is not equal to a single elementary barrier.
It emerges from system-level flux control and surface redistribution.

⸻

4. Barrier Attribution via Perturbation

To identify controlling barriers, each forward activation energy was perturbed by +0.05 eV and Ea_app was recomputed.

Findings:
	•	Surface reaction (E3f) and CO₂ desorption (E4f) strongly influence Ea_app
	•	O₂ dissociation (E2f) influence depends on CO partial pressure
	•	Dominant barrier changes across regimes

This demonstrates:

Apparent activation energy is regime-dependent and condition-sensitive.

⸻

5. Regime Map: Barrier Attribution vs PCO

A 2D heatmap of ΔEa_app vs PCO reveals:
	•	Low CO: O₂ dissociation contributes more strongly
	•	High CO: Surface reaction and CO₂ desorption dominate
	•	Ea_app decreases as surface becomes CO-poisoned

This establishes a direct link between operating conditions and dominant kinetic barriers.

⸻

Technical Features
	•	Fully Arrhenius-based microkinetic framework
	•	ODE integration for surface dynamics
	•	Parameter sweeps (PCO, T)
	•	Apparent activation energy extraction
	•	Degree-of-rate-control style perturbation analysis
	•	Regime-dependent barrier attribution heatmap

⸻

Core Insight

Catalytic performance is not determined by the largest intrinsic barrier alone.

It is determined by:
	•	Which steps control net flux
	•	How surface coverages redistribute
	•	How operating conditions reshape kinetic bottlenecks

This project demonstrates how a microkinetic model transforms microscopic energetics into interpretable, regime-dependent catalytic behavior.
