import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import os
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
    page_title="CliMetrics", page_icon="🏥", layout="wide"
)

def show_main_content():
    # Initialize username in session state
    if 'username' not in st.session_state:
        st.session_state.username = 'default_username'

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

    # Get data from database
    db = next(get_db())
    data = get_procedures_df(db)

    # Add logout button in sidebar
    if st.sidebar.button("Logout"):
        from auth import logout
        logout()

    # Header
    st.title("CliMetrics")
    st.markdown(
        f"Welcome, {st.session_state.username}! Compare your performance metrics with colleagues"
    )

    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Service selection
    service = st.sidebar.selectbox(
        "Select Service", options=sorted(data["service"].unique())
    )

    # Surgeon selection
    surgeons = sorted(data[data["service"] == service]["surgeon"].unique())
    current_surgeon = st.sidebar.selectbox("Select Surgeon", options=surgeons)

    # Metric selection
    st.sidebar.header("Metrics")
    selected_metric = st.sidebar.radio(
        "Select Metric to Display",
        options=[
            "Length of Stay",
            "Complication Rates",
            "T-Stage Distribution",
            "P-Stage Distribution",
        ],
    )

    # Calculate metrics
    metrics = get_surgeon_metrics(db, service, current_surgeon)

    # Display selected visualization
    st.subheader(f"{selected_metric} Comparison")
    if selected_metric == "Length of Stay":
        fig = create_los_comparison(data, service, current_surgeon)
    elif selected_metric == "Complication Rates":
        fig = create_complication_rate_chart(data, service, current_surgeon)
    elif selected_metric == "T-Stage Distribution":
        fig = create_stage_distribution_chart(data, service, current_surgeon, "t_stage")
    else:  # P-Stage Distribution
        fig = create_stage_distribution_chart(data, service, current_surgeon, "p_stage")

    st.plotly_chart(fig, use_container_width=True)

    # Footer
    st.markdown(
        """
        <div style='margin-top: 50px; text-align: center; color: #666;'>
            <small>Data is stored in a PostgreSQL database.</small>
        </div>
    """,
        unsafe_allow_html=True,
    )
    
def main():
    # Check if we should show landing page or main app
    if 'show_main_app' not in st.session_state:
        st.session_state.show_main_app = False

    if not st.session_state.show_main_app:
        # Create a container for the iframe
        container = st.container()
        
        # Load the HTML file
        try:
            with open("index.html", "r") as f:
                html_content = f.read()
            
            # Display the HTML content
            components.html(html_content, height=800)

            
            # JavaScript to handle the button click
            container.markdown("""
                <script>
                    window.addEventListener('message', function(e) {
                        if (e.data === 'launch_app') {
                            window.location.reload();
                        }
                    });
                </script>
            """, unsafe_allow_html=True)
            
            # Hidden button that will be clicked by JavaScript
            if container.button("Launch App", key="launch_button"):
                st.session_state.show_main_app = True
                st.rerun()
                
        except FileNotFoundError:
            st.error("Landing page not found. Redirecting to main app...")
            st.session_state.show_main_app = True
            st.rerun()
    else:
        show_main_content()  # Your existing main app code    
    

if __name__ == "__main__":
    main()
