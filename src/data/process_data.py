import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path
import joblib

RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Define columns
INDEX_NAMES = ['unit_nr', 'time_cycles']
SETTING_NAMES = ['setting_1', 'setting_2', 'setting_3']
SENSOR_NAMES = ['s_{}'.format(i) for i in range(1, 22)] 
COL_NAMES = INDEX_NAMES + SETTING_NAMES + SENSOR_NAMES

# Sensors to drop (constant or low variance based on EDA)
SENSORS_TO_DROP = ['s_1', 's_5', 's_10', 's_16', 's_18', 's_19']
FEATURE_COLS = [c for c in SENSOR_NAMES if c not in SENSORS_TO_DROP] + SETTING_NAMES

def load_data(filename):
    path = RAW_DATA_DIR / filename
    return pd.read_csv(path, sep='\s+', header=None, names=COL_NAMES)

def calculate_rul_train(df):
    # Calculate RUL for training data (max cycle - current cycle)
    max_cycle = df.groupby('unit_nr')['time_cycles'].max().reset_index()
    max_cycle.columns = ['unit_nr', 'max_cycle']
    df = df.merge(max_cycle, on='unit_nr', how='left')
    df['RUL'] = df['max_cycle'] - df['time_cycles']
    df.drop('max_cycle', axis=1, inplace=True)
    return df

def process_data():
    print("Loading data...")
    train_df = load_data('train_FD001.txt')
    test_df = load_data('test_FD001.txt')
    test_rul_df = pd.read_csv(RAW_DATA_DIR / 'RUL_FD001.txt', sep='\s+', header=None, names=['RUL'])

    print("Calculating RUL...")
    train_df = calculate_rul_train(train_df)
    
    # For test data, we need to add the True RUL to the last cycle
    # The RUL file contains the RUL for the *last* data point in the test file for each unit
    # We can calculate RUL for all points by adding the True RUL to the max cycle and subtracting current
    max_cycle_test = test_df.groupby('unit_nr')['time_cycles'].max().reset_index()
    max_cycle_test.columns = ['unit_nr', 'max_cycle']
    test_rul_df['unit_nr'] = test_rul_df.index + 1
    test_rul_df['max_cycle'] = max_cycle_test['max_cycle'] + test_rul_df['RUL']
    test_rul_df.drop('RUL', axis=1, inplace=True) # Rename to max_life to avoid confusion
    test_rul_df.rename(columns={'max_cycle': 'max_life'}, inplace=True)
    
    test_df = test_df.merge(test_rul_df, on='unit_nr', how='left')
    test_df['RUL'] = test_df['max_life'] - test_df['time_cycles']
    test_df.drop('max_life', axis=1, inplace=True)

    print("Normalizing data...")
    scaler = MinMaxScaler()
    train_df[FEATURE_COLS] = scaler.fit_transform(train_df[FEATURE_COLS])
    test_df[FEATURE_COLS] = scaler.transform(test_df[FEATURE_COLS])
    
    # Drop unused sensors
    train_df.drop(columns=SENSORS_TO_DROP, inplace=True)
    test_df.drop(columns=SENSORS_TO_DROP, inplace=True)

    print("Saving processed data...")
    train_df.to_csv(PROCESSED_DATA_DIR / 'train_FD001_processed.csv', index=False)
    test_df.to_csv(PROCESSED_DATA_DIR / 'test_FD001_processed.csv', index=False)
    
    # Save scaler
    joblib.dump(scaler, PROCESSED_DATA_DIR / 'scaler.pkl')
    print("Data processing complete.")

if __name__ == "__main__":
    process_data()
