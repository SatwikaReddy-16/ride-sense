import pandas as pd
import os

def load_raw():
    # Load CSV directly from the same folder as this file
    file_path = os.path.join(os.path.dirname(__file__), "ride_dataset.csv")

    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    return df
