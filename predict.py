import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import tensorflow as tf
import pandas as pd
import numpy as np
import joblib

from tensorflow.keras.models import load_model

print("STEP 1: STARTED")

# ============================================================

# LOAD INPUT DATA

# ============================================================

df = pd.read_excel("input.xlsx")

print("STEP 2: DATA LOADED")

# ============================================================

# DATE COLUMN

# ============================================================

df['date'] = pd.to_datetime(df['date'])

# ============================================================

# FEATURE ENGINEERING

# ============================================================

for i in range(1, 6):
df[f'wl_lag{i}'] = df['wl'].shift(i)

df['wl_roll3'] = df['wl'].rolling(3).mean()

# ============================================================

# REMOVE NaN

# ============================================================

df.dropna(inplace=True)

# ============================================================

# USE RECENT DATA ONLY IF VERY LARGE

# ============================================================

if len(df) > 365:
df = df.tail(365)

print("STEP 3: FEATURES CREATED")

# ============================================================

# FEATURES

# ============================================================

features = [
'imerg',
'wl_lag1',
'wl_lag2',
'wl_lag3',
'wl_lag4',
'wl_lag5',
'wl_roll3'
]

X = df[features].values.astype(np.float32)

print("STEP 4: FEATURES EXTRACTED")

# ============================================================

# LOAD SCALER

# ============================================================

scaler = joblib.load("scaler.pkl")

print("STEP 5: SCALER LOADED")

# ============================================================

# SCALE DATA

# ============================================================

X_scaled = scaler.transform(X).astype(np.float32)

print("STEP 6: DATA SCALED")

# ============================================================

# CREATE SEQUENCES

# ============================================================

sequence_length = 10

X_seq = []

for i in range(sequence_length, len(X_scaled)):
X_seq.append(X_scaled[i-sequence_length:i])

X_seq = np.array(X_seq).astype(np.float32)

print("STEP 7: SEQUENCE CREATED")

# ============================================================

# SAVE DATES

# ============================================================

dates = df['date'].iloc[sequence_length:].reset_index(drop=True)

# ============================================================

# LOAD MODEL

# ============================================================

model = load_model(
"kosi_transformer_model.keras",
compile=False
)

print("STEP 8: MODEL LOADED")

# ============================================================

# PREDICTION

# ============================================================

pred = model.predict(X_seq, verbose=0)

print("STEP 9: PREDICTION COMPLETED")

# ============================================================

# OUTPUT

# ============================================================

leads = [1, 3, 5, 7, 10]

output = pd.DataFrame({
'Date': dates
})

for i, lead in enumerate(leads):
output[f'Prediction_t+{lead}'] = pred[:, i]

# ============================================================

# SAVE OUTPUT

# ============================================================

output.to_csv("output.csv", index=False)

print("STEP 10: OUTPUT SAVED")
