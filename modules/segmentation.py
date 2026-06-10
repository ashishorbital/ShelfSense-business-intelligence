"""
MODULE 2 — Customer Segmentation
Model   : K-Means Clustering (RFM-based)
Input   : customer_features.csv
Output  : customer_segments.csv (VIP / Regular / Low Value)
"""

from pathlib import Path
import pandas as pd
import pickle

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# =====================================================
# PATH CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

FEATURES_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "customer_features.csv"
)

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "segmentation_model.pkl"
)

OUTPUT_FILE = (
    BASE_DIR
    / "outputs"
    / "customer_segments.csv"
)

# =====================================================
# RFM FEATURES
# =====================================================

RFM_FEATURES = [
    "days_since_last_purchase",
    "purchase_frequency",
    "total_revenue",
]

# =====================================================
# LOAD FEATURES
# =====================================================

def load_features(path=FEATURES_FILE):

    df = pd.read_csv(path)

    upper = df["total_revenue"].quantile(0.99)

    df = df[
        df["total_revenue"] <= upper
    ].copy()

    print(
        f"[SEG] Loaded {len(df):,} customers"
    )

    return df

# =====================================================
# TRAIN MODEL
# =====================================================

def train(df):

    X = df[RFM_FEATURES].copy()

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(
        n_clusters=3,
        init="k-means++",
        n_init=20,
        random_state=42
    )

    labels = kmeans.fit_predict(X_scaled)

    df = df.copy()

    df["cluster"] = labels

    cluster_summary = (
        df.groupby("cluster")["total_revenue"]
        .mean()
        .sort_values(ascending=False)
    )

    tier_names = [
        "VIP Customer",
        "Regular Customer",
        "Low Value Customer"
    ]

    label_map = {}

    for i, cluster_id in enumerate(
        cluster_summary.index
    ):
        label_map[cluster_id] = tier_names[i]

    df["segment"] = (
        df["cluster"]
        .map(label_map)
    )

    print("[SEG] Cluster Summary:")

    summary = (
        df.groupby("segment")
        .agg(
            count=(
                "CustomerID",
                "count"
            ),
            avg_revenue=(
                "total_revenue",
                "mean"
            ),
            avg_frequency=(
                "purchase_frequency",
                "mean"
            ),
            avg_recency_days=(
                "days_since_last_purchase",
                "mean"
            ),
        )
        .round(1)
    )

    print(summary.to_string())

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(MODEL_PATH, "wb") as f:

        pickle.dump(
            {
                "kmeans": kmeans,
                "scaler": scaler,
                "label_map": label_map
            },
            f
        )

    print(
        f"[SEG] Model saved → {MODEL_PATH}"
    )

    return df

# =====================================================
# SINGLE CUSTOMER PREDICTION
# =====================================================

def predict_single(
    days_since_last_purchase,
    purchase_frequency,
    total_revenue,
    model_path=MODEL_PATH
):

    with open(model_path, "rb") as f:

        bundle = pickle.load(f)

    kmeans = bundle["kmeans"]
    scaler = bundle["scaler"]
    label_map = bundle["label_map"]

    X = scaler.transform(
        [[
            days_since_last_purchase,
            purchase_frequency,
            total_revenue
        ]]
    )

    cluster = int(
        kmeans.predict(X)[0]
    )

    return {
        "cluster": cluster,
        "segment": label_map[cluster]
    }

# =====================================================
# MAIN PIPELINE
# =====================================================

def run(
    features_path=FEATURES_FILE,
    output_path=OUTPUT_FILE
):

    print("\n" + "=" * 52)
    print("   MODULE 2 — CUSTOMER SEGMENTATION (K-Means)")
    print("=" * 52)

    df = load_features(features_path)

    result = train(df)

    cols = [
        "CustomerID",
        "segment",
        "cluster",
        "days_since_last_purchase",
        "purchase_frequency",
        "total_revenue",
        "unique_products",
        "avg_order_value",
        "customer_lifespan_days"
    ]

    result = result[
        [
            c for c in cols
            if c in result.columns
        ]
    ]

    Path(output_path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    result.to_csv(
        output_path,
        index=False
    )

    print(
        f"[SEG] Segments saved → {output_path}"
    )

    return result

# =====================================================

if __name__ == "__main__":
    run()