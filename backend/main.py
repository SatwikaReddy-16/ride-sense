# backend/main.py
import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from typing import Optional

CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "ride_dataset.csv")

app = FastAPI(title="RideSense API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class YM(BaseModel):
    year: int
    month: int


# ----------------------------
# Helper: block past months
# ----------------------------
def is_past_year_month(year: int, month: int) -> bool:
    today = pd.Timestamp.today().replace(day=1)
    selected = pd.Timestamp(year=year, month=month, day=1)
    return selected < today


# ----------------------------
# Load CSV once
# ----------------------------
_df: Optional[pd.DataFrame] = None
if os.path.exists(CSV_PATH):
    try:
        _df = pd.read_csv(CSV_PATH, low_memory=False)

        if "date" in _df.columns:
            _df["date"] = pd.to_datetime(_df["date"], errors="coerce")
            _df["year"] = _df["date"].dt.year
            _df["month"] = _df["date"].dt.month
            _df["ym"] = _df["date"].dt.to_period("M").dt.to_timestamp()
        elif "year" in _df.columns and "month" in _df.columns:
            _df["ym"] = pd.to_datetime(_df[["year", "month"]].assign(day=1))
        else:
            _df["ym"] = pd.NaT

        print("CSV loaded:", CSV_PATH)
    except Exception as e:
        print("CSV load failed:", e)
        _df = None
else:
    print("CSV not found:", CSV_PATH)
    _df = None


# ----------------------------
# Monthly aggregation
# ----------------------------
def _aggregate_monthly(df: pd.DataFrame):
    df = df.copy()

    if "daily_revenue" not in df.columns and "revenue" in df.columns:
        df["daily_revenue"] = df["revenue"]
    if "daily_rides" not in df.columns and "total_rides" in df.columns:
        df["daily_rides"] = df["total_rides"]

    df["daily_revenue"] = pd.to_numeric(df.get("daily_revenue"), errors="coerce")
    df["daily_rides"] = pd.to_numeric(df.get("daily_rides"), errors="coerce")

    agg = df.groupby(["year", "month"]).agg(
        avg_daily_revenue=("daily_revenue", "mean"),
        avg_daily_rides=("daily_rides", "mean"),
        top_category=("ride_category", lambda x: x.mode().iat[0] if not x.mode().empty else "Unknown")
    ).reset_index()

    return agg


def _project_value_by_year(years, values, target_year):
    try:
        x = np.array(years, dtype=float)
        y = np.array(values, dtype=float)
        mask = np.isfinite(x) & np.isfinite(y)
        x, y = x[mask], y[mask]

        if len(x) <= 1:
            return float(np.nanmean(y))

        coef = np.polyfit(x, y, 1)
        return float(np.polyval(coef, target_year))
    except Exception:
        return float("nan")


# ----------------------------
# Predict single month
# ----------------------------
@app.post("/predict")
async def predict(payload: YM):
    year, month = payload.year, payload.month

    if is_past_year_month(year, month) or _df is None or _df.empty:
        return {
            "predicted_revenue": 0,
            "predicted_rides": 0,
            "predicted_top_category": "Unknown",
        }

    monthly = _aggregate_monthly(_df)
    exact = monthly[(monthly.year == year) & (monthly.month == month)]

    if not exact.empty:
        return {
            "predicted_revenue": float(exact.avg_daily_revenue.iloc[0] * 30),
            "predicted_rides": int(round(exact.avg_daily_rides.iloc[0] * 30)),
            "predicted_top_category": exact.top_category.iloc[0],
        }

    same_month = monthly[monthly.month == month]
    if same_month.empty:
        return {
            "predicted_revenue": 0,
            "predicted_rides": 0,
            "predicted_top_category": "Unknown",
        }

    proj_rev = _project_value_by_year(
        same_month.year, same_month.avg_daily_revenue, year
    )
    proj_rides = _project_value_by_year(
        same_month.year, same_month.avg_daily_rides, year
    )

    cat = same_month.sort_values("year", ascending=False).top_category.iloc[0]

    return {
        "predicted_revenue": max(0, float(proj_rev * 30)) if pd.notna(proj_rev) else 0,
        "predicted_rides": max(0, int(round(proj_rides * 30))) if pd.notna(proj_rides) else 0,
        "predicted_top_category": cat or "Unknown",
    }


# ----------------------------
# Predict future series (chart)
# ----------------------------
@app.post("/predict_series")
async def predict_series(payload: YM):
    year, month = payload.year, payload.month
    today = pd.Timestamp.today().replace(day=1)

    results = []
    y, m = year, month

    for _ in range(12):
        ts = pd.Timestamp(year=y, month=m, day=1)
        label = ts.strftime("%b %Y")

        if ts < today:
            results.append({
                "label": label,
                "rides": 0,
                "revenue": 0
            })
        else:
            res = await predict(YM(year=y, month=m))
            results.append({
                "label": label,
                "rides": res["predicted_rides"],
                "revenue": res["predicted_revenue"]
            })

        m += 1
        if m > 12:
            m = 1
            y += 1

    return {"history": results}
