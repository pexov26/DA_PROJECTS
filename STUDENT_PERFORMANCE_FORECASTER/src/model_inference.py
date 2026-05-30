import pandas as pd
import joblib
import streamlit as st

@st.cache_resource
def load_forecasting_model(model_path):
    """
    Loads the trained Random Forest model. 
    Cached to prevent reloading on every user interaction.
    """
    return joblib.load(model_path)

def get_prediction(model, study_hours, sleep_hours, phone_usage):
    """
    Takes the user inputs, packages them into a DataFrame, 
    and returns the predicted exam score.
    """
    # Package inputs exactly how the model expects them
    input_data = pd.DataFrame({
        'Study_Hours_Daily': [study_hours],
        'Sleep_Hours': [sleep_hours],       # <--- THIS IS THE FIXED LINE
        'Phone_Usage_Hours_Daily': [phone_usage]
    })

    # Make the prediction and return the single float value
    predicted_score = model.predict(input_data)[0]
    
    return predicted_score