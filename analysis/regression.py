import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

# ---- Load data ----
kpi_path = Path("data") / "monthly_kpi.csv"
monthly_kpi = pd.read_csv(kpi_path)

# ---- Basic checks ----
print("Rows:", len(monthly_kpi))
print(monthly_kpi.head())
print("\nMissing values:\n", monthly_kpi.isna().sum())

# Make sure numeric columns are numeric
for col in ["total_orders", "avg_delivery_days", "delay_rate"]:
    monthly_kpi[col] = pd.to_numeric(monthly_kpi[col], errors="coerce")

monthly_kpi = monthly_kpi.dropna(subset=["total_orders", "avg_delivery_days", "delay_rate"])

monthly_kpi["month_index"] = range(len(monthly_kpi))

# ---- Model 1: Simple Linear Regression ----
# delay_rate = b0 + b1 * total_orders
X1 = monthly_kpi[["total_orders"]]
y = monthly_kpi["delay_rate"]

m1 = LinearRegression()
m1.fit(X1, y)

pred1 = m1.predict(X1)

print("\nMODEL 1: delay_rate ~ total_orders")
print("Intercept:", m1.intercept_)
print("Coefficient (total_orders):", m1.coef_[0])
print("R2:", r2_score(y, pred1))
print("MAE:", mean_absolute_error(y, pred1))

# ---- Model 2: Multiple Linear Regression ----
# delay_rate = b0 + b1 * total_orders + b2 * avg_delivery_days
X2 = monthly_kpi[["total_orders", "avg_delivery_days"]]

m2 = LinearRegression()
m2.fit(X2, y)

pred2 = m2.predict(X2)

print("\nMODEL 2: delay_rate ~ total_orders + avg_delivery_days")
print("Intercept:", m2.intercept_)
print("Coefficients:", dict(zip(X2.columns, m2.coef_)))
print("R2:", r2_score(y, pred2))
print("MAE:", mean_absolute_error(y, pred2))

X2 = monthly_kpi[["total_orders", "avg_delivery_days"]]
y = monthly_kpi["delay_rate"]

# Define weights (inverse of delivery days)
weights = 1 / (monthly_kpi["avg_delivery_days"] + 1e-6)

# Fit weighted regression
model_wls = LinearRegression()
model_wls.fit(X2, y, sample_weight=weights)

pred_wls = model_wls.predict(X2)

from sklearn.metrics import r2_score, mean_absolute_error

print("\nWeighted Regression (WLS)")
print("Coefficients:", dict(zip(X2.columns, model_wls.coef_)))
print("R2:", r2_score(y, pred_wls))
print("MAE:", mean_absolute_error(y, pred_wls))


# The volume is weak
# Add time trend


# Model 3: delay_rate ~ total_orders + month_index
X3 = monthly_kpi[["total_orders", "month_index"]]
m3 = LinearRegression()
m3.fit(X3, y)
pred3 = m3.predict(X3)

print("\nMODEL 3: delay_rate ~ total_orders + month_index")
print("Coefficients:", dict(zip(X3.columns, m3.coef_)))
print("R2:", r2_score(y, pred3))
print("MAE:", mean_absolute_error(y, pred3))

# Testing nonlinear volume effect
monthly_kpi["total_orders_sq"] = monthly_kpi["total_orders"]**2
X4 = monthly_kpi[["total_orders", "total_orders_sq"]]
m4 = LinearRegression()
m4.fit(X4,y)
pred4 = m4.predict(X4)
print("\nMODEL 4: delay_rate ~ total_orders + total_orders_sq")
print("Coefficients:", dict(zip(X4.columns,m4.coef_)))
print("R2",r2_score(y,pred4))
print("MAE:", mean_absolute_error(y,pred4))

# ----- Model 5: Interaction Effect -----
monthly_kpi["interaction"] = (
monthly_kpi["total_orders"] * monthly_kpi["avg_delivery_days"]
)

X5 = monthly_kpi[["total_orders", "avg_delivery_days", "interaction"]]

m5 = LinearRegression()
m5.fit(X5, y)
pred5 = m5.predict(X5)

print("\nMODEL 5: delay_rate ~ total_orders + avg_delivery_days + interaction")
print("Coefficients:", dict(zip(X5.columns, m5.coef_)))
print("R2:", r2_score(y, pred5))
print("MAE:", mean_absolute_error(y, pred5))


import numpy as np

monthly_kpi["log_orders"] = np.log(monthly_kpi["total_orders"])

X6 = monthly_kpi[["log_orders"]]

m6 = LinearRegression()
m6.fit(X6, y)
pred6 = m6.predict(X6)

print("\nMODEL 6: delay_rate ~ log(total_orders)")
print("Coefficient:", m6.coef_[0])
print("R2:", r2_score(y, pred6))
print("MAE:", mean_absolute_error(y, pred6))

# ----- Visualization for Model 4 (Quadratic Volume Model) -----

sorted_df_quad = monthly_kpi.sort_values("total_orders")

X4_sorted = sorted_df_quad[["total_orders", "total_orders_sq"]]
pred4_sorted = m4.predict(X4_sorted)

plt.figure(figsize=(8, 5))

plt.scatter(monthly_kpi["total_orders"], y, alpha=0.6, label="Actual")
plt.plot(sorted_df_quad["total_orders"], pred4_sorted,
color="red", label="Quadratic Fit")

plt.xlabel("Total Orders")
plt.ylabel("Delay Rate")
plt.title("Delay Rate vs Volume (Quadratic Model)")
plt.legend()
plt.tight_layout()

plt.savefig("reports/figures/model4_quadratic_volume.png", dpi=300)
plt.close()


# ----- Visualization for Model 6 (Log Volume Model) -----

sorted_df_log = monthly_kpi.sort_values("total_orders")

X6_sorted = sorted_df_log[["log_orders"]]
pred6_sorted = m6.predict(X6_sorted)

plt.figure(figsize=(8, 5))

plt.scatter(monthly_kpi["total_orders"], y, alpha=0.6, label="Actual")
plt.plot(sorted_df_log["total_orders"], pred6_sorted,
color="green", label="Log Fit")

plt.xlabel("Total Orders")
plt.ylabel("Delay Rate")
plt.title("Delay Rate vs Volume (Log Model)")
plt.legend()
plt.tight_layout()

plt.savefig("reports/figures/model6_log_volume.png", dpi=300)
plt.close()

# ----- Residual Diagnostics for Model 4 26/02-----

residuals4 = y - pred4

plt.figure(figsize=(8, 5))
plt.scatter(pred4, residuals4, alpha=0.7)
plt.axhline(0, color='red')
plt.xlabel("Predicted Delay Rate")
plt.ylabel("Residuals")
plt.title("Residual Plot - Quadratic Model")
plt.tight_layout()
plt.savefig("reports/figures/model4_residuals.png", dpi=300)
plt.close()

print("Residual mean (Model 4):", residuals4.mean())
print("Residual std (Model 4):", residuals4.std())


# -- Comparison Models
model_comparison = pd.DataFrame({
"Model": [
"Linear Volume",
"Volume + Delivery Days",
"Volume + Time",
"Quadratic Volume",
"Log Volume"
],
"R2": [
r2_score(y, pred1),
r2_score(y, pred2),
r2_score(y, pred3),
r2_score(y, pred4),
r2_score(y, pred6)
],
"MAE": [
mean_absolute_error(y, pred1),
mean_absolute_error(y, pred2),
mean_absolute_error(y, pred3),
mean_absolute_error(y, pred4),
mean_absolute_error(y, pred6)
]
})

print("\nModel Comparison Table:")
print(model_comparison)


# ----- Ridge Regression on Quadratic Model -----

from sklearn.linear_model import Ridge

ridge = Ridge(alpha=1.0)
ridge.fit(X4, y)
pred_ridge = ridge.predict(X4)

print("\nRidge Regression (Quadratic)")
print("Coefficients:", dict(zip(X4.columns, ridge.coef_)))
print("R2:", r2_score(y, pred_ridge))
print("MAE:", mean_absolute_error(y, pred_ridge))