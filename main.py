import pandas as pd
# Load dataset
orders= pd.read_csv("data/olist_orders_dataset.csv")

# Show basic info
#print("First 5 rows:")
#print(orders.head())

#print("\nDataset info:")
#print(orders.info())

#print("\nSummary statistics:")
#print(orders.describe())

import pandas as pd 

orders= pd.read_csv(
    "data/olist_orders_dataset.csv",
#convert character into datetime
parse_dates=[
"order_purchase_timestamp",
"order_approved_at",
"order_delivered_carrier_date",
"order_delivered_customer_date",
"order_estimated_delivery_date",
]
)
#print("\nDataset info:")
#orders.info()

#create new time features
orders["purchase_year"] = orders["order_purchase_timestamp"].dt.year
orders["purchase_month"] = orders["order_purchase_timestamp"].dt.month
orders["purchase_day"] = orders["order_purchase_timestamp"].dt.day
#print(orders[["order_purchase_timestamp","purchase_year",
# "purchase_month","purchase_day"]].head())

# Today's Goal 21/02/2026 
# Analyse delivery performance and delay rate
# Step 1 Delivery performance
delivered=orders[orders["order_status"]=="delivered"].copy()

delivered["delivery_days"]=(
    delivered["order_delivered_customer_date"]-
    delivered["order_purchase_timestamp"]
).dt.days

delivered["delivery_delay"]=(
    delivered["order_delivered_customer_date"]-
    delivered["order_estimated_delivery_date"]
).dt.days

# print("\nDelivery columns preview:")
# print(delivered[["delivery_days","delivery_delay"]].head(10))

# print("\nDelivery_days summary:")
# print(delivered["delivery_days"].describe())

# print("\nDelivery_delay summary:")
# print(delivered["delivery_delay"].describe())

# step 2 KPI + monthly trend (Power BI friendly)

# create omnthly column
delivered["purchase_month"]= delivered["order_purchase_timestamp"].dt.to_period("M")
# print(delivered[["order_purchase_timestamp","purchase_month"]].head())

# create monthly KPI
monthly_kpi = delivered.groupby("purchase_month").agg(
    total_orders=("order_id", "count"),
    avg_delivery_days=("delivery_days", "mean"),
    avg_delay=("delivery_delay", "mean"),
    delayed_orders=("delivery_delay", lambda x: (x > 0).sum())
).reset_index()

monthly_kpi["delay_rate"] = monthly_kpi["delayed_orders"] / monthly_kpi["total_orders"]

monthly_kpi = monthly_kpi.sort_values("purchase_month")

print(monthly_kpi.head())

# visualise the Delay rate trend
import matplotlib.pyplot as plt


monthly_kpi["purchase_month"]=monthly_kpi["purchase_month"].astype(str)
plt.figure(figsize=(10,5))
plt.plot(
    monthly_kpi["purchase_month"],
    monthly_kpi["delay_rate"]
)
plt.xticks(rotation=45)
plt.title("Monthly Delay Rate Trend")
plt.xlabel("Purchase_month")
plt.ylabel("Delay_rate")
plt.tight_layout()
plt.savefig("reports/figures/monthly_delay_trend.png",dpi=300)
plt.show()
plt.close()
# The spike month is 2018-02 and 2016-09 but there is 
# only 1 order 2016-09 so we should ignore the noise 2016-09

# Correlation between volume and delay rate:
print("\nCorrelation between volume and delay rate:")
print(monthly_kpi[["total_orders","delay_rate"]].corr())

delivered["order_delivered_customer_date"]= pd.to_datetime(delivered["order_delivered_customer_date"])
delivered["month"]= delivered["order_delivered_customer_date"].dt.to_period("M")

monthly_delay = (
    delivered.groupby("month")["delivery_delay"]
    .mean()
    .reset_index())
print(monthly_delay)

monthly_delay["month"]=monthly_delay["month"].astype(str)

import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))
plt.plot(monthly_delay["month"],monthly_delay["delivery_delay"])
plt.xticks(rotation=45)
plt.title("Average Delivery Delay by Month")
plt.xlabel("Month")
plt.tight_layout()

plt.savefig("reports/figures/monthly_avg_delivery_delay_trend.png",dpi=300)
plt.show()
plt.close()

# Observation:
# If the trend increases -> operational inefficiency growing.
# If decreasing -> logistics improving.
# If stable -> process control stable.

# export clean dataset for modeling
monthly_kpi.to_csv("data/monthly_kpi.csv",index=False)

# 1. Regime Segmentation (Low vs High Stress)
## Step 1 — Split Data
threshold = monthly_kpi["total_orders"].median()

low_regime = monthly_kpi[monthly_kpi["total_orders"] < threshold]
high_regime = monthly_kpi[monthly_kpi["total_orders"] >= threshold]

## Step 2 — Fit OLS Separately 
import statsmodels.api as sm

# LOW REGIME
X_low = sm.add_constant(low_regime["total_orders"])
y_low = low_regime["delay_rate"]

model_low = sm.OLS(y_low, X_low).fit()

print("LOW STRESS REGIME")
print(model_low.summary())

# HIGH REGIME
X_high = sm.add_constant(high_regime["total_orders"])
y_high = high_regime["delay_rate"]

model_high = sm.OLS(y_high, X_high).fit()

print("HIGH STRESS REGIME")
print(model_high.summary())


## Instead of splitting manually, you can also 
## create interaction model:
monthly_kpi["high_stress"] = (monthly_kpi["total_orders"] >= threshold).astype(int)

X = monthly_kpi[["total_orders", "high_stress"]]
X["interaction"] = X["total_orders"] * X["high_stress"]

X = sm.add_constant(X)
y = monthly_kpi["delay_rate"]

model_interaction = sm.OLS(y, X).fit()
print(model_interaction.summary())

# Fit regression separately


# 2. Quantile Regression
import statsmodels.formula.api as smf

model_q50 = smf.quantreg("delay_rate ~ total_orders", monthly_kpi).fit(q=0.5)
model_q90 = smf.quantreg("delay_rate ~ total_orders", monthly_kpi).fit(q=0.9)

print(model_q50.summary())
print(model_q90.summary())

# 3. Robust Standard Errors
import statsmodels.api as sm

X = sm.add_constant(monthly_kpi["total_orders"])
y = monthly_kpi["delay_rate"]

model = sm.OLS(y, X).fit(cov_type="HC3")

print(model.summary())

# 4. Time Series Modeling
## Step1
from statsmodels.graphics.tsaplots import plot_acf
plot_acf(monthly_kpi["delay_rate"])

## Step2
from statsmodels.tsa.ar_model import AutoReg

model_ar = AutoReg(monthly_kpi["delay_rate"], lags=1).fit()
print(model_ar.summary())