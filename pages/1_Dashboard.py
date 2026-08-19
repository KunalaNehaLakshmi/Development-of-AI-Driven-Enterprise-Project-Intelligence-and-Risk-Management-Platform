import streamlit as st
import pandas as pd
from utils.ui import inject_css, page_header, render_domain_banner, get_risk_color

# ============================================================
# PAGE SETUP
# ============================================================

inject_css()

page_header(
    "Project Intelligence Dashboard",
    "Executive summary of project health, automated domain classification, quantitative risk scores, and deliverable tracking."
)

is_batch = st.session_state.get("is_batch", False)
batch_projects = st.session_state.get("batch_projects", [])

project_id = st.session_state.get("selected_project_id")
project = st.session_state.get("selected_project", {})

if not project_id or not project:
    st.warning("No active project found. Please upload a project document or load an enterprise reference dataset.")
    st.page_link("pages/2_Document_Upload.py", label="Open Document Ingestion")
    st.stop()

# Render Domain Banner
render_domain_banner(
    detected_domain=project.get("project_type_category", "IT"),
    model_used=project.get("model_used", "XGBoost Regressor"),
    detection_reason=project.get("domain_detection_reason", "")
)

# ============================================================
# BATCH SUMMARY (IF BATCH ACTIVE)
# ============================================================

if is_batch and batch_projects:
    st.subheader("Batch Project Risk Distribution")
    
    results_list = []
    for p in batch_projects:
        results_list.append({
            "Project Name": p.get("name", "Unknown"),
            "Domain": p.get("project_type_category", "IT"),
            "Health Score": p.get("health_score", 0),
            "Risk Score": p.get("risk_score", 0),
            "Risk Level": p.get("risk_level", "Unknown")
        })
        
    df = pd.DataFrame(results_list)
    
    col_b1, col_b2 = st.columns([1, 2])
    with col_b1:
        st.write("##### Risk Level Breakdown")
        risk_counts = df['Risk Level'].value_counts()
        st.bar_chart(risk_counts)
    with col_b2:
        st.write("##### Batch Project Inventory")
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    csv_export = df.to_csv(index=False)
    st.download_button(
        label="Download Batch Results (CSV)",
        data=csv_export,
        file_name="batch_project_risk_scores.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.divider()

# ============================================================
# EXECUTIVE METRIC CARDS
# ============================================================

st.subheader("Project Status & Risk Index")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Project Name", project.get("name", "Active Project"))
with col2:
    st.metric("Classified Domain", project.get("project_type_category", "IT"))
with col3:
    budget_num = project.get('budget', 0)
    st.metric("Allocated Budget", f"${budget_num:,.0f}" if isinstance(budget_num, (int, float)) else str(budget_num))
with col4:
    deadline_val = project.get("deadline", "TBD")
    if deadline_val == "TBD" and project.get("features", {}).get("planned_duration_days", 0) > 0:
        deadline_val = f"{int(project['features']['planned_duration_days'])} days"
    st.metric("Planned Duration", deadline_val)

risk_level = str(project.get("risk_level", "LOW")).upper()
risk_score = float(project.get("risk_score", 0.0))
health_score = float(project.get("health_score", 100.0 - risk_score))
model_used = project.get("model_used", "XGBoost Regressor")
severity_border, severity_bg = get_risk_color(risk_level)

st.markdown(
    f"""
    <div style="background: {severity_bg}; border: 1.5px solid {severity_border};
                padding: 1.1rem 1.4rem; border-radius: 8px; margin: 1.2rem 0;
                display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
        <div>
            <div style="color: {severity_border}; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">
                ML Inference Assessment • {model_used}
            </div>
            <div style="font-size: 1.6rem; font-weight: 800; color: #F9FAFB; margin-top: 2px;">
                {risk_level} RISK LEVEL ({risk_score:.1f}/100)
            </div>
        </div>
        <div style="text-align: right;">
            <div style="color: #9CA3AF; font-size: 0.82rem;">Overall Project Health Index</div>
            <div style="font-size: 1.6rem; font-weight: 800; color: #38BDF8;">
                {health_score:.1f} / 100
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SCOPE & DELIVERABLES
# ============================================================

st.divider()
st.subheader("Scope & Deliverables")
st.write(project.get("project_scope", "No scope defined in document."))

deliverables = project.get("deliverables", [])
if deliverables:
    with st.expander("Key Deliverables Breakdown", expanded=True):
        for d in deliverables:
            st.write(f"- {d}")

missing_info = project.get("missing_info", [])
if missing_info:
    st.warning("Identified Information Gaps: The following critical parameters were omitted from the uploaded document:")
    for m in missing_info:
        st.write(f"- {m}")

# ============================================================
# DEEP DIVE NAVIGATION
# ============================================================

st.divider()
st.subheader("Project Intelligence Navigation")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.page_link("pages/3_Project_Analysis.py", label="Project Analysis & Tasks", use_container_width=True)
with c2:
    st.page_link("pages/4_Risk_Intelligence.py", label="Risk Intelligence & Factors", use_container_width=True)
with c3:
    st.page_link("pages/5_Schedule_Intelligence.py", label="Schedule & Milestones", use_container_width=True)
with c4:
    st.page_link("pages/6_Dependencies.py", label="Dependencies & CPM", use_container_width=True)

c5, c6, c7, c8 = st.columns(4)
with c5:
    st.page_link("pages/7_What_If_Simulation.py", label="What-If Simulation", use_container_width=True)
with c6:
    st.page_link("pages/8_Recommendations.py", label="Strategic Recommendations", use_container_width=True)
with c7:
    st.page_link("pages/9_Documentation.py", label="Documentation Generator", use_container_width=True)
with c8:
    st.page_link("pages/10_AI_Assistant.py", label="RAG AI Assistant", use_container_width=True)