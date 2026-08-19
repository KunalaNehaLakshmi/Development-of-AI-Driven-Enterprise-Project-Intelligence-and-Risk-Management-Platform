import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    /* Centralized Enterprise Dark Theme */
    :root {
        --bg-main: #0B0F19;
        --bg-secondary: #111827;
        --bg-card: #1F2937;
        --border-color: #374151;
        --text-primary: #F9FAFB;
        --text-secondary: #9CA3AF;
        --accent-blue: #3B82F6;
        --risk-critical: #EF4444;
        --risk-high: #F87171;
        --risk-medium: #F59E0B;
        --risk-low: #10B981;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #374151;
    }

    /* Enterprise Headers */
    .enterprise-header {
        padding: 1.1rem 1.4rem;
        background: #111827;
        border: 1px solid #374151;
        border-radius: 8px;
        margin-bottom: 1.2rem;
    }
    
    .enterprise-header h1 {
        margin: 0;
        font-size: 1.65rem;
        font-weight: 700;
        color: #F9FAFB;
        letter-spacing: -0.3px;
    }
    
    .enterprise-header p {
        margin: 0.3rem 0 0 0;
        color: #9CA3AF;
        font-size: 0.95rem;
        font-weight: 400;
    }

    /* Cards */
    .enterprise-card {
        background: #1F2937;
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }

    /* Status Badges */
    .domain-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    .domain-badge-it {
        background: rgba(59, 130, 246, 0.15);
        color: #60A5FA;
        border: 1px solid #3B82F6;
    }

    .domain-badge-nonit {
        background: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid #F59E0B;
    }

    /* Streamlit Metric Overrides */
    [data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #F9FAFB !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        color: #9CA3AF !important;
        font-weight: 500 !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 6px;
        font-weight: 600;
        border: 1px solid #374151;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #1F2937 !important;
        border-radius: 6px !important;
        color: #F9FAFB !important;
    }
    </style>
    """, unsafe_allow_html=True)


def page_header(title, subtitle=None):
    st.markdown(
        f"""
        <div class="enterprise-header">
            <h1>{title}</h1>
            {f'<p>{subtitle}</p>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_domain_banner(detected_domain, model_used, detection_reason=""):
    is_it = (str(detected_domain).upper() in ["IT", "IT PROJECT"])
    badge_class = "domain-badge-it" if is_it else "domain-badge-nonit"
    domain_title = "IT Project" if is_it else "Non-IT Project"

    st.markdown(
        f"""
        <div style="background: #111827; border: 1px solid #374151; border-left: 4px solid {'#3B82F6' if is_it else '#F59E0B'};
                    padding: 1rem 1.3rem; border-radius: 8px; margin-bottom: 1.2rem;
                    display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.8rem;">
            <div>
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
                    <span class="domain-badge {badge_class}">Detected Domain: {domain_title}</span>
                    <span style="color: #9CA3AF; font-size: 0.85rem;">Active Model: <b>{model_used}</b></span>
                </div>
                <div style="color: #D1D5DB; font-size: 0.88rem;">
                    <b>Detection Rationale:</b> {detection_reason or 'Extracted project scope and technical parameters.'}
                </div>
            </div>
            <div>
                <span style="font-size: 0.78rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.5px;">Automated Classification</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def get_risk_color(risk_level):
    lvl = str(risk_level).upper()
    if "CRITICAL" in lvl:
        return "#EF4444", "rgba(239, 68, 68, 0.15)"
    elif "HIGH" in lvl:
        return "#F87171", "rgba(248, 113, 113, 0.15)"
    elif "MEDIUM" in lvl:
        return "#F59E0B", "rgba(245, 158, 11, 0.15)"
    else:
        return "#10B981", "rgba(16, 185, 129, 0.15)"
