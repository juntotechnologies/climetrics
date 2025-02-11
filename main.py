import streamlit as st
import pandas as pd
from data_generator import get_surgeon_metrics, get_procedures_df, populate_mock_data
from visualization import (
    create_los_comparison,
    create_complication_rate_chart,
    create_stage_distribution_chart,
)
from styles import apply_custom_styles
from models import get_db, Surgeon, Procedure
from auth import check_auth, create_test_user

# Page configuration
st.set_page_config(
    page_title="Surgical Metrics Dashboard", page_icon="🏥", layout="wide"
)

# Initialize username in session state
if 'username' not in st.session_state:
    st.session_state.username = 'default_username'

# Display username
st.write(f"Hello {st.session_state.username}!")

# Apply custom styles
apply_custom_styles()

# Initialize database and session state
if "initialized" not in st.session_state:
    db = next(get_db())
    if not db.query(Surgeon).first():  # If database is empty
        populate_mock_data(db)
    create_test_user()  # Create test user if not exists
    st.session_state.initialized = True

# Check authentication
if not check_auth():
    st.stop()

# Landing page content
st.title("Welcome to the Surgical Metrics Dashboard")
st.markdown("""
This dashboard provides insights into various surgical metrics, including:
- Length of Stay (LOS) Comparison
- Complication Rate Chart
- Stage Distribution Chart

Use the navigation options below to explore the different sections of the dashboard.
""")

# Navigation options
if st.button("View LOS Comparison"):
    st.session_state.page = "los_comparison"
elif st.button("View Complication Rate Chart"):
    st.session_state.page = "complication_rate_chart"
elif st.button("View Stage Distribution Chart"):
    st.session_state.page = "stage_distribution_chart"
else:
    st.session_state.page = "landing"

# Display the selected page
if st.session_state.page == "los_comparison":
    st.header("Length of Stay (LOS) Comparison")
    # Add your LOS comparison code here
    create_los_comparison()
elif st.session_state.page == "complication_rate_chart":
    st.header("Complication Rate Chart")
    # Add your complication rate chart code here
    create_complication_rate_chart()
elif st.session_state.page == "stage_distribution_chart":
    st.header("Stage Distribution Chart")
    # Add your stage distribution chart code here
    create_stage_distribution_chart()
else:
    st.header("Landing Page")
    st.write("Please select an option from the navigation above.")
