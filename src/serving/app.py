from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

app = FastAPI(title="Predictive Maintenance API", version="1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and scaler
MODEL_PATH = Path("models/rf_model.pkl")
SCALER_PATH = Path("data/processed/scaler.pkl")

model = None
scaler = None

@app.on_event("startup")
def load_artifacts():
    global model, scaler
    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)
    if SCALER_PATH.exists():
        scaler = joblib.load(SCALER_PATH)

class SensorData(BaseModel):
    setting_1: float
    setting_2: float
    setting_3: float
    s_2: float
    s_3: float
    s_4: float
    s_6: float
    s_7: float
    s_8: float
    s_9: float
    s_11: float
    s_12: float
    s_13: float
    s_14: float
    s_15: float
    s_17: float
    s_20: float
    s_21: float

@app.get("/")
def health_check():
    return {"status": "healthy"}

@app.post("/predict")
def predict(data: SensorData):
    if not model or not scaler:
        raise HTTPException(status_code=503, detail="Model or scaler not loaded")
    
    # Convert input to dataframe
    input_dict = data.dict()
    
    # Define the correct column order (matching training data)
    # The scaler expects: unit_nr, time_cycles, setting_1, setting_2, setting_3, then sensors
    # But we don't have unit_nr and time_cycles for prediction, so we use the features the scaler was fit on
    feature_order = ['setting_1', 'setting_2', 'setting_3', 's_2', 's_3', 's_4', 's_6', 's_7', 's_8', 's_9', 's_11', 's_12', 's_13', 's_14', 's_15', 's_17', 's_20', 's_21']
    
    # Create dataframe with correct column order
    input_data = pd.DataFrame([[input_dict[col] for col in feature_order]], columns=feature_order)
    
    # Normalize
    try:
        scaled_data = scaler.transform(input_data)
        prediction = model.predict(scaled_data)
        return {"RUL": float(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
