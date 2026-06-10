"""
MODULE 1 — Customer Lifetime Value Prediction
Model   : Random Forest Regressor
Input   : customer_features.csv
Output  : CLV predictions + feature importance
"""

from pathlib import Path
import pandas as pd
import numpy as np
import pickle

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

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
    / "clv_model.pkl"
)

OUTPUT_FILE = (
    BASE_DIR
    / "outputs"
    / "clv_predictions.csv"
)

# =====================================================
# FEATURES
# =====================================================

FEATURES = [
    "purchase_frequency",
    "total_quantity",
    "unique_products",
    "days_since_last_purchase",
    "customer_lifespan_days",
    "avg_order_value",
]

TARGET = "total_revenue"

# =====================================================
# LOAD FEATURES
# =====================================================

def load_features(path=FEATURES_FILE):

    df = pd.read_csv(path)

    upper = df[TARGET].quantile(0.99)

    df = df[df[TARGET] <= upper].copy()

    print(
        f"[CLV] Loaded {len(df):,} customers  "
        f"(outliers trimmed above £{upper:,.0f})"
    )

    return df

# =====================================================
# TRAIN MODEL
# =====================================================

def train(df):

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        y_pred
    )

    r2 = r2_score(
        y_test,
        y_pred
    )

    print(f"[CLV] MAE : £{mae:,.2f}")
    print(
        f"[CLV] R²  : {r2:.4f}  "
        f"({r2*100:.1f}% variance explained)"
    )

    fi = (
        pd.Series(
            model.feature_importances_,
            index=FEATURES
        )
        .sort_values(ascending=False)
    )

    print("[CLV] Feature Importance:")

    for feat, imp in fi.items():

        bar = "█" * int(imp * 40)

        print(
            f"      {feat:<32} "
            f"{bar}  {imp:.3f}"
        )

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print(
        f"[CLV] Model saved → {MODEL_PATH}"
    )

    return model

# =====================================================
# PREDICT ALL CUSTOMERS
# =====================================================

def predict_all(df, model):

    df = df.copy()

    df["predicted_clv"] = (
        model.predict(df[FEATURES])
        .round(2)
    )

    p33 = df["predicted_clv"].quantile(0.33)
    p66 = df["predicted_clv"].quantile(0.66)

    df["clv_tier"] = pd.cut(
        df["predicted_clv"],
        bins=[-np.inf, p33, p66, np.inf],
        labels=[
            "Low",
            "Medium",
            "High"
        ]
    )

    return df[
        [
            "CustomerID",
            "total_revenue",
            "predicted_clv",
            "clv_tier"
        ]
        + FEATURES
    ]

# =====================================================
# SINGLE CUSTOMER PREDICTION
# =====================================================

def predict_single(
    purchase_frequency,
    total_quantity,
    unique_products,
    days_since_last_purchase,
    customer_lifespan_days,
    avg_order_value,
    model_path=MODEL_PATH
):

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    X = pd.DataFrame([
        {
            "purchase_frequency":
                purchase_frequency,

            "total_quantity":
                total_quantity,

            "unique_products":
                unique_products,

            "days_since_last_purchase":
                days_since_last_purchase,

            "customer_lifespan_days":
                customer_lifespan_days,

            "avg_order_value":
                avg_order_value,
        }
    ])

    return {
        "predicted_clv":
            round(
                float(model.predict(X)[0]),
                2
            )
    }

# =====================================================
# MAIN PIPELINE
# =====================================================

def run(
    features_path=FEATURES_FILE,
    output_path=OUTPUT_FILE
):

    print("\n" + "=" * 52)
    print("   MODULE 1 — CLV PREDICTION (Random Forest)")
    print("=" * 52)

    df = load_features(features_path)

    model = train(df)

    result = predict_all(
        df,
        model
    )

    Path(output_path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    result.to_csv(
        output_path,
        index=False
    )

    print(
        f"[CLV] Predictions saved → {output_path}"
    )

    return result

# =====================================================

if __name__ == "__main__":
    run()