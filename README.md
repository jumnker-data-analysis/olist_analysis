# Olist Delivery Performance Analysis

## Project Overview

This project analyzes delivery performance using the Olist e-commerce dataset.
The goal is to understand operational factors affecting delivery delays, build a clean analytical pipeline for KPI generation, and extend the analisis with revenue-based metrics such as Avereage Order Value (AOV) and visualization.

The project demonstrates a typical **data analyst workflow**:

Raw Data → Data Cleaning → KPI Generation → Statistical Analysis → Dashboard Visualization → Business Insights

---

# Objectives

The main objectives of this project are:

• Build a clean and reproducible **data processing pipeline** using Python
• Analyze **delivery performance trends over time**
• Identify factors influencing **delivery delay rate**
• Generate monthly operational KPIs for dashboard reporting
• Support business decision-making through data insights
• Explore revenue-based KPIs such as monthly Avereage Order Value (AOV)

---

# Tech Stack

Python (Pandas, Numpy)

Data Visualization
• Matplotlib
• Power BI
Statistical Modeling
• Scikit-learn
• Statsmodels
Tools
• VS Code
• Git / GitHub

---

# Project Structure
olist_analysis

data/

raw datasets
mothly_kpi.csv -> clean KPI dataset

notebooks/

aov_exploration.ipynb -> delivered-order AOV exploration
aov_exploration_monthly.ipynb -> monthly AOV exploration and validation

analysis/

regression.py -> regression models and diagnostics

reports/

figures and charts

main.py ->data pipeline script




README.md

---

# Data Pipeline

The data pipeline is implemented in **main.py**.

Key steps:

1. Load raw datasets
2. Parse datetime columns
3. Filter delivered orders
4. Calculate delivery time metrics
5. Aggregate monthly performance KPIs
6. Export clean dataset for visualization

Example KPI generation:

monthly = delivered.groupby(“purchase_month”).agg(

total_orders=(“order_id”,“count”),

avg_delivery_days=(“delivery_days”,“mean”),

avg_delay=(“delivery_delay”,“mean”),

delayed_orders=(“delivery_delay”,lambda x:(x>0).sum())

)

---

# Key Metrics

The project calculates the following operational metrics:

| Metric | Description |
|------|-------------|
| total_orders | number of orders per month |
| avg_delivery_days | average delivery time |
| avg_delay | average delivery delay |
| delayed_orders | number of delayed orders |
| delay_rate | percentage of delayed deliveries |
| aov | average order value for delivered orders with valid payment records|

---

# Data Notes

Monthly AOV is calculated using delivered orders matched to payment records.
Some early months may appear in the order-based KPI dataset but be excluded from AOV analysis if matching payment records are unavailable.

---

# Statistical Analysis

Several regression models were tested to understand delivery delay behavior.

Models explored:

• Linear regression
• Log-transformed order volume
• Interaction models
• Ridge regression
• Weighted regression

Model diagnostics included:

• Residual analysis
• Heteroskedasticity observation
• Autocorrelation testing (ACF)

---

# Key Insights

Initial analysis suggests:

• Delivery delay is **not strongly driven by order volume alone**

• Higher **average delivery days strongly correlates with delay rate**

• Operational issues may be related to:

- warehouse processing efficiency
- logistics bottlenecks
- delivery network capacity

These insights suggest delay performance may be driven by **multiple compounded operational factors**.

---

# Visualization

A Power BI dashboard was created using the generated KPI dataset.

Dashboard pages include:

Page 1 – Delivery Performance Overview
• Total orders
• Delay rate trend
• Average delivery days

Page 2 – Operational Drivers
• Order volume vs delay rate
• Delivery performance trends

---

# Future Improvements

Potential extensions for deeper analysis:

• Regime segmentation (high vs low volume periods)
• Quantile regression
• Robust standard errors
• Time-series modeling
• More detailed operational feature engineering

---

# Learning Outcomes

This project demonstrates the ability to:

• build a reproducible data pipeline
• perform exploratory data analysis
• apply regression modeling
• create business-oriented insights
• present results through dashboards

---

# Author

Leo
Aspiring Data Analyst

Background:
• Taiwanese
• 11 years living in Sydney
• Currently based in Bangkok
• Transitioning into data analytics

Focus areas:
Python • Data Analysis • Visualization • Business Insights

---