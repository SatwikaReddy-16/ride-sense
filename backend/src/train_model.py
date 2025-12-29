# src/train_model.py
from pathlib import Path
import joblib
import numpy as np
from xgboost import XGBRegressor, XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, accuracy_score

from src.load_data import load_raw
from src.preprocess import daily_to_monthly

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    denom = np.where(y_true == 0, 1e-8, y_true)
    return np.mean(np.abs((y_true - y_pred) / denom)) * 100

def train_and_save():
    df = load_raw()
    monthly = daily_to_monthly(df)

    X = monthly[["year", "month", "monthly_avg_fare"]]
    y_revenue = monthly["monthly_revenue"]
    y_rides = monthly["monthly_rides"]
    y_cat = monthly["top_category"]

    # last 6 months as test
    if len(monthly) > 12:
        X_train = X.iloc[:-6]
        X_test = X.iloc[-6:]
        rev_train = y_revenue.iloc[:-6]
        rev_test = y_revenue.iloc[-6:]
        rides_train = y_rides.iloc[:-6]
        rides_test = y_rides.iloc[-6:]
        cat_train = y_cat.iloc[:-6]
        cat_test = y_cat.iloc[-6:]
    else:
        from sklearn.model_selection import train_test_split
        X_train, X_test, rev_train, rev_test = train_test_split(
            X, y_revenue, test_size=0.2, shuffle=False
        )
        _, _, rides_train, rides_test = train_test_split(
            X, y_rides, test_size=0.2, shuffle=False
        )
        _, _, cat_train, cat_test = train_test_split(
            X, y_cat, test_size=0.2, shuffle=False
        )

    # Regression models
    rev_model = XGBRegressor(
        n_estimators=200,
        objective="reg:squarederror",
        random_state=42,
        verbosity=0
    )
    rides_model = XGBRegressor(
        n_estimators=200,
        objective="reg:squarederror",
        random_state=42,
        verbosity=0
    )

    rev_model.fit(X_train, rev_train)
    rides_model.fit(X_train, rides_train)

    # Classification model
    lbl = LabelEncoder()
    y_cat_train_enc = lbl.fit_transform(cat_train)
    y_cat_test_enc = lbl.transform(cat_test)

    # inject label noise (~5%)
    rng = np.random.default_rng(42)
    n_noise = max(1, int(0.05 * len(y_cat_train_enc))) if len(y_cat_train_enc) > 0 else 0
    y_cat_train_noisy = y_cat_train_enc.copy()

    if n_noise > 0:
        idx = rng.choice(len(y_cat_train_enc), size=n_noise, replace=False)
        random_labels = rng.integers(0, len(lbl.classes_), size=n_noise)
        y_cat_train_noisy[idx] = random_labels

    cat_model = XGBClassifier(
        n_estimators=30,
        max_depth=2,
        subsample=0.6,
        colsample_bytree=0.6,
        reg_alpha=2.0,
        reg_lambda=2.0,
        objective="multi:softmax",
        num_class=len(lbl.classes_),
        random_state=42,
        verbosity=0
    )

    cat_model.fit(X_train, y_cat_train_noisy)

    # Metrics
    rev_pred = rev_model.predict(X_test)
    rides_pred = rides_model.predict(X_test)
    cat_pred_enc = cat_model.predict(X_test)

    print("Revenue MAE:", mean_absolute_error(rev_test, rev_pred))
    print("Rides MAE:", mean_absolute_error(rides_test, rides_pred))
    print("Revenue MAPE (%):", mean_absolute_percentage_error(rev_test, rev_pred))
    print("Rides MAPE (%):", mean_absolute_percentage_error(rides_test, rides_pred))
    print("Category accuracy:", accuracy_score(y_cat_test_enc, cat_pred_enc))

    # Save models
    joblib.dump(rev_model, MODEL_DIR / "revenue_model.joblib")
    joblib.dump(rides_model, MODEL_DIR / "rides_model.joblib")
    joblib.dump(cat_model, MODEL_DIR / "category_model.joblib")
    joblib.dump(lbl, MODEL_DIR / "category_label_encoder.joblib")

if __name__ == "__main__":
    train_and_save()
