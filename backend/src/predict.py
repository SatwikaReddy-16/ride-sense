# src/predict.py
from pathlib import Path
from datetime import date
import joblib
import pandas as pd

from src.load_data import load_raw
from src.preprocess import daily_to_monthly

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

def load_models():
    rev = joblib.load(MODEL_DIR / "revenue_model.joblib")
    rides = joblib.load(MODEL_DIR / "rides_model.joblib")
    cat = joblib.load(MODEL_DIR / "category_model.joblib")
    lbl = joblib.load(MODEL_DIR / "category_label_encoder.joblib")
    return rev, rides, cat, lbl

def predict_for_month(year: int, month: int):
    today = date.today()

    # allow current and future only
    if (year < today.year) or (year == today.year and month < today.month):
        return {
            "year": year,
            "month": month,
            "predicted_revenue": 0,
            "predicted_rides": 0,
            "predicted_top_category": None
        }

    df = load_raw()
    monthly = daily_to_monthly(df)

    if not monthly.empty:
        last_avg = monthly["monthly_avg_fare"].iloc[-1]
    else:
        last_avg = df["avg_fare"].mean()

    X_new = pd.DataFrame([{
        "year": year,
        "month": month,
        "monthly_avg_fare": last_avg
    }])

    rev_model, rides_model, cat_model, lbl = load_models()

    rev_pred = float(rev_model.predict(X_new)[0])
    rides_pred = float(rides_model.predict(X_new)[0])

    cat_pred_enc = cat_model.predict(X_new)[0]
    cat_pred = lbl.inverse_transform([cat_pred_enc])[0]

    return {
        "year": year,
        "month": month,
        "predicted_revenue": rev_pred,
        "predicted_rides": rides_pred,
        "predicted_top_category": cat_pred
    }

if __name__ == "__main__":
    print(predict_for_month(2025, 12))
