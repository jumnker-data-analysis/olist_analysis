## Project Structure

- main.py → Data preparation and KPI generation
- analysis/regression.py → Regression modeling
- data/ → Raw and derived datasets
- reports/figures/ → Model visualizations

Regression Analysis Summary

Objective

Investigate drivers of monthly delivery delay rate using volume and delivery time metrics.

Models Tested

Model 1 — Linear (Volume Only)

R² ≈ 0.17

Volume alone has weak explanatory power.


Model 4 — Quadratic Volume

R² ≈ 0.91

Suggests nonlinear relationship.

Efficiency improves with scale initially.

Slight congestion effect at extreme volumes.


Model 5 — Delivery Days + Interaction

R² ≈ 0.92+

Average delivery days strongly explains delay rate.

Structural time factors dominate.



Model 6 — Log(Volume)

R² ≈ 0.32

Diminishing marginal impact of volume.

Scale effect exists but not primary driver.

Key Business Insight


Delay rate is primarily driven by delivery duration rather than total order volume.



Volume exhibits nonlinear behavior, but structural logistics efficiency and external postal system performance appear to be the dominant factors.

Next Steps
Residual diagnostics

Model comparison table

Multicollinearity check

Robust regression testing