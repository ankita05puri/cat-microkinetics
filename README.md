CO Oxidation Microkinetic Modeling Framework

From Periodic DFT Energetics to Regime-Dependent Catalytic Performance

⸻

Overview

This repository implements a physics-based microkinetic framework for heterogeneous CO oxidation on Pt(111).

The objective is to translate periodic DFT-derived adsorption energies and activation barriers into macroscopic catalytic performance under varying temperature and gas-phase conditions.

The computational pipeline links:

DFT Energetics → Arrhenius Rate Constants → Surface Coverage Dynamics → Steady-State Flux → Catalyst Performance Maps

The framework demonstrates how surface competition, kinetic coupling, and operating conditions collectively determine turnover frequency (TOF) and apparent activation behavior.

⸻

Reaction Network

The following elementary steps are modeled:
	1.	CO(g) + * ⇌ CO*
	2.	O₂(g) + 2* ⇌ 2O*
	3.	CO* + O* ⇌ CO₂*
	4.	CO₂* ⇌ CO₂(g) + *

where * denotes an empty surface site.

Surface site balance is explicitly enforced:

θ_CO + θ_O + θ_CO₂ + θ_* = 1

All rate constants follow Arrhenius form:

k = A · exp(−Ea / (kB T))

⸻

Mathematical Framework
	•	Mean-field microkinetic model
	•	ODE-based surface coverage evolution
	•	Numerical integration to steady state
	•	TOF defined as steady-state net CO₂ formation rate

Temperature sweeps enable extraction of apparent activation energy (Ea_app) from ln(TOF) vs 1/T analysis.

⸻

Key Results

1. Regime-Dependent Catalytic Performance

TOF vs P_CO reveals three kinetic regimes:
	•	Oxygen-activated regime (low CO)
	•	Balanced regime (maximum activity)
	•	CO-poisoned regime (high CO)

Volcano-like behavior emerges from site competition and coverage redistribution, not from a single dominant barrier.

⸻

2. Surface Coverage Redistribution

Increasing CO partial pressure:
	•	Increases θ_CO
	•	Decreases θ_*
	•	Suppresses O₂ adsorption

Catalytic performance is governed by surface availability and flux coupling, not intrinsic rate constants alone.

⸻

3. Emergent Apparent Activation Energy

Apparent activation energy is not equal to any individual elementary barrier.

It emerges from system-level flux redistribution and coverage shifts across operating conditions.

⸻

4. Barrier Sensitivity and Regime Mapping

Forward activation barriers were perturbed (+0.05 eV) to quantify flux control.

Findings:
	•	O₂ dissociation dominates in oxygen-rich regimes
	•	Surface reaction and CO₂ desorption dominate in CO-rich regimes
	•	The kinetically controlling step shifts across state space

A 2D regime map explicitly visualizes migration of rate control.

⸻

Technical Implementation
	•	Python-based modular solver
	•	Arrhenius-based rate construction
	•	Stiff ODE integration (BDF)
	•	Temperature and P_CO sweeps
	•	Apparent activation energy extraction
	•	Barrier perturbation analysis (DRC-style)
	•	Regime heatmap visualization

The architecture is modular and compatible with periodic DFT workflows and future data-driven parameterization.

⸻

Model Assumptions
	•	Mean-field approximation
	•	Single site type
	•	No lateral interactions
	•	No coverage-dependent barriers
	•	No transport limitations

These assumptions preserve interpretability while allowing systematic extension.

⸻

Reproducibility
	•	python run_baseline.py
	•	python sweep_pco.py
	•	python sweep_T.py
	•	python sweep_drc.py
	• 	python sweep_heatmap.py

⸻

Core Insight

Catalytic performance is not determined by the largest intrinsic barrier.

It is determined by:
	•	Which steps control net flux
	•	How surface coverages redistribute
	•	How operating conditions reshape kinetic bottlenecks

This framework demonstrates how electronic-structure energetics can be transformed into predictive, regime-dependent catalytic behavior.

