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

# Next Steps
Residual diagnostics

Model comparison table

Multicollinearity check

Robust regression testing

# Olist Delay Rate Analysis – Model Evaluation

Objective

To identify the key drivers of monthly delay rate using regression modeling and evaluate model robustness through diagnostics and alternative specifications.

Modeling Process

We tested multiple regression specifications to understand the structural relationship between delay rate and operational variables.

# Model 1: Volume Only (Linear)

Model:delay_rate ~ total_orders

R² ≈ 0.056

Conclusion:

Order volume alone has very weak explanatory power. Volume is not the primary driver of delay.

# Model 2: Volume + Average Delivery Days (Core Model)

Model:delay_rate ~ total_orders + avg_delivery_days

R² ≈ 0.915

MAE ≈ 0.036

Conclusion:

Delay rate is primarily driven by delivery duration.

Business Interpretation:

Operational efficiency (delivery performance) dominates delay behavior. Volume amplifies stress but is not the core determinant.

This is the selected final model.

# Model 3: Volume + Time Trend

Model: delay_rate ~ total_orders + month_index

Low R².

Conclusion:

No significant linear time trend explains delay variation.

# Model 4: Quadratic Volume

Model: delay_rate ~ total_orders + total_orders²

R² ≈ 0.208

Conclusion:

Some nonlinear congestion effect exists at extreme volumes, but explanatory power remains limited.

# Model 5: Volume + Delivery Days + Interaction

Model: delay_rate ~ total_orders + avg_delivery_days + interaction

Conclusion:

Interaction effects do not materially improve explanatory power. Delivery duration remains dominant.

# Model 6: Log Volume

Model:delay_rate ~ log(total_orders)

R² ≈ 0.323

Conclusion:

There is evidence of diminishing marginal effect of scale, but volume remains secondary to delivery duration.

# Model Diagnostics

Residual Analysis

Residual plots indicate heteroskedasticity:

Residual variance increases at higher predicted delay rates.

This suggests higher uncertainty during stress regimes.

Interpretation:

Variance increases due to structural operational stress rather than random noise.

# Ridge Regression

Ridge regularization was applied to test for overfitting.

Result:

No meaningful change in R² or MAE.

Coefficients remain stable.

Conclusion:

The model does not suffer from severe overfitting.

# Weighted Regression

Weighted regression (inverse of delivery days) was tested to address heteroskedasticity.

Result:

R² decreased

MAE increased

# Conclusion:

High-delay months contain structural signal, not noise.

Down-weighting them reduces explanatory power.

Therefore, weighted regression is not appropriate for this dataset.

# Final Model Selection

Selected Model:

delay_rate ~ total_orders + avg_delivery_days

# Reason:

Highest explanatory power

Lowest MAE

Stable under regularization

Robust against weighting

# Business Implications
Delay rate is primarily driven by delivery performance.

Volume amplifies stress but does not independently drive delays.

Operational KPIs should focus on:

Average delivery lead time

Warehouse processing time

Inventory availability rate

Order fulfillment cycle time

On-time dispatch rate

# Key Insight

Delay behavior is operationally driven, not demand-driven.

Volume exhibits nonlinear effects but is not the dominant factor.

Delivery duration is the structural backbone of delay variation.