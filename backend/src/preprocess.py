# src/preprocess.py
import pandas as pd

def daily_to_monthly(df):
    """
    Aggregate daily data to monthly. Returns monthly dataframe with:
    - date (month end)
    - monthly_rides (sum)
    - monthly_revenue (sum)
    - monthly_avg_fare (mean)
    - top_category (most frequent category in that month)
    """
    df = df.copy()

    # Ensure datetime & sorting (important)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    df.set_index("date", inplace=True)

    agg = (
        df.resample("ME")
        .agg({
            "daily_rides": "sum",
            "daily_revenue": "sum",
            "avg_fare": "mean",
            "ride_category": lambda x: x.mode().iat[0] if not x.mode().empty else x.iloc[0]
        })
        .rename(columns={
            "daily_rides": "monthly_rides",
            "daily_revenue": "monthly_revenue",
            "avg_fare": "monthly_avg_fare",
            "ride_category": "top_category"
        })
        .reset_index()
    )

    agg["year"] = agg["date"].dt.year
    agg["month"] = agg["date"].dt.month

    return agg
