import streamlit as st

def attendance_logic(attendance_pct):
    """
    Handles the high-stakes attendance rules:
    - 80%+ : Good/Eligible
    - 75%-80% : Warning
    - Below 75% : Fine Required
    """
    if attendance_pct >= 80:
        return "✅ Eligible (Good)", "green", "ELIGIBLE"
    elif attendance_pct >= 75:
        return "⚠️ Warning (Focus)", "orange", "WARNING: FOCUS NEEDED"
    else:
        return "❌ Fine Required", "red", "NOT PERMITTED - FINE REQUIRED"

def sidebar_status_banner(status_text, color):
    """Displays the colored status banner in the sidebar"""
    st.sidebar.markdown(
        f"""
        <div style="background-color: {color}; padding: 10px; border-radius: 5px; text-align: center;">
            <h3 style="color: white; margin: 0;">{status_text}</h3>
        </div>
        """, 
        unsafe_allow_html=True
    )