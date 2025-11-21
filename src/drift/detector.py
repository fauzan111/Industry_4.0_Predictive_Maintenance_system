import pandas as pd
import numpy as np
from alibi_detect.cd import KolmogorovSmirnovDrift
from pathlib import Path
import joblib

PROCESSED_DATA_DIR = Path("data/processed")
MODELS_DIR = Path("models")

def fit_detector():
    print("Loading reference data...")
    train_df = pd.read_csv(PROCESSED_DATA_DIR / 'train_FD001_processed.csv')
    X_ref = train_df.drop('RUL', axis=1).values
    
    # Initialize drift detector
    # p_val=0.05 means we flag drift if p-value < 0.05
    print("Fitting drift detector...")
    cd = KolmogorovSmirnovDrift(X_ref, p_val=0.05)
    
    # Save detector
    # Alibi detect objects can be pickled, but sometimes require specific save/load methods
    # For simple KS drift, pickle/joblib is usually fine
    joblib.dump(cd, MODELS_DIR / "drift_detector.pkl")
    print("Drift detector saved.")

def check_drift(new_data):
    cd = joblib.load(MODELS_DIR / "drift_detector.pkl")
    preds = cd.predict(new_data)
    return preds

if __name__ == "__main__":
    fit_detector()
