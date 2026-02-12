# cat-microkinetics
CO oxidation microkinetic model linking surface energetics to catalytic performance.

Overview

This project implements a microkinetic model for heterogeneous CO oxidation on a catalytic surface.

The goal is to connect elementary surface reaction steps to macroscopic catalytic performance (turnover frequency, TOF) under varying gas-phase conditions.

The model demonstrates how surface coverage dynamics govern activity and poisoning behavior.

⸻

Reaction Network

The following elementary steps are modeled:
	1.	CO(g) + * ⇌ CO*
	2.	O₂(g) + 2* ⇌ 2O*
	3.	CO* + O* ⇌ CO₂*
	4.	CO₂* ⇌ CO₂(g) + *

Where:
	•	* represents an empty surface site
	•	θ_CO, θ_O, θ_* represent surface coverages

⸻

Model Structure
	•	Ordinary differential equations (ODEs) describe time evolution of surface coverages.
	•	Steady-state is obtained via time integration.
	•	Net catalytic rate is defined as the net rate of CO₂ formation (r₄).
	•	A parameter sweep over CO partial pressure (PCO) is performed to evaluate performance.

⸻

Key Results

1. Catalytic Performance Curve

TOF vs PCO shows three regimes:
	•	Low PCO: surface mostly free → rate limited by CO adsorption
	•	Intermediate PCO: optimal balance of CO* and O* → maximum activity
	•	High PCO: surface saturated with CO* → oxygen adsorption suppressed → CO poisoning

This behavior arises from site competition and surface coverage coupling.

⸻

2. Surface Coverage Analysis

Coverage vs PCO reveals:
	•	Increasing PCO increases θ_CO
	•	θ_* decreases as CO occupies sites
	•	Oxygen adsorption becomes suppressed at high CO pressure

Catalytic performance is therefore controlled by surface availability, not just intrinsic rate constants.
