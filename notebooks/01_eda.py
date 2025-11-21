# %% [markdown]
# # Exploratory Data Analysis - NASA CMAPSS Dataset
# 
# This notebook explores the NASA Turbofan Engine Degradation Simulation dataset.
# We will focus on `train_FD001.txt` which simulates engine degradation under one operating condition.

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# %%
# Define column names based on dataset documentation
index_names = ['unit_nr', 'time_cycles']
setting_names = ['setting_1', 'setting_2', 'setting_3']
sensor_names = ['s_{}'.format(i) for i in range(1, 22)] 
col_names = index_names + setting_names + sensor_names

# %%
# Load data
data_path = Path('../data/raw/train_FD001.txt')
if not data_path.exists():
    print(f"File not found: {data_path}")
    print("Please run src/data/download_data.py first.")
else:
    df = pd.read_csv(data_path, sep='\s+', header=None, names=col_names)
    print(f"Data shape: {df.shape}")
    print(df.head())

# %% [markdown]
# ## Data Description
# - `unit_nr`: Engine identifier
# - `time_cycles`: Time step (cycle)
# - `setting_1` to `setting_3`: Operational settings
# - `s_1` to `s_21`: Sensor measurements

# %%
if 'df' in locals():
    print(df.describe())

# %% [markdown]
# ## RUL Calculation
# For the training data, the RUL (Remaining Useful Life) is calculated as the number of cycles remaining before the engine fails.
# Since the training data goes until failure, RUL = max(time_cycles) - current(time_cycles).

# %%
def add_rul(df):
    # Get the max cycle for each unit
    max_cycle = df.groupby('unit_nr')['time_cycles'].max().reset_index()
    max_cycle.columns = ['unit_nr', 'max_cycle']
    
    # Merge back
    df = df.merge(max_cycle, on='unit_nr', how='left')
    
    # Calculate RUL
    df['RUL'] = df['max_cycle'] - df['time_cycles']
    
    # Drop max_cycle as it's no longer needed
    df.drop('max_cycle', axis=1, inplace=True)
    return df

if 'df' in locals():
    df = add_rul(df)
    print(df[['unit_nr', 'time_cycles', 'RUL']].head())

# %% [markdown]
# ## Sensor Analysis
# Let's visualize how sensors change over time for a specific unit.

# %%
def plot_sensors(df, unit_nr=1):
    unit_data = df[df['unit_nr'] == unit_nr]
    
    plt.figure(figsize=(20, 15))
    for i, sensor in enumerate(sensor_names):
        plt.subplot(5, 5, i+1)
        plt.plot(unit_data['time_cycles'], unit_data[sensor])
        plt.title(sensor)
        plt.xlabel('Cycles')
    plt.tight_layout()
    plt.show()

if 'df' in locals():
    plot_sensors(df, unit_nr=1)

# %% [markdown]
# ## Correlation Analysis
# Check correlation between sensors and RUL.

# %%
if 'df' in locals():
    plt.figure(figsize=(15, 10))
    sns.heatmap(df.corr(), cmap='coolwarm', annot=False)
    plt.title('Correlation Matrix')
    plt.show()

# %% [markdown]
# ## Observations
# - Some sensors (e.g., s_1, s_5, s_10, s_16, s_18, s_19) seem constant or have very low variance. These might be candidates for removal.
# - Others show a clear trend as RUL decreases (cycles increase).
