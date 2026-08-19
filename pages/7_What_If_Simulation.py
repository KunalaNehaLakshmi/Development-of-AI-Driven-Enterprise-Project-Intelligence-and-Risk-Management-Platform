import streamlit as st
from utils.ui import inject_css, page_header
from utils.predictor import predict_it_risk, predict_non_it_risk

# ============================================================
# PAGE SETUP
# ============================================================

inject_css()

is_it = (st.session_state.get("user_type", "IT") == "IT")
domain_label = "IT Project" if is_it else "Non-IT Project"

page_header(
    f"What-If Scenario Simulation Engine ({domain_label})",
    "Simulate timeline shifts, budget fluctuations, and resource constraints without affecting live baseline data."
)

project = st.session_state.get("selected_project")
if not project:
    st.warning("⚠️ No active project found. Please upload a project document or load a demo sample.")
    st.page_link("pages/2_Document_Upload.py", label="📤 Go to Document Upload & Demo Loader")
    st.stop()

base_features = dict(project.get("features", {}))
base_risk = float(project.get("risk_score", 50.0))

# ============================================================
# SIMULATION PARAMETERS
# ============================================================

st.subheader("⚙️ Scenario Stress-Test Parameters")

col_p1, col_p2, col_p3 = st.columns(3)

with col_p1:
    sim_delay = st.slider("Additional Schedule Delay (Days)", 0, 90, 15, help="Simulates upstream supplier delay or uncompleted sprint milestones.")
with col_p2:
    sim_budget = st.slider("Budget Variance (%)", -40, 60, 10, help="Simulates budget reductions or unexpected cost inflation.")
with col_p3:
    sim_resource = st.slider("Team / Resource Deficit (%)", 0, 60, 20, help="Simulates engineer churn or subcontractor labor shortages.")

# ============================================================
# SIMULATION INFERENCE EXECUTION
# ============================================================

if st.button("🚀 Run Scenario Simulation", type="primary", use_container_width=True):
    sim_features = dict(base_features)
    
    if is_it:
        # Perturb IT features
        sim_features["schedule_overrun_pct"] = float(sim_features.get("schedule_overrun_pct", 0.0)) + (sim_delay * 0.8)
        sim_features["cost_overrun_pct"] = float(sim_features.get("cost_overrun_pct", 0.0)) + max(0.0, float(sim_budget))
        sim_features["team_turnover_pct"] = float(sim_features.get("team_turnover_pct", 0.0)) + float(sim_resource)
        sim_features["resource_availability_pct"] = max(20.0, float(sim_features.get("resource_availability_pct", 100.0)) - float(sim_resource))
        pred = predict_it_risk(sim_features)
    else:
        # Perturb Non-IT features
        sim_features["delay_days"] = float(sim_features.get("delay_days", 0.0)) + float(sim_delay)
        sim_features["dependency_delay"] = float(sim_features.get("dependency_delay", 0.0)) + (sim_delay * 0.5)
        sim_features["resource_availability"] = max(0.2, float(sim_features.get("resource_availability", 1.0)) - (sim_resource / 100.0))
        sim_features["schedule_variance"] = float(sim_features.get("schedule_variance", 0.0)) + float(sim_delay)
        pred = predict_non_it_risk(sim_features)
        
    sim_risk = float(pred["risk_score"])
    sim_level = pred["risk_level"].upper()
    delta_risk = sim_risk - base_risk
    
    st.divider()
    st.subheader("📊 Simulation Impact Assessment")
    
    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        st.metric("Baseline Risk Score", f"{base_risk:.1f}/100")
    with col_r2:
        st.metric("Simulated Risk Score", f"{sim_risk:.1f}/100", delta=f"{delta_risk:+.1f}", delta_color="inverse")
    with col_r3:
        st.metric("Simulated Risk Level", sim_level)
        
    if sim_risk >= 70:
        st.error("🚨 **High Risk Scenario:** The simulated shock pushes the project beyond acceptable risk tolerance. Risk mitigation reserves must be released.")
    elif sim_risk >= 45:
        st.warning("⚠️ **Elevated Risk Scenario:** Moderate schedule & cost impact detected. Additional monitoring recommended.")
    else:
        st.success("✅ **Manageable Scenario:** The project buffer can absorb this perturbation without severe disruption.")
        
    st.write("##### 💡 Suggested Scenario Actions:")
    if sim_delay > 20:
        st.markdown("- ⏳ Fast-track parallel work streams and re-negotiate non-critical milestone delivery dates.")
    if sim_resource > 20:
        st.markdown("- 👥 Reallocate senior engineering capacity or engage approved backup vendors to mitigate team deficit.")
    if sim_budget > 25:
        st.markdown("- 💰 Trigger contingency budget authorization and conduct scope re-prioritization.")