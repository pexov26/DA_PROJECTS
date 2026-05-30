import streamlit as st

def render_sidebar():
    """
    Renders the sidebar for user inputs and returns the selected values.
    """
    st.sidebar.header("⚙️ Adjust Daily Habits")
    
    study_hours = st.sidebar.slider("Study Hours", min_value=0.0, max_value=10.0, value=5.0, step=0.5)
    sleep_hours = st.sidebar.slider("Sleep Hours", min_value=4.0, max_value=10.0, value=7.0, step=0.5)
    phone_usage = st.sidebar.slider("Phone Usage", min_value=0.0, max_value=14.0, value=4.0, step=0.5)
    attendance = st.sidebar.slider("Attendance %", 0.0, 100.0, 85.0, 1.0)

    # Dynamic Eligibility Status in the sidebar
    if attendance >= 80: 
        status_color, status_text = "green", "ELIGIBLE"
    elif attendance >= 75: 
        status_color, status_text = "orange", "WARNING: FOCUS"
    else: 
        status_color, status_text = "red", "NOT PERMITTED - FINE REQUIRED"

    st.sidebar.markdown(
        f"<h3 style='color:{status_color}; text-align:center;'>{status_text}</h3>", 
        unsafe_allow_html=True
    )

    return study_hours, sleep_hours, phone_usage, attendance