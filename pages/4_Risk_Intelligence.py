import streamlit as st
import pandas as pd
from utils.ui import inject_css, page_header, render_domain_banner, get_risk_color

# ============================================================
# PAGE SETUP
# ============================================================

inject_css()

page_header(
    "Risk Intelligence & ML Explainability",
    "Inspect quantitative risk factor contributions, explainability attributions, and qualitative risk indicators inferred by machine learning."
)

project = st.session_state.get("selected_project")
if not project:
    st.warning("No active project found. Please ingest a project document or reference dataset.")
    st.page_link("pages/2_Document_Upload.py", label="Open Document Ingestion")
    st.stop()

# Render Domain Banner
render_domain_banner(
    detected_domain=project.get("project_type_category", "IT"),
    model_used=project.get("model_used", "XGBoost Regressor"),
    detection_reason=project.get("domain_detection_reason", "")
)

# ============================================================
# QUANTITATIVE ML RISK SCORE
# ============================================================

risk_level = str(project.get("risk_level", "LOW")).upper()
risk_score = float(project.get("risk_score", 0.0))
model_used = project.get("model_used", "XGBoost Regressor")
severity_border, severity_bg = get_risk_color(risk_level)

col_score1, col_score2, col_score3 = st.columns([1.5, 1.5, 2])
with col_score1:
    st.metric("Predicted Risk Level", risk_level)
with col_score2:
    st.metric("ML Risk Score", f"{risk_score:.1f} / 100")
with col_score3:
    st.metric("Inference Engine", model_used)

st.markdown(
    f"""
    <div style="background: {severity_bg}; border-left: 4px solid {severity_border};
                padding: 0.9rem 1.2rem; border-radius: 6px; margin: 0.8rem 0 1.5rem 0;">
        <span style="color: {severity_border}; font-weight: 700; text-transform: uppercase; font-size: 0.82rem; letter-spacing: 0.5px;">Assessment:</span>
        <span style="color: #F9FAFB; margin-left: 6px; font-size: 0.92rem;">
            The <b>{model_used}</b> classified this project as <b>{risk_level}</b> risk with a computed score of <b>{risk_score:.1f}%</b>.
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# ML FEATURE DRIVERS (EXPLAINABILITY)
# ============================================================

st.divider()
st.subheader("Major Risk Drivers & Feature Attribution")
st.write("Quantitative indicators extracted from project parameters and their normalized impact on the risk model:")

features = project.get("features", {})
is_it = (str(project.get("project_type_category", "IT")).upper() == "IT")
drivers = []

if is_it:
    if features.get("team_turnover_pct", 0) > 15:
        drivers.append({"Driver": "Team Turnover Rate", "Observed Value": f"{features['team_turnover_pct']}%", "Impact Level": "High", "Weight": 0.22})
    if features.get("tech_complexity_score", 0) > 70:
        drivers.append({"Driver": "Technical Architecture Complexity", "Observed Value": f"{features['tech_complexity_score']}/100", "Impact Level": "High", "Weight": 0.20})
    if features.get("schedule_overrun_pct", 0) > 10:
        drivers.append({"Driver": "Schedule Overrun Rate", "Observed Value": f"{features['schedule_overrun_pct']}%", "Impact Level": "High", "Weight": 0.18})
    if features.get("vendor_dependency_count", 0) >= 2:
        drivers.append({"Driver": "External Vendor API Dependencies", "Observed Value": f"{features['vendor_dependency_count']} vendors", "Impact Level": "Medium", "Weight": 0.15})
    if features.get("cost_overrun_pct", 0) > 8:
        drivers.append({"Driver": "Budget Cost Variance", "Observed Value": f"{features['cost_overrun_pct']}%", "Impact Level": "Medium", "Weight": 0.14})
    if features.get("defect_count", 0) > 10:
        drivers.append({"Driver": "Unresolved Defect Density", "Observed Value": f"{features['defect_count']} bugs", "Impact Level": "Medium", "Weight": 0.11})
else:
    if features.get("dependency_delay", 0) > 7:
        drivers.append({"Driver": "Supply Chain & Material Delay", "Observed Value": f"{features['dependency_delay']} days", "Impact Level": "Critical", "Weight": 0.24})
    if features.get("delay_days", 0) > 15:
        drivers.append({"Driver": "Cumulative Work Package Slips", "Observed Value": f"{features['delay_days']} days", "Impact Level": "High", "Weight": 0.20})
    if features.get("resource_availability", 1.0) < 0.85:
        res_shortage = round((1.0 - features.get("resource_availability", 1.0)) * 100, 1)
        drivers.append({"Driver": "On-Site Resource Shortage", "Observed Value": f"{res_shortage}% deficit", "Impact Level": "High", "Weight": 0.18})
    if features.get("testing_failure_rate", 0) > 0.08:
        fail_pct = round(features.get("testing_failure_rate", 0) * 100, 1)
        drivers.append({"Driver": "Safety & Integration Test Failures", "Observed Value": f"{fail_pct}%", "Impact Level": "High", "Weight": 0.15})
    if features.get("critical_dependency_count", 0) >= 3:
        drivers.append({"Driver": "Critical Path Dependency Density", "Observed Value": f"{features['critical_dependency_count']} paths", "Impact Level": "Medium", "Weight": 0.12})
    if features.get("security_audit_progress", 100) < 70:
        audit_gap = round(100.0 - features.get("security_audit_progress", 0), 1)
        drivers.append({"Driver": "Regulatory & Safety Audit Deficit", "Observed Value": f"{audit_gap}% pending", "Impact Level": "Medium", "Weight": 0.11})

if drivers:
    df_drivers = pd.DataFrame(drivers)
    st.dataframe(df_drivers, use_container_width=True, hide_index=True)
    
    st.write("##### Feature Contribution Weight")
    chart_data = pd.DataFrame({
        "Driver": [d["Driver"] for d in drivers],
        "Weight": [d["Weight"] for d in drivers]
    }).set_index("Driver")
    st.bar_chart(chart_data)
else:
    st.success("No extreme anomalies or high-risk driver outliers were detected.")

# ============================================================
# QUALITATIVE RISKS (GENAI INFERRED)
# ============================================================

st.divider()
st.subheader("Qualitative Contextual Risks")
st.write("Risks inferred from document narrative, contract terms, or team meeting transcripts:")

potential_risks = project.get("potential_risks", [])
if potential_risks:
    for r in potential_risks:
        st.markdown(f"- {r}")
else:
    st.info("No explicit qualitative risks were identified in the uploaded document text.")

# ============================================================
# MITIGATION ACTIONS
# ============================================================

st.divider()
st.subheader("Recommended Next Actions")
c_act1, c_act2 = st.columns(2)
with c_act1:
    st.page_link("pages/7_What_If_Simulation.py", label="Run What-If Scenario Stress-Test", use_container_width=True)
with c_act2:
    st.page_link("pages/9_Documentation.py", label="Generate Formal Risk Register", use_container_width=True)