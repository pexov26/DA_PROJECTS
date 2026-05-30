import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Centralized colors for consistency across all charts
tier_colors = {
    "Toppers": "#4285F4",
    "Average": "#34A853",
    "Below Average": "#FBBC05",
    "Poor": "#EA4335"
}

def render_kpis(predicted_score, study_hours, sleep_hours, phone_usage):
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


def render_global_analysis(df):
    st.subheader("📊 Global Dataset Analysis")
    chart_col1, chart_col2 = st.columns(2)

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


def render_deep_dive(df):
    st.subheader("🚀 Deep Dive: Productivity & AI Integration")

    # Calculate the average scores for each tier
    tier_summary = df.groupby('Student_Tier', as_index=False, observed=False)[['Productivity_Score', 'AI_Tool_Usage_Hours_Daily']].mean()

    bar_col1, bar_col2 = st.columns(2)

    with bar_col1:
        fig_prod_bar = px.bar(
            tier_summary, x="Student_Tier", y="Productivity_Score",
            color="Student_Tier", title="Avg Productivity Score by Tier",
            color_discrete_map=tier_colors
        )
        st.plotly_chart(fig_prod_bar, use_container_width=True)

    with bar_col2:
        fig_ai_bar = px.bar(
            tier_summary, x="Student_Tier", y="AI_Tool_Usage_Hours_Daily",
            color="Student_Tier", title="Avg AI Tool Usage (Hours) by Tier",
            color_discrete_map=tier_colors
        )
        st.plotly_chart(fig_ai_bar, use_container_width=True)

    # Area Chart
    df_sorted = df.sort_values("AI_Tool_Usage_Hours_Daily")
    fig_area = px.area(
        df_sorted, x="AI_Tool_Usage_Hours_Daily", y="Productivity_Score", 
        color="Student_Tier", title="The AI-Productivity Connection: Impact of AI Tools on Output",
        color_discrete_map=tier_colors, line_group="Student_Tier"
    )
    st.plotly_chart(fig_area, use_container_width=True)


def render_eligibility_pipeline(df):
    st.subheader("📋 Exam Eligibility & Attendance Pipeline")
    eligibility_col1, eligibility_col2 = st.columns(2)

    eligibility_counts = df['Eligibility_Status'].value_counts().reset_index()

    with eligibility_col1:
        fig_eligibility = px.bar(
            eligibility_counts, x='count', y='Eligibility_Status', orientation='h',
            title="Student Eligibility Pipeline", color='Eligibility_Status',
            color_discrete_map={
                "✅ Eligible (Good)": "#34A853", 
                "⚠️ Warning (Focus)": "#FBBC05", 
                "❌ Fine Required": "#EA4335"
            }
        )
        st.plotly_chart(fig_eligibility, use_container_width=True)

    with eligibility_col2:
        tier_counts = df['Student_Tier'].value_counts().reset_index()
        fig_donut = px.pie(
            tier_counts, values='count', names='Student_Tier', 
            title="Student Performance Mix", hole=0.5, 
            color='Student_Tier', color_discrete_map=tier_colors
        )
        fig_donut.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_donut, use_container_width=True)