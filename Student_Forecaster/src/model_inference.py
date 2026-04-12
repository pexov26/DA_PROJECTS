import joblib
import pandas as pd

def load_student_model():
    return joblib.load("models/student_rf_model.pkl")

def make_prediction(model, study, sleep, phone):
    input_data = pd.DataFrame({
        'Study_Hours_Daily': [study],
        'Sleep_Hours_Daily': [sleep],
        'Phone_Usage_Hours_Daily': [phone]
    })
    return model.predict(input_data)[0]