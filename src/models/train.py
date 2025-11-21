import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import mlflow
import mlflow.sklearn
import argparse
from pathlib import Path
import joblib

PROCESSED_DATA_DIR = Path("data/processed")
MODELS_DIR = Path("models")
MODELS_DIR.mkdir(exist_ok=True)

def load_data():
    train_df = pd.read_csv(PROCESSED_DATA_DIR / 'train_FD001_processed.csv')
    test_df = pd.read_csv(PROCESSED_DATA_DIR / 'test_FD001_processed.csv')
    
    X_train = train_df.drop('RUL', axis=1)
    y_train = train_df['RUL']
    X_test = test_df.drop('RUL', axis=1)
    y_test = test_df['RUL']
    
    return X_train, y_train, X_test, y_test

def train(n_estimators=100, max_depth=None):
    X_train, y_train, X_test, y_test = load_data()
    
    with mlflow.start_run():
        # Log parameters
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("model_type", "RandomForestRegressor")
        
        print(f"Training RandomForest with n_estimators={n_estimators}, max_depth={max_depth}...")
        rf = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        rf.fit(X_train, y_train)
        
        # Predict
        predictions = rf.predict(X_test)
        
        # Metrics
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        r2 = r2_score(y_test, predictions)
        
        print(f"RMSE: {rmse}")
        print(f"R2: {r2}")
        
        # Log metrics
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        
        # Log model
        mlflow.sklearn.log_model(rf, "model")
        
        # Save locally
        joblib.dump(rf, MODELS_DIR / "rf_model.pkl")
        print("Model saved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--max_depth", type=int, default=None)
    parser.add_argument("--tracking_uri", type=str, default=None)
    args = parser.parse_args()
    
    if args.tracking_uri:
        mlflow.set_tracking_uri(args.tracking_uri)
        
    train(n_estimators=args.n_estimators, max_depth=args.max_depth)
