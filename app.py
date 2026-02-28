import streamlit as st
from utils.auth import AuthManager
from utils.styles import get_login_styles

st.set_page_config(
    page_title="Global Inequality Platform - Login",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(get_login_styles(), unsafe_allow_html=True)

auth_manager = AuthManager()

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False


def main():
    # Hero section
    st.markdown("""
    <div class="hero-section">
        <div class="logo">🌍</div>
        <h1 class="hero-title">Global Inequality Platform</h1>
        <p class="hero-subtitle" style="text-align: center; margin: 0 auto; max-width: 800px;">
            Unlock powerful insights into worldwide income inequality patterns with advanced analytics and AI
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        tab1, tab2 = st.tabs([" Sign In", " Create Account"])

        with tab1:
            st.markdown('<div class="auth-container">', unsafe_allow_html=True)
            st.markdown("### Welcome Back!")
            login_form()
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="auth-container">', unsafe_allow_html=True)
            st.markdown("### Join Our Platform")
            register_form()
            st.markdown('</div>', unsafe_allow_html=True)

    # Features section
    st.markdown(
        '<h2 style="text-align: center; font-size: 48px; color: white; margin: 80px 0 50px 0;">Platform Features</h2>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    features = [
        ("", "Power BI Dashboards", "Interactive visualizations with deep data exploration"),
        ("", "Global Mapping", "Visualize inequality patterns across countries"),
        ("", "Trend Analysis", "Track changes over time with forecasting"),
        ("", "AI Insights", "Get intelligent analysis powered by AI")
    ]

    for col, (icon, title, desc) in zip([col1, col2, col3, col4], features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)


def login_form():
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        col1, col2 = st.columns(2)
        with col1:
            login_btn = st.form_submit_button(" Sign In", use_container_width=True)
        with col2:
            demo_btn = st.form_submit_button(" Demo Mode", use_container_width=True)

        if login_btn:
            if username and password:
                user = auth_manager.login_user(username, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_id = user[0]
                    st.success(" Login successful!")
                    st.balloons()
                    st.switch_page("pages/1_🏠_Home.py")
                else:
                    st.error(" Invalid credentials")
            else:
                st.warning(" Please fill all fields")

        if demo_btn:
            st.session_state.authenticated = True
            st.session_state.username = "demo_user"
            st.session_state.demo_mode = True
            st.info(" Entering demo mode...")
            st.switch_page("pages/1_🏠_Home.py")


def register_form():
    with st.form("register_form"):
        username = st.text_input("Username", placeholder="Choose a username")
        email = st.text_input("Email", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password", placeholder="Create a password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")

        agree = st.checkbox("I agree to Terms & Conditions")

        register_btn = st.form_submit_button(" Create Account", use_container_width=True)

        if register_btn:
            if not all([username, email, password, confirm_password]):
                st.warning(" Please fill all fields")
            elif password != confirm_password:
                st.error(" Passwords don't match")
            elif len(password) < 6:
                st.error(" Password must be at least 6 characters")
            elif not agree:
                st.warning(" Please agree to terms")
            else:
                success, message = auth_manager.register_user(username, email, password)
                if success:
                    st.success(f" {message}")
                    st.balloons()
                else:
                    st.error(f" {message}")


if __name__ == "__main__":
    if st.session_state.authenticated:
        st.switch_page("pages/1_🏠_Home.py")
    else:
        main()
