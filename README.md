# CO Oxidation Microkinetics Modeling

## DFT-to-Performance Framework for Catalytic Regime Analysis
This repository implements a physics-based microkinetic framework for heterogeneous CO oxidation on Pt(111).

The objective is to translate DFT-derived adsorption energies and activation barriers into macroscopic catalytic behavior across temperature and gas-phase conditions.

The framework demonstrates how surface competition, kinetic coupling, and operating conditions collectively determine catalytic performance, including turnover frequency (TOF), apparent activation energy, and regime-dependent rate control.

The computational pipeline links:

```bash
DFT Energetics
      ↓
Arrhenius Rate Constants
      ↓
Surface Coverage Dynamics
      ↓
Steady-State Flux (TOF)
      ↓
Catalytic Performance Maps
```
These simulations form the mechanistic foundation for data-driven catalytic modeling and surrogate development.

## Reaction Network
	The following elementary steps are modeled:
	1.	CO(g) + * ⇌ CO*
	2.	O₂(g) + 2* ⇌ 2O*
	3.	CO* + O* ⇌ CO₂*
	4.	CO₂* ⇌ CO₂(g) + *

where * denotes an empty surface site.
 
Surface site balance: 
```bash
θ_CO + θ_O + θ_CO2 + θ_* = 1
```

All rate constants follow Arrhenius kinetics: 
```bash
k = A · exp(−Ea / (kB T))
```

## Mathematical Framework

The model implements a mean-field microkinetic formulation.

	Key components:
	•	ODE-based surface coverage dynamics
	•	Stiff numerical integration using BDF
	•	Steady-state catalytic flux calculation

Turnover frequency (TOF) is defined as the steady-state CO₂ formation rate.

Temperature sweeps enable extraction of apparent activation energy from:
```bash
ln(TOF) vs 1/T
```

## Key Microkinetic Results

### Regime-Dependent Catalytic Performance
	
	TOF vs CO partial pressure reveals three kinetic regimes:
	•	Oxygen-activated regime (low CO)
	•	Balanced regime (maximum activity)
	•	CO-poisoned regime (high CO)

Volcano-like behavior emerges from surface coverage competition, not from a single dominant barrier.

### Surface Coverage Redistribution
	
	Increasing CO partial pressure:
	•	increases θ_CO
	•	decreases available surface sites θ_*
	•	suppresses O₂ adsorption

Catalytic activity is therefore governed by surface availability and flux coupling.

### Emergent Apparent Activation Energy

The apparent activation energy is not equal to any single elementary barrier.

Instead it emerges from system-level flux redistribution and coverage shifts across operating conditions.

### Barrier Sensitivity and Rate Control

Forward activation barriers were perturbed (+0.05 eV) to evaluate flux control.

## Key observations:
	
	•	O₂ dissociation dominates in oxygen-rich regimes
	•	Surface reaction and CO₂ desorption dominate in CO-rich regimes
	•	The rate-controlling step shifts across operating conditions

A 2D regime map visualizes the migration of rate control.

## Technical Implementation

	The modeling framework includes:
	•	Modular Python microkinetic solver
	•	Arrhenius-based rate constant construction
	•	Stiff ODE integration (BDF)
	•	Temperature and pressure sweeps
	•	Apparent activation energy extraction
	•	Barrier perturbation analysis
	•	Catalytic regime visualization

## Model Assumptions
	
	•	Mean-field approximation
	•	Single surface site type
	•	No lateral interactions
	•	No coverage-dependent barriers
	•	No transport limitations

These assumptions preserve mechanistic interpretability while enabling systematic extensions.

## Reproducibility

Run the baseline simulations:

```bash
python run_baseline.py
python sweep_pco.py
python sweep_T.py
python sweep_drc.py
python sweep_heatmap.py
```

## Extension: Machine Learning Surrogate

The microkinetic simulations generated in this repository are used to construct machine learning surrogates for rapid catalytic performance prediction.

## Summary

This project demonstrates how DFT-derived energetics can be translated into predictive catalytic behavior through mechanistic microkinetic modeling.

The framework enables:
	•	catalytic regime identification
	•	sensitivity and rate-control analysis
	•	mechanistic interpretation of apparent activation energies

and forms the kinetic foundation for data-driven catalyst modeling.
