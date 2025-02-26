import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styles to the Streamlit app."""
    st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
            background-color: #ffffff;
        }

        .metric-card {
            background-color: #f8f9fa;
            border-radius: 0.75rem;
            padding: 1.5rem;
            margin: 0.75rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: transform 0.2s ease-in-out;
        }

        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .metric-value {
            font-size: 2.5rem;
            font-weight: bold;
            color: #0066cc;
            margin-bottom: 0.5rem;
        }

        .metric-label {
            font-size: 1rem;
            color: #4a5568;
            font-weight: 500;
        }

        h1 {
            color: #2c3e50;
            font-weight: 700;
            margin-bottom: 1rem;
        }

        h2, h3 {
            color: #2c3e50;
            font-weight: 600;
        }

        .stSelectbox label, .stRadio label {
            color: #2c3e50;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }

        .stSidebar {
            background-color: #f8f9fa;
            padding: 2rem 1rem;
        }

        .stSidebar [data-testid="stMarkdownContainer"] h1 {
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
        }

        /* Custom radio buttons */
        .stRadio > label {
            font-weight: 600;
            margin-bottom: 1rem;
        }

        .stRadio > div {
            margin-top: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)