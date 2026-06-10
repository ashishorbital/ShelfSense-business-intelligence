from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUTS_DIR = BASE_DIR / "outputs"



CLV_FILE = BASE_DIR / "outputs" / "clv_predictions.csv"
SEG_FILE = BASE_DIR / "outputs" / "customer_segments.csv"
FORECAST_FILE = BASE_DIR / "outputs" / "forecast.csv"
RULES_FILE = BASE_DIR / "outputs" / "association_rules.csv"


def get_kpis():

    clv = pd.read_csv(
        OUTPUTS_DIR / "clv_predictions.csv"
    )

    seg = pd.read_csv(
        OUTPUTS_DIR / "customer_segments.csv"
    )

    forecast = pd.read_csv(
        OUTPUTS_DIR / "forecast.csv"
    )

    return {

        "customers":
            int(len(clv)),

        "vip_customers":
            int(
                (
                    seg["segment"]
                    == "VIP Customer"
                ).sum()
            ),

        "avg_clv":
            round(
                clv["predicted_clv"]
                .mean(),
                2
            ),

        "forecast_revenue":
            round(
                forecast[
                    "predicted_revenue"
                ].sum(),
                2
            ),

        "avg_order_value":
            round(
                clv[
                    "avg_order_value"
                ].mean(),
                2
            ),

        "avg_purchase_frequency":
            round(
                clv[
                    "purchase_frequency"
                ].mean(),
                2
            )
    }


def get_segments():

    seg = pd.read_csv(SEG_FILE)

    return (
        seg["segment"]
        .value_counts()
        .to_dict()
    )


def get_forecast():

    forecast = pd.read_csv(FORECAST_FILE)

    return forecast.to_dict(
        orient="records"
    )


def get_recommendations(product):

    rules = pd.read_csv(
        OUTPUTS_DIR / "association_rules.csv"
    )

    mask = rules["antecedents"] \
        .str.contains(
            product.upper(),
            case=False,
            na=False
        )

    results = rules[mask] \
        .sort_values(
            "lift",
            ascending=False
        ) \
        .head(10)

    recommendations = []

    for _, row in results.iterrows():

        recommendations.append({

            "product":
                str(row["consequents"]),

            "confidence":
                round(
                    float(row["confidence"]),
                    4
                ),

            "lift":
                round(
                    float(row["lift"]),
                    2
                ),

            "support":
                round(
                    float(row["support"]),
                    4
                )
        })

    return recommendations


def get_clv(customer_id):

    df = pd.read_csv(
        OUTPUTS_DIR / "clv_predictions.csv"
    )

    customer = df[
        df["CustomerID"] == customer_id
    ]

    if customer.empty:

        return {
            "found": False,
            "message": "Customer not found"
        }

    row = customer.iloc[0]

    return {

        "found": True,

        "customer_id":
            int(row["CustomerID"]),

        "predicted_clv":
            round(
                float(row["predicted_clv"]),
                2
            ),

        "tier":
            str(row["clv_tier"]),

        "total_revenue":
            round(
                float(row["total_revenue"]),
                2
            ),

        "purchase_frequency":
            int(row["purchase_frequency"]),

        "avg_order_value":
            round(
                float(row["avg_order_value"]),
                2
            ),

        "days_since_last_purchase":
            int(row["days_since_last_purchase"]),

        "unique_products":
            int(row["unique_products"])
    }


def get_segment_summary():

    seg = pd.read_csv(SEG_FILE)

    summary = (
        seg["segment"]
        .value_counts()
        .reset_index()
    )

    summary.columns = [
        "segment",
        "count"
    ]

    return summary.to_dict(
        orient="records"
    )

def get_segment_analytics():

    seg = pd.read_csv(
        OUTPUTS_DIR /
        "customer_segments.csv"
    )

    result = (
        seg.groupby("segment")
        .agg(
            customers=("CustomerID", "count"),
            avg_revenue=("total_revenue", "mean"),
            avg_frequency=("purchase_frequency", "mean"),
            avg_recency=("days_since_last_purchase", "mean")
        )
        .round(2)
        .reset_index()
    )

    return result.to_dict(
        orient="records"
    )

def get_forecast_summary():

    fc = pd.read_csv(
        OUTPUTS_DIR / "forecast.csv"
    )

    total = fc["predicted_revenue"].sum()

    avg = fc["predicted_revenue"].mean()

    best_row = fc.loc[
        fc["predicted_revenue"].idxmax()
    ]

    worst_row = fc.loc[
        fc["predicted_revenue"].idxmin()
    ]

    volatility = (
        fc["predicted_revenue"].std()
        / avg
    ) * 100

    return {

        "forecast_revenue":
            round(total, 2),

        "average_daily":
            round(avg, 2),

        "best_day":
            round(
                best_row["predicted_revenue"],
                2
            ),

        "best_day_date":
            str(best_row["date"]),

        "worst_day":
            round(
                worst_row["predicted_revenue"],
                2
            ),

        "worst_day_date":
            str(worst_row["date"]),

        "volatility":
            round(volatility, 2)
    }

def get_products():

    rules = pd.read_csv(
        OUTPUTS_DIR / "association_rules.csv"
    )

    products = []

    for item in rules["antecedents"]:

        for product in str(item).split(","):

            products.append(
                product.strip()
            )

    return sorted(
        list(set(products))
    )
