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