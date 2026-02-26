CO Oxidation Microkinetic Modeling Framework

From Periodic DFT Energetics to Regime-Dependent Catalytic Performance

⸻

Overview

This repository implements a physics-based microkinetic modeling framework for heterogeneous CO oxidation on Pt(111).

The objective is to translate periodic DFT-derived adsorption energies and activation barriers into macroscopic catalytic performance metrics under varying temperature and gas-phase conditions.

The framework connects:

DFT Energetics → Arrhenius Rate Constants → Surface Coverage Dynamics → Steady-State Flux → Catalyst Performance Maps

It demonstrates how surface competition, kinetic coupling, and operating conditions collectively determine turnover frequency and apparent activation behavior.

⸻

Reaction Network

The following elementary steps are modeled:
	1.	CO(g) + * ⇌ CO*
	2.	O₂(g) + 2* ⇌ 2O*
	3.	CO* + O* ⇌ CO₂*
	4.	CO₂* ⇌ CO₂(g) + *

Where * denotes an empty surface site.

Surface site balance is explicitly enforced:

θ_CO + θ_O + θ_CO₂ + θ_* = 1

All forward and reverse rate constants follow Arrhenius form:

k = A · exp(−Ea / (kB T))

⸻

Mathematical Framework
	•	Mean-field microkinetic model
	•	ODE-based surface coverage evolution
	•	Numerical integration to steady state
	•	Turnover frequency (TOF) defined as steady-state net CO₂ formation rate

Temperature sweeps enable extraction of apparent activation energy (Ea_app) from Arrhenius-style ln(TOF) vs 1/T analysis.

⸻

Key Results

1. Regime-Dependent Catalytic Performance

TOF vs P_CO reveals three distinct kinetic regimes:
	•	Oxygen-activated regime (low CO partial pressure)
	•	Balanced surface regime (maximum catalytic activity)
	•	CO-poisoned regime (high CO partial pressure)

Volcano-like activity emerges from surface site competition and coverage redistribution, not from a single dominant barrier.

⸻

2. Surface Coverage Redistribution

Increasing CO partial pressure shifts surface occupation:
	•	θ_CO increases
	•	θ_* decreases
	•	O₂ adsorption becomes suppressed

Catalytic performance is governed by surface availability and flux coupling, not intrinsic rate constants alone.

⸻

3. Apparent Activation Energy Emergence

Apparent activation energy is not equal to any single elementary barrier.

It emerges from system-level flux redistribution and shifts in surface coverage across operating conditions.

⸻

4. Barrier Sensitivity Analysis

Forward activation energies were perturbed (+0.05 eV) to quantify regime-dependent flux control.

Findings:
	•	Surface reaction and CO₂ desorption dominate in CO-rich regimes
	•	O₂ dissociation dominates in oxygen-rich regimes
	•	The kinetically controlling barrier shifts across state space

This demonstrates condition-dependent migration of rate control.

⸻

Technical Implementation
	•	Python-based microkinetic solver
	•	Arrhenius-based rate constant construction
	•	ODE integration for surface dynamics
	•	Parameter sweeps across temperature and P_CO
	•	Apparent activation energy extraction
	•	Barrier perturbation analysis
	•	Regime heatmap visualization

The architecture is modular and designed for integration with periodic DFT workflows and data-driven parameterization.

⸻

Model Assumptions
	•	Mean-field approximation (no lateral interactions)
	•	Single active site type
	•	No coverage-dependent activation barriers
	•	No transport limitations
	•	Uniform surface

These assumptions maintain interpretability while allowing extension toward more complex models.

⸻

Reproducibility
	• Run baseline simulation: python run_baseline.py
	• Sweep CO partial pressure: python sweep_pco.py
	• Generate regime heatmap: python sweep_heatmap.py

⸻

Core Insight

Catalytic performance is not determined by the largest intrinsic barrier.

It is determined by:
	•	Which steps control net flux
	•	How surface coverages redistribute
	•	How operating conditions reshape kinetic bottlenecks

This framework demonstrates how electronic structure energetics can be transformed into predictive, regime-dependent catalytic performance maps.


