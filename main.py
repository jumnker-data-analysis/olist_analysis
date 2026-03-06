from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ----------------------------
# Config
# ----------------------------
DATA_DIR = Path("data")
REPORT_DIR = Path("reports")
FIG_DIR = REPORT_DIR / "figures"

ORDERS_CSV = DATA_DIR / "olist_orders_dataset.csv"
OUT_MONTHLY_KPI = DATA_DIR / "monthly_kpi.csv"


# ----------------------------
# Helpers
# ----------------------------
def ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)


def load_orders(path: Path) -> pd.DataFrame:
# Parse important datetime columns in ONE read
    date_cols = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    ]
    return pd.read_csv(path, parse_dates=date_cols)


def build_delivered_table(orders: pd.DataFrame) -> pd.DataFrame:
    delivered = orders.loc[orders["order_status"] == "delivered"].copy()

# Delivery days: delivered_customer - purchase
    delivered["delivery_days"] = (
    delivered["order_delivered_customer_date"] - delivered["order_purchase_timestamp"]
    ).dt.days

# Delivery delay: delivered_customer - estimated_delivery
    delivered["delivery_delay"] = (
    delivered["order_delivered_customer_date"] - delivered["order_estimated_delivery_date"]
    ).dt.days

# Safe guards: drop rows where dates missing or negative weird values
    delivered = delivered.dropna(subset=["delivery_days", "delivery_delay"])
    return delivered


def build_monthly_kpi(delivered: pd.DataFrame) -> pd.DataFrame:
    delivered["purchase_month"] = delivered["order_purchase_timestamp"].dt.to_period("M")

    monthly_kpi = (
    delivered.groupby("purchase_month")
    .agg(
    total_orders=("order_id", "count"),
    avg_delivery_days=("delivery_days", "mean"),
    avg_delay=("delivery_delay", "mean"),
    delayed_orders=("delivery_delay", lambda x: (x > 0).sum()),
    )
    .reset_index()
    .sort_values("purchase_month")
    )

    monthly_kpi["delay_rate"] = monthly_kpi["delayed_orders"] / monthly_kpi["total_orders"]

# nice for plotting
    monthly_kpi["purchase_month_str"] = monthly_kpi["purchase_month"].astype(str)

    return monthly_kpi


def save_monthly_kpi(monthly_kpi: pd.DataFrame, out_path: Path) -> None:
    monthly_kpi.to_csv(out_path, index=False)


def plot_monthly_delay_rate(monthly_kpi: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 5))
    plt.plot(monthly_kpi["purchase_month_str"], monthly_kpi["delay_rate"])
    plt.xticks(rotation=45)
    plt.title("Monthly Delay Rate Trend")
    plt.xlabel("Purchase Month")
    plt.ylabel("Delay Rate")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "monthly_delay_rate_trend.png", dpi=300)
    plt.close()


def plot_monthly_avg_delay(monthly_kpi: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 5))
    plt.plot(monthly_kpi["purchase_month_str"], monthly_kpi["avg_delay"])
    plt.xticks(rotation=45)
    plt.title("Monthly Average Delivery Delay by Month")
    plt.xlabel("Purchase Month")
    plt.ylabel("Average Delivery Delay (days)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "monthly_avg_delivery_delay_trend.png", dpi=300)
    plt.close()


def plot_volume_vs_delayrate(monthly_kpi: pd.DataFrame) -> None:
    plt.figure(figsize=(7, 5))
    plt.scatter(monthly_kpi["total_orders"], monthly_kpi["delay_rate"])
    plt.title("Volume vs Delay Rate (Monthly)")
    plt.xlabel("Total Orders")
    plt.ylabel("Delay Rate")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "volume_vs_delay_rate.png", dpi=300)
    plt.close()


# ----------------------------
# Main
# ----------------------------
def main() -> None:
    ensure_dirs()

orders = load_orders(ORDERS_CSV)
delivered = build_delivered_table(orders)
monthly_kpi = build_monthly_kpi(delivered)

save_monthly_kpi(monthly_kpi, OUT_MONTHLY_KPI)

plot_monthly_delay_rate(monthly_kpi)
plot_monthly_avg_delay(monthly_kpi)
plot_volume_vs_delayrate(monthly_kpi)

print("✅ Saved:", OUT_MONTHLY_KPI)
print("✅ Figures saved to:", FIG_DIR)


if __name__ == "__main__":
    main()