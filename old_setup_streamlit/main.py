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
    
    @st.cache_data
    def load_data():
        db = next(get_db())  # Get database connection
        procedures_df = get_procedures_df(db)
        return procedures_df

    # Load the data
    df = load_data()

    # Create filters in the sidebar
    st.sidebar.title("Filters")
    service = st.sidebar.selectbox(
        "Select Service",
        options=sorted(df['service'].unique())
    )

    current_surgeon = st.sidebar.selectbox(
        "Select Surgeon",
        options=sorted(df['surgeon'].unique())
    )

    # Create visualization
    los_fig = create_los_comparison(df, service, current_surgeon)
    st.plotly_chart(los_fig)

elif st.session_state.page == "complication_rate_chart":
    st.header("Complication Rate Chart")
    
    @st.cache_data
    def load_data():
        db = next(get_db())  # Get database connection
        procedures_df = get_procedures_df(db)
        return procedures_df

    df = load_data()

    st.sidebar.title("Filters")
    service = st.sidebar.selectbox(
        "Select Service",
        options=sorted(df['service'].unique())
    )

    current_surgeon = st.sidebar.selectbox(
        "Select Surgeon",
        options=sorted(df['surgeon'].unique())
    )

    comp_fig = create_complication_rate_chart(df, service, current_surgeon)
    st.plotly_chart(comp_fig)

elif st.session_state.page == "stage_distribution_chart":
    st.header("Stage Distribution Chart")
    
    @st.cache_data
    def load_data():
        db = next(get_db())  # Get database connection
        procedures_df = get_procedures_df(db)
        return procedures_df

    df = load_data()

    st.sidebar.title("Filters")
    service = st.sidebar.selectbox(
        "Select Service",
        options=sorted(df['service'].unique())
    )

    current_surgeon = st.sidebar.selectbox(
        "Select Surgeon",
        options=sorted(df['surgeon'].unique())
    )

    stage_fig = create_stage_distribution_chart(df, service, current_surgeon)
    st.plotly_chart(stage_fig)

else:
    st.header("Landing Page")
    st.write("Please select an option from the navigation above.")
