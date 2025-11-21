import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from pathlib import Path
import joblib

PROCESSED_DATA_DIR = Path("data/processed")
MODELS_DIR = Path("models")
MODELS_DIR.mkdir(exist_ok=True)

print("Loading data...")
train_df = pd.read_csv(PROCESSED_DATA_DIR / 'train_FD001_processed.csv')
test_df = pd.read_csv(PROCESSED_DATA_DIR / 'test_FD001_processed.csv')

X_train = train_df.drop('RUL', axis=1)
y_train = train_df['RUL']
X_test = test_df.drop('RUL', axis=1)
y_test = test_df['RUL']

print(f"Training data shape: {X_train.shape}")
print(f"Test data shape: {X_test.shape}")

print("\nTraining Random Forest model...")
rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)

print("\nMaking predictions...")
predictions = rf.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

print(f"\n✅ Model Performance:")
print(f"   RMSE: {rmse:.2f} cycles")
print(f"   R² Score: {r2:.4f}")

# Save model
joblib.dump(rf, MODELS_DIR / "rf_model.pkl")
print(f"\n✅ Model saved to {MODELS_DIR / 'rf_model.pkl'}")

# Show sample predictions
print("\n📊 Sample Predictions (first 5):")
print("Actual RUL | Predicted RUL | Error")
print("-" * 40)
for i in range(5):
    error = abs(y_test.iloc[i] - predictions[i])
    print(f"{y_test.iloc[i]:10.1f} | {predictions[i]:13.1f} | {error:5.1f}")
