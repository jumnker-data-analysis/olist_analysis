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

print("\nDelivery columns preview:")
print(delivered[["delivery_days","delivery_delay"]].head(10))

print("\nDelivery_days summary:")
print(delivered["delivery_days"].describe())

print("\nDelivery_delay summary:")
print(delivered["delivery_delay"].describe())

# step 2 KPI + monthly trend (Power BI friendly)

