import streamlit as st
import pandas as pd

# Import our custom modules from the src folder
from src.ui_filters import render_sidebar
from src.model_inference import load_forecasting_model, get_prediction
from src.charts_and_metrics import (
    render_kpis, 
    render_global_analysis, 
    render_deep_dive, 
    render_eligibility_pipeline
)

# 1. Page Configuration
st.set_page_config(page_title="Student Forecaster", layout="wide")

# 2. Data & Model Loading (Cached for fast performance)
@st.cache_data
def load_and_prep_data():
    df = pd.read_csv("data/ultimate_student_metrics_30k.csv")
    bins = [0, 50, 70, 85, 100]
    labels = ["Poor", "Below Average", "Average", "Toppers"]
    df['Student_Tier'] = pd.cut(df['Exam_Score'], bins=bins, labels=labels, include_lowest=True)
    
    def check_eligibility(pct):
        if pct >= 80: return "✅ Eligible (Good)"
        elif pct >= 75: return "⚠️ Warning (Focus)"
        else: return "❌ Fine Required"
    df['Eligibility_Status'] = df['Attendance_Pct'].apply(check_eligibility)
    
    return df

df = load_and_prep_data()
model = load_forecasting_model("models/student_rf_model.pkl")

st.title("🎓 Student Performance Forecaster")

# 3. Sidebar UI (Returns the user's inputs)
study_hours, sleep_hours, phone_usage, attendance = render_sidebar()

# 4. Inference Engine (Makes the prediction)
predicted_score = get_prediction(model, study_hours, sleep_hours, phone_usage)

# 5. Dashboard Rendering (Builds the charts)
render_kpis(predicted_score, study_hours, sleep_hours, phone_usage)

st.markdown("---")
render_global_analysis(df)

st.markdown("---")
render_deep_dive(df)

st.markdown("---")
render_eligibility_pipeline(df)