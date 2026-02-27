CO Oxidation Microkinetic & Surrogate Modeling Framework

From Periodic DFT Energetics to Regime-Dependent Catalytic Performance

⸻

Overview

This repository implements a physics-based microkinetic framework for heterogeneous CO oxidation on Pt(111), and extends it with a physics-informed machine learning surrogate for rapid performance evaluation.

The objective is to transform periodic DFT-derived adsorption energies and activation barriers into macroscopic catalytic behavior under varying temperature and gas-phase conditions — and to assess how well a surrogate model can approximate that behavior across kinetic regimes.

The computational pipeline links:

DFT Energetics → Arrhenius Rate Constants → Surface Coverage Dynamics → Steady-State Flux → Catalytic Performance Maps → Surrogate Approximation

This framework demonstrates how surface competition, kinetic coupling, and operating conditions collectively determine turnover frequency (TOF), apparent activation energy, and regime-dependent rate control.

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
	•	Stiff numerical integration (BDF) to steady state
	•	TOF defined as steady-state net CO₂ formation rate

Temperature sweeps enable extraction of apparent activation energy (Ea_app) from ln(TOF) vs 1/T analysis.

⸻

Key Microkinetic Results

1. Regime-Dependent Catalytic Performance

TOF vs P_CO reveals three kinetic regimes:
	•	Oxygen-activated regime (low CO)
	•	Balanced regime (maximum activity)
	•	CO-poisoned regime (high CO)

Volcano-like behavior emerges from site competition and coverage redistribution — not from a single dominant barrier.

⸻

2. Surface Coverage Redistribution

Increasing CO partial pressure:
	•	Increases θ_CO
	•	Decreases θ_*
	•	Suppresses O₂ adsorption

Catalytic performance is governed by surface availability and flux coupling, not intrinsic rate constants alone.

⸻

3. Emergent Apparent Activation Energy

Apparent activation energy is not equal to any single elementary barrier.

It emerges from system-level flux redistribution and coverage shifts across operating conditions.

⸻

4. Barrier Sensitivity & Regime Mapping

Forward activation barriers were perturbed (+0.05 eV) to quantify flux control (DRC-style analysis).

Findings:
	•	O₂ dissociation dominates in oxygen-rich regimes
	•	Surface reaction and CO₂ desorption dominate in CO-rich regimes
	•	The kinetically controlling step shifts across state space

A 2D regime map explicitly visualizes migration of rate control.

⸻

Surrogate Modeling & Generalization Analysis

Objective

To evaluate whether a physics-informed machine learning surrogate can approximate microkinetic TOF across operating conditions (T, P_CO), and to analyze its generalization behavior across kinetic regimes.

Because catalytic rates span multiple orders of magnitude, the surrogate is trained in log space.

⸻

Feature Engineering

Physics-informed features:
	•	invT = 1/T
	•	logPCO = log(P_CO)
	•	Target: log(TOF)

Log-space training reflects Arrhenius scaling and stabilizes learning.

⸻

Interpolation Performance (Random Split)

When trained and tested on mixed state space (random split):
	•	R²(logTOF) ≈ 0.99
	•	R²(TOF) ≈ 0.99

The surrogate accurately interpolates within the trained kinetic manifold.

See:
	•	figures/ml/parity_random.png
	•	figures/ml/error_vs_pco_random.png

This demonstrates that microkinetic behavior can be efficiently approximated for rapid sweeps within known regimes.

⸻

Extrapolation Performance (PCO Hold-Out)

When trained on P_CO ≤ 1.0 and evaluated on P_CO > 1.0:
	•	Structured error growth observed
	•	Absolute log-error increases systematically with CO pressure
	•	Performance degrades in the CO-poisoned regime

See:
	•	figures/ml/parity_holdout_pco_1p0.png
	•	figures/ml/error_vs_pco_holdout_pco_1p0.png

This reveals that:
	•	The surrogate approximates learned manifolds
	•	It does not extrapolate reliably across unseen kinetic regimes
	•	Regime transitions must be treated explicitly

The degradation aligns with physical transition into surface poisoning, highlighting limitations of purely data-driven extrapolation.

⸻

Generalization Curve

Performance was evaluated across increasing P_CO training cutoffs to quantify regime-dependent learning behavior.

See:
	•	figures/ml/generalization_curve.png

The curve shows systematic improvement as more of the high-CO regime is included in training.

⸻

Core Insight

Catalytic performance is not determined by the largest intrinsic barrier.

It is determined by:
	•	Which steps control net flux
	•	How surface coverages redistribute
	•	How operating conditions reshape kinetic bottlenecks
	•	Whether surrogate models are trained within the correct regime

This framework demonstrates:
	•	How electronic-structure energetics translate into predictive catalytic behavior
	•	How regime transitions emerge from mechanistic coupling
	•	Where data-driven surrogates succeed and where they fail

Mechanistic modeling and machine learning are complementary — not interchangeable.

⸻

Technical Implementation
	•	Modular Python solver
	•	Arrhenius-based rate construction
	•	Stiff ODE integration (BDF)
	•	Temperature and P_CO sweeps
	•	Apparent activation energy extraction
	•	Barrier perturbation analysis
	•	Regime heatmap visualization
	•	Physics-informed ML surrogate (Gradient Boosting)
	•	Interpolation vs extrapolation diagnostics

⸻

Model Assumptions
	•	Mean-field approximation
	•	Single site type
	•	No lateral interactions
	•	No coverage-dependent barriers
	•	No transport limitations

These assumptions preserve interpretability while enabling systematic extension.

⸻

Reproducibility

Microkinetic simulations:
```bash
python run_baseline.py
python sweep_pco.py
python sweep_T.py
python sweep_drc.py
python sweep_heatmap.py
```

Surrogate modeling:
```bash
python -m ml.generate_dataset
python -m ml.surrogate
python -m ml.generalization_curve
```
⸻

Summary

This project integrates:
	•	Electronic-structure energetics
	•	Mechanistic microkinetic modeling
	•	Regime mapping
	•	Sensitivity analysis
	•	Physics-informed surrogate modeling
	•	Generalization diagnostics

It demonstrates how catalytic behavior emerges from nonlinear surface dynamics — and how surrogate models must respect regime structure to remain predictive.
