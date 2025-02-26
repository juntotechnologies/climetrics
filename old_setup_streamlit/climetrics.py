
import streamlit as st
from auth import login_button

def climetrics_page():
    # Add login button to top right
    login_button()
    
    # Main content
    st.markdown("<h1 style='text-align: center;'>Climetrics</h1>", unsafe_allow_html=True)
    
    # Hero section
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h2>Transform Your Clinical Data into Actionable Insights</h2>
            <p>Monitor, analyze, and improve your surgical outcomes with our comprehensive analytics platform.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Features section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style='text-align: center;'>
                <h3>📊 Real-time Analytics</h3>
                <p>Track surgical metrics and outcomes in real-time</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div style='text-align: center;'>
                <h3>🔍 Performance Insights</h3>
                <p>Compare metrics with peers and identify areas for improvement</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div style='text-align: center;'>
                <h3>📈 Quality Improvement</h3>
                <p>Make data-driven decisions to enhance patient care</p>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    climetrics_page()
