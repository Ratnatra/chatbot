import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load model, scaler, and feature names
clf = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')
feature_names = joblib.load('features.pkl')

# Simple UI
st.title("Personalized Medicine Recommendation")

# Dynamically create input fields for each feature
user_data = {}
for feature in feature_names:
    user_data[feature] = st.text_input(f"Enter value for {feature}")

if st.button("Get Recommendation"):
    # Convert user input to dataframe
    input_df = pd.DataFrame([user_data])
    # Convert columns to correct types (float if possible)
    for col in input_df.columns:
        try:
            input_df[col] = input_df[col].astype(float)
        except ValueError:
            pass  # If conversion fails, keep as is
    # One-hot encoding to match training data
    input_df = pd.get_dummies(input_df)
    # Add missing columns with 0
    for col in feature_names:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[feature_names]
    # Scale input
    input_scaled = scaler.transform(input_df)
    # Predict
    pred = clf.predict(input_scaled)[0]
    st.success(f"Recommended Medication: {pred}")