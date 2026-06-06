# Olist Delivery Performance Analysis

## Project Overview

This project analyzes delivery performance using the Olist Brazil e-commerce dataset.

The goal is to understand delivery delays, build a clean Python data pipeline, generate monthly KPI metrics, and create dashboard-ready outputs for business reporting.

This project demonstrates a practical data analyst workflow:

Raw Data → Data Cleaning → KPI Generation → Exploratory Analysis → Statistical Modeling → Dashboard Visualization → Business Insights

---

## Business Problem

E-commerce delivery performance directly affects customer satisfaction, repeat purchases, and operational efficiency.

### This project explores:

- How delivery performance changes over time
- Whether order volume is strongly related to delivery delays
- Which operational metrics are useful for dashboard reporting
- How delivery data can support business decision-making

---

## Objectives

- Build a reproducible data processing pipeline using Python
- Clean and transform delivery-related order data
- Calculate delivery KPIs such as average delivery days, delay rate, and average delay
- Explore the relationship between order volume and delivery delays
- Create dashboard-ready datasets for Excel and Power BI
- Generate business insights for operational improvement

---

## Tools & Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Statsmodels
- Excel
- Power BI
- VS Code
- Git / GitHub

---

## Project Structure


olist_analysis/
├── data/
│ ├── raw/
│ └── processed/
├── notebooks/
│ ├── delivery_delay_exploration.ipynb
│ ├── aov_exploration.ipynb
│ └── kpi_state_exploration.ipynb
├── analysis/
│ ├── regression.py
│ └── model_experiments.md
├── reports/
│ └── figures/
├── excel/
│ └── monthly_kpi_dashboard.xlsx
├── powerbi/
├── main.py
├── requirements.txt
└── README.md

---

## Data Pipeline

The main data pipeline is implemented in main.py.

### Key steps:

Load raw datasets
Parse datetime columns
Filter delivered orders
Calculate delivery time and delay metrics
Aggregate monthly KPI metrics
Export processed data for dashboard visualization

---

## Key Metrics

| Metric | Description | 
| :------ | :----------- | 
| total_orders | Number of delivered orders per month
| avg_delivery_days | Average number of days from purchase to delivery |
| avg_delay | Average difference between actual and estimated delivery date |
| delayed_orders | Number of orders delivered later than estimated |
| delay_rate | Percentage of delayed deliveries |
| aov | Average order value for delivered orders with valid payment records |

---

## Analysis Performed

### Delivery Performance Analysis

Monthly delivery trend analysis
- Average delivery days
- Late delivery rate
- Delay behavior over time

### Revenue-Based Analysis

- Average order value exploration
- Delivered-order revenue analysis
- Monthly AOV validation

### Statistical Modeling

Several regression models were tested to understand delivery delay behavior:
- Linear regression
- Log-transformed order volume model
- Interaction models
- Ridge regression
- Weighted regression
### Model diagnostics included:

- Residual analysis
- Heteroskedasticity observation
- Autocorrelation testing using ACF

---

## Key Insights
- Delivery delays are not primarily driven by order volume, suggesting that operational inefficiencies may be more important than demand spikes.
- Higher average delivery time is strongly associated with higher delay rates.
- Delivery performance is likely influenced by multiple operational factors, including warehouse processing time, logistics bottlenecks, and delivery capacity constraints.
- Delay behavior cannot be explained by a single variable, so future analysis should include more operational features.
- Dashboard KPIs help translate delivery performance into clear business insights for decision-making.

---

## Visualization
Dashboard outputs were created using Excel and Power BI.

### Dashboard sections include:

- Total orders
- Monthly delay rate trend
- Average delivery days
- Order volume vs delay rate
- Delivery performance trend
- Key operational insights

---

## Business Recommendations

- Monitor delay rate as a core operational KPI.
- Investigate months with unusually high delay rates.
- Compare delivery performance by region, seller, and logistics route in future analysis.
- Use dashboard reporting to identify early warning signs of delivery issues.
- Improve operational data collection to better explain delay drivers.

---

## Future Improvements

### Potential next steps:

- Add state-level delivery performance analysis
- Add seller-level delivery performance
- Build a full Power BI dashboard version
- Add time-series analysis
- Add robust regression methods
- Improve dashboard design and storytelling
- Add more detailed operational features

---

## Learning Outcomes

### This project demonstrates the ability to:

- Build a reproducible Python data pipeline
- Clean and transform real-world e-commerce data
- Generate business KPIs
- Perform exploratory analysis
- Apply basic statistical modeling
- Create dashboard-ready datasets
- Communicate insights clearly for business decision-making

---

## Author
Yu-Jheng Su (Leo)

Aspiring Data Analyst based in Bangkok, Thailand.

### Background:

- Taiwanese
- 11 years of professional experience in Sydney, Australia
- Transitioning into data analytics and business intelligence

### Focus areas:
Python1 • SQL • Excel • Power BI • Data Analysis • Business Insights