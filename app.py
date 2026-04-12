import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib

# 1. Page Configuration & Data Loading
st.set_page_config(page_title="Student Forecaster", layout="wide")

# Load the dataset
df = pd.read_csv("data/ultimate_student_metrics_30k.csv")

# Create the Student_Tier column for coloring
bins = [0, 50, 70, 85, 100]
labels = ["Poor", "Below Average", "Average", "Toppers"]
df['Student_Tier'] = pd.cut(df['Exam_Score'], bins=bins, labels=labels, include_lowest=True)

# Load the trained Machine Learning model
model = joblib.load("models/student_rf_model.pkl")

st.title("🎓 Student Performance Forecaster")

# 2. The Sidebar (User Inputs)
st.sidebar.header("⚙️ Adjust Daily Habits")
study_hours = st.sidebar.slider("Study Hours", min_value=0.0, max_value=10.0, value=5.0, step=0.5)
sleep_hours = st.sidebar.slider("Sleep Hours", min_value=4.0, max_value=10.0, value=7.0, step=0.5)
phone_usage = st.sidebar.slider("Phone Usage", min_value=0.0, max_value=14.0, value=4.0, step=0.5)
attendance = st.sidebar.slider("Attendance %", 0.0, 100.0, 85.0, 1.0)

# Define color based on your rules
if attendance >= 80: status_color, status_text = "green", "ELIGIBLE"
elif attendance >= 75: status_color, status_text = "orange", "WARNING: FOCUS"
else: status_color, status_text = "red", "NOT PERMITTED - FINE REQUIRED"

st.sidebar.markdown(f"<h3 style='color:{status_color}; text-align:center;'>{status_text}</h3>", unsafe_allow_html=True)

# Package inputs for the model
input_data = pd.DataFrame({
    'Study_Hours_Daily': [study_hours],
    'Sleep_Hours_Daily': [sleep_hours],
    'Phone_Usage_Hours_Daily': [phone_usage]
})

# Make the prediction
predicted_score = model.predict(input_data)[0]

# 3. The Top Row (Forecasted KPIs)
st.subheader("Forecasted Results")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Forecasted Exam Score", value=f"{predicted_score:.1f}%", delta="Target: 80%")

with col2:
    # Productivity Gauge
    prod_value = min(100, study_hours * 8 + sleep_hours * 2)
    fig_prod = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prod_value,
        title={'text': "Predicted Productivity"},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#4285F4"}}
    ))
    fig_prod.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_prod, use_container_width=True)

with col3:
    # Focus Gauge
    focus_value = max(0, 100 - phone_usage * 5)
    fig_focus = go.Figure(go.Indicator(
        mode="gauge+number",
        value=focus_value,
        title={'text': "Predicted Focus"},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#34A853"}}
    ))
    fig_focus.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_focus, use_container_width=True)

st.markdown("---")

# 4. The Visuals (Plotly Charts)
st.subheader("📊 Global Dataset Analysis")
chart_col1, chart_col2 = st.columns(2)

tier_colors = {
    "Toppers": "#4285F4",
    "Average": "#34A853",
    "Below Average": "#FBBC05",
    "Poor": "#EA4335"
}

with chart_col1:
    fig_hist = px.histogram(
        df, x="Exam_Score", color="Student_Tier", 
        title="Student Grade Distribution", 
        color_discrete_map=tier_colors
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with chart_col2:
    fig_scatter = px.scatter(
        df, x="Phone_Usage_Hours_Daily", y="Exam_Score", 
        color="Student_Tier", title="Impact of Phone Usage", 
        opacity=0.6, color_discrete_map=tier_colors
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown("---")
# 5. Deep Dive: Productivity & AI Integration
st.subheader("🚀 Deep Dive: Productivity & AI Integration")

# Calculate the average scores for each tier
tier_summary = df.groupby('Student_Tier', as_index=False)[['Productivity_Score', 'AI_Tool_Usage_Hours_Daily']].mean()

bar_col1, bar_col2 = st.columns(2)

with bar_col1:
    # 1. Productivity Bar Chart
    fig_prod_bar = px.bar(
        tier_summary, 
        x="Student_Tier", 
        y="Productivity_Score",
        color="Student_Tier",
        title="Avg Productivity Score by Tier",
        color_discrete_map=tier_colors
    )
    st.plotly_chart(fig_prod_bar, use_container_width=True)

with bar_col2:
    # 2. AI Usage Bar Chart
    fig_ai_bar = px.bar(
        tier_summary, 
        x="Student_Tier", 
        y="AI_Tool_Usage_Hours_Daily",
        color="Student_Tier",
        title="Avg AI Tool Usage (Hours) by Tier",
        color_discrete_map=tier_colors
    )
    st.plotly_chart(fig_ai_bar, use_container_width=True)

# 3. AI-Productivity Relationship (Area Chart)
# We sort the data by AI usage to make the line/area chart smooth
df_sorted = df.sort_values("AI_Tool_Usage_Hours_Daily")

fig_area = px.area(
    df_sorted, 
    x="AI_Tool_Usage_Hours_Daily", 
    y="Productivity_Score", 
    color="Student_Tier",
    title="The AI-Productivity Connection: Impact of AI Tools on Output",
    color_discrete_map=tier_colors,
    line_group="Student_Tier"
)
st.plotly_chart(fig_area, use_container_width=True)
# Create Attendance Eligibility Column
def check_eligibility(pct):
    if pct >= 80: return "✅ Eligible (Good)"
    elif pct >= 75: return "⚠️ Warning (Focus)"
    else: return "❌ Fine Required"

df['Eligibility_Status'] = df['Attendance_Pct'].apply(check_eligibility)
# --- SECTION 6: ELIGIBILITY & REALITY CHECK ---
st.markdown("---")
st.subheader("📋 Exam Eligibility & Attendance Pipeline")

# 1. Create two columns for side-by-side visuals
eligibility_col1, eligibility_col2 = st.columns(2)

# 2. Prepare the data for the bar chart
eligibility_counts = df['Eligibility_Status'].value_counts().reset_index()

with eligibility_col1:
    # Horizontal Bar Chart (The "Pipeline" Look)
    fig_eligibility = px.bar(
        eligibility_counts, 
        x='count', 
        y='Eligibility_Status', 
        orientation='h',
        title="Student Eligibility Pipeline",
        color='Eligibility_Status',
        color_discrete_map={
            "✅ Eligible (Good)": "#34A853", 
            "⚠️ Warning (Focus)": "#FBBC05", 
            "❌ Fine Required": "#EA4335"
        }
    )
    st.plotly_chart(fig_eligibility, use_container_width=True)

with eligibility_col2:
    # 1. Count how many students are in each tier
    tier_counts = df['Student_Tier'].value_counts().reset_index()
    
    # 2. Build the Donut Chart
    fig_donut = px.pie(
        tier_counts, 
        values='count', 
        names='Student_Tier', 
        title="Student Performance Mix",
        hole=0.5, # This creates the "Donut" hole in the middle
        color='Student_Tier',
        color_discrete_map=tier_colors
    )
    
    # 3. Clean up the legend position to match your screenshot
    fig_donut.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    st.plotly_chart(fig_donut, use_container_width=True)