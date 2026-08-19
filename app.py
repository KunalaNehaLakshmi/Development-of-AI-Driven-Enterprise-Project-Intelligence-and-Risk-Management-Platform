import os
import json
import streamlit as st
from utils.ui import inject_css, render_domain_banner


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Project Intelligence & Risk Advisor",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_css()


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "detected_domain" not in st.session_state:
    st.session_state.detected_domain = "IT"

if "domain_reason" not in st.session_state:
    st.session_state.domain_reason = ""

if "documents" not in st.session_state:
    st.session_state.documents = {}

if "selected_project_id" not in st.session_state:
    st.session_state.selected_project_id = None

if "selected_project" not in st.session_state:
    st.session_state.selected_project = None

if "project_analyzed" not in st.session_state:
    st.session_state.project_analyzed = False

if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "api_base" not in st.session_state:
    st.session_state.api_base = "http://127.0.0.1:8000"


# ============================================================
# LOGIN / AUTHENTICATION PAGE
# ============================================================

if not st.session_state.logged_in:

    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        .block-container {
            padding-top: 4rem;
            max-width: 520px;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )

    USER_FILE = "users.json"

    def load_users():
        if not os.path.exists(USER_FILE):
            default_users = {
                "it_user": {"password": "it123", "role": "Enterprise User"}, 
                "nonit_user": {"password": "nonit123", "role": "Enterprise User"}
            }
            with open(USER_FILE, "w") as f:
                json.dump(default_users, f, indent=4)
            return default_users
        try:
            with open(USER_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {"it_user": {"password": "it123", "role": "Enterprise User"}}

    def save_users(users):
        with open(USER_FILE, "w") as f:
            json.dump(users, f, indent=4)

    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: #F9FAFB; font-size: 1.8rem; font-weight: 700; margin-bottom: 0.3rem;">
                AI Project Intelligence &amp; Risk Advisor
            </h2>
            <p style="color: #9CA3AF; font-size: 0.95rem;">
                Predictive Risk Analytics, Schedule Intelligence &amp; Autonomous Document Comprehension
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

    with tab_login:
        with st.container(border=True):
            st.markdown("<h4 style='color: #F9FAFB; margin-bottom: 1rem;'>Account Authentication</h4>", unsafe_allow_html=True)
            
            login_username = st.text_input("Username / Email", placeholder="e.g. it_user or nonit_user", key="login_user")
            login_password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")
            
            st.write("")
            if st.button("Sign In", type="primary", use_container_width=True, key="btn_signin"):
                uname = login_username.strip()
                users = load_users()
                
                if uname in users and users[uname]["password"] == login_password:
                    st.session_state.logged_in = True
                    st.session_state.username = uname

                    # Reset project state
                    st.session_state.documents = {}
                    st.session_state.selected_project_id = None
                    st.session_state.selected_project = None
                    st.session_state.project_analyzed = False
                    st.session_state.prediction = None
                    st.rerun()
                else:
                    st.error("Authentication failed. Use demo accounts: it_user / it123 or nonit_user / nonit123")

    with tab_signup:
        with st.container(border=True):
            st.markdown("<h4 style='color: #F9FAFB; margin-bottom: 1rem;'>Register New Account</h4>", unsafe_allow_html=True)
            
            new_username = st.text_input("Username", placeholder="e.g. analyst@company.com", key="signup_user")
            new_password = st.text_input("Password", type="password", placeholder="••••••••", key="signup_pass")
            
            st.write("")
            if st.button("Register Account", use_container_width=True, key="btn_signup"):
                uname = new_username.strip()
                if not uname or not new_password:
                    st.error("Please enter both username and password.")
                else:
                    users = load_users()
                    if uname in users:
                        st.error("Username already registered. Please sign in.")
                    else:
                        users[uname] = {"password": new_password, "role": "Enterprise User"}
                        save_users(users)
                        st.success(f"Account registered for '{uname}'. You may now sign in.")

    st.stop()


# ============================================================
# LOGGED-IN HEADER BANNER
# ============================================================

project = st.session_state.get("selected_project")
detected_domain = st.session_state.get("detected_domain", "IT")
domain_reason = st.session_state.get("domain_reason", "")
model_used = project.get("model_used", "XGBoost Regressor" if detected_domain == "IT" else "Logistic Regression") if project else "XGBoost / CatBoost / Random Forest"

st.markdown(
    f"""
    <div style="background: #111827; border-bottom: 1px solid #374151;
                padding: 0.8rem 1.4rem; border-radius: 8px; margin-bottom: 1.2rem;
                display: flex; align-items: center; justify-content: space-between; gap: 1rem;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="color: #F9FAFB; font-weight: 700; font-size: 1.1rem;">
                AI Project Intelligence &amp; Risk Advisor
            </span>
            <span style="color: #6B7280;">|</span>
            <span style="color: #9CA3AF; font-size: 0.9rem;">
                Active Project: <b style="color: #F9FAFB;">{project.get('name', 'No Active Project Ingested') if project else 'No Active Project Ingested'}</b>
            </span>
        </div>
        <div>
            <span style="background: {'rgba(59, 130, 246, 0.15)' if detected_domain == 'IT' else 'rgba(245, 158, 11, 0.15)'};
                         color: {'#60A5FA' if detected_domain == 'IT' else '#FBBF24'};
                         border: 1px solid {'#3B82F6' if detected_domain == 'IT' else '#F59E0B'};
                         padding: 3px 10px; border-radius: 4px; font-size: 0.82rem; font-weight: 600;">
                {detected_domain} Project Engine
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR CONTROLS
# ============================================================

with st.sidebar:
    st.markdown("### Project Advisor")
    st.caption(f"Authenticated as: **{st.session_state.username}**")
    
    st.divider()

    # Batch project selector (if batch upload active)
    if st.session_state.get("is_batch", False) and "batch_projects" in st.session_state:
        st.markdown("**Batch Project Navigator**")
        batch_projects = st.session_state.batch_projects
        project_names = [p.get("name", f"Project {p['id']}") for p in batch_projects]
        
        selected_proj = st.session_state.get("selected_project")
        current_name = selected_proj.get("name") if selected_proj else None
        try:
            default_index = project_names.index(current_name) if current_name in project_names else 0
        except ValueError:
            default_index = 0
            
        selected_name = st.selectbox(
            "Active Project",
            options=project_names,
            index=default_index,
            label_visibility="collapsed"
        )
        
        if selected_name != current_name:
            for p in batch_projects:
                if p.get("name", f"Project {p['id']}") == selected_name:
                    st.session_state.selected_project = p
                    st.session_state.selected_project_id = p["id"]
                    st.session_state.detected_domain = p.get("project_type_category", "IT")
                    st.session_state.domain_reason = p.get("domain_detection_reason", "")
                    st.rerun()

        st.divider()

    if st.button("Sign Out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.documents = {}
        st.session_state.selected_project_id = None
        st.session_state.selected_project = None
        st.session_state.project_analyzed = False
        st.session_state.prediction = None
        st.rerun()


# ============================================================
# CENTRALIZED ENTERPRISE NAVIGATION
# ============================================================

pages = [
    st.Page("pages/2_Document_Upload.py", title="Document Ingestion"),
    st.Page("pages/1_Dashboard.py", title="Project Dashboard"),
    st.Page("pages/3_Project_Analysis.py", title="Project Analysis"),
    st.Page("pages/4_Risk_Intelligence.py", title="Risk Intelligence"),
    st.Page("pages/5_Schedule_Intelligence.py", title="Schedule Intelligence"),
    st.Page("pages/6_Dependencies.py", title="Dependencies & CPM"),
    st.Page("pages/7_What_If_Simulation.py", title="What-If Simulation"),
    st.Page("pages/8_Recommendations.py", title="Recommendations"),
    st.Page("pages/9_Documentation.py", title="Documentation"),
    st.Page("pages/10_AI_Assistant.py", title="RAG AI Assistant"),
]

navigation = st.navigation(pages, position="sidebar")
navigation.run()