import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import joblib

# Tambahkan root project ke sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.inference import load_model, predict

st.title("Digital Twin Dashboard - Hydraulic Condition Monitoring")

# Load data & model (contoh: cooler_model)
df = pd.read_csv("./data/processed_dataset.csv")
model = load_model(path="./models/cooler_model.pkl")
scaler = joblib.load("./models/scaler.pkl")
feature_names = joblib.load("./models/feature_names.pkl")

# Sidebar
st.sidebar.header("Filter Data")
cycle = st.sidebar.slider("Cycle Index", 0, len(df)-1, 0)
input_data = df.iloc[[cycle]].copy()

# Drop target columns dan urutkan sesuai feature_names
TARGET_COLS = ['cooler', 'valve', 'leakage', 'acc', 'stable']
input_features = input_data.drop(columns=[col for col in TARGET_COLS if col in input_data.columns], errors='ignore')
input_features = input_features[feature_names]
input_features_scaled = scaler.transform(input_features)

# Show sensor data
st.subheader("Sensor Data for Selected Cycle")
st.write(input_data)

# Prediction
st.subheader("Predicted Component Conditions")
preds, probs = predict(model, input_features_scaled)
st.write(f"Predicted class: {preds[0]}")
st.write(f"Prediction probabilities: {probs[0]}")

# Optional: Feature Importance
if st.checkbox("Show Feature Importance"):
    importance_df = pd.read_csv("./data/cooler_feature_importance.csv")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x="importance", y="feature", data=importance_df.head(10), ax=ax)
    st.pyplot(fig)
