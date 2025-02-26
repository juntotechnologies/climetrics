import streamlit as st
from models import authenticate_user, create_access_token, User, get_db
from datetime import timedelta



def login_button():
    """Add login button to the top right corner"""
    st.markdown(
        """
        <style>
        .stButton button {
            float: right;
            background-color: #0066cc;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    if not st.session_state.get("is_authenticated", False):
        if st.button("Login / Register"):
            st.session_state.show_login = True
            st.rerun()

def login_page():
    st.title("🏥 Login to Climetrics")
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")

    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if not username or not password:
                st.error("Please enter both username and password")
                return False

            db = next(get_db())
            user = authenticate_user(db, username, password)

            if user:
                # Create access token
                access_token = create_access_token(
                    data={"sub": user.username},
                    expires_delta=timedelta(minutes=30)
                )

                # Store in session state
                st.session_state["token"] = access_token
                st.session_state["username"] = user.username
                st.session_state["is_authenticated"] = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")
                return False

    with tab2:
        st.subheader("Register")
        new_username = st.text_input("Username", key="reg_username")
        new_password = st.text_input("Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password")
        full_name = st.text_input("Full Name")

        if st.button("Register"):
            if not all([new_username, new_password, confirm_password, full_name]):
                st.error("Please fill in all fields")
                return False

            if new_password != confirm_password:
                st.error("Passwords do not match")
                return False

            db = next(get_db())
            existing_user = db.query(User).filter(User.username == new_username).first()
            if existing_user:
                st.error("Username already exists")
                return False

            new_user = User(
                username=new_username,
                password_hash=User.get_password_hash(new_password),
                full_name=full_name,
                is_active=True
            )
            db.add(new_user)
            db.commit()

            st.success("Registration successful! Please login.")

def create_test_user():
    """Create a test user if none exists"""
    db = next(get_db())
    if not db.query(User).filter(User.username == "test").first():
        test_user = User(
            username="test",
            password_hash=User.get_password_hash("test123"),
            full_name="Test User",
            is_active=True
        )
        db.add(test_user)
        db.commit()

def check_auth():
    """Check if user is authenticated"""
    is_authenticated = st.session_state.get("is_authenticated", False)
    if not is_authenticated:
        login_page()
        return False
    return True

def logout():
    """Clear session state and log out user"""
    for key in ["token", "username", "is_authenticated"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()