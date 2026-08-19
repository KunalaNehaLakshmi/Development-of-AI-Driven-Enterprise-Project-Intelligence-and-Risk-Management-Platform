import streamlit as st
from utils.ui import inject_css, page_header

# ============================================================
# PAGE SETUP
# ============================================================

inject_css()

is_it = (st.session_state.get("user_type", "IT") == "IT")
domain_label = "IT Project" if is_it else "Non-IT Project"

page_header(
    f"💡 AI Strategic Recommendations ({domain_label})",
    "Dynamic risk mitigation actions and operational playbooks tailored to observed project risks."
)

project = st.session_state.get("selected_project")
if not project:
    st.warning("⚠️ No active project found. Please upload a project document or load a demo sample.")
    st.page_link("pages/2_Document_Upload.py", label="📤 Go to Document Upload & Demo Loader")
    st.stop()

features = project.get("features", {})
risk_level = str(project.get("risk_level", "LOW")).upper()
risk_score = float(project.get("risk_score", 0.0))

# ============================================================
# GENERATE DYNAMIC RECOMMENDATIONS
# ============================================================

st.subheader("🎯 Prioritized Action Plan")

recs = []

if is_it:
    # IT Domain Recommendations
    if features.get("team_turnover_pct", 0) > 15:
        recs.append(("🚨 High Priority", "Knowledge Retention & Pair Programming", "Team turnover exceeds 15%. Implement pair-programming on core architecture modules and mandate asynchronous documentation of microservice APIs."))
    if features.get("tech_complexity_score", 0) > 70:
        recs.append(("🚨 High Priority", "Architectural Spike & Refactoring", "High technical complexity detected. Schedule dedicated sprint spikes to benchmark database sharding and latency bottlenecks before production rollout."))
    if features.get("vendor_dependency_count", 0) >= 2:
        recs.append(("⚠️ Medium Priority", "Vendor SLA Tightening & Circuit Breakers", "Multiple third-party API dependencies identified. Implement circuit breakers and fallback caching mocks in case vendor endpoints experience downtime."))
    if features.get("schedule_overrun_pct", 0) > 10:
        recs.append(("⚠️ Medium Priority", "Sprint Scope De-Scoping", "Schedule slippage detected. Move non-critical 'nice-to-have' user stories to the Phase 2 backlog to safeguard the hard launch deadline."))
else:
    # Non-IT Domain Recommendations
    if features.get("dependency_delay", 0) > 7:
        recs.append(("🚨 High Priority", "Supply Chain Escalation & Buffer Stocks", "Material / hardware shipment delay exceeds 7 days. Issue formal vendor default notice and explore expedited airfreight options."))
    if features.get("resource_availability", 1.0) < 0.85:
        recs.append(("🚨 High Priority", "Subcontractor Mobilization", "On-site staffing deficit detected. Mobilize standby subcontracting labor teams to maintain physical construction and track laying cadence."))
    if features.get("security_audit_progress", 100) < 70:
        recs.append(("⚠️ Medium Priority", "Statutory Safety Certification Readiness", "Statutory safety audit is trailing schedule. Conduct pre-audit inspection drills to avoid commissioner clearance rejection."))
    if features.get("delay_days", 0) > 15:
        recs.append(("⚠️ Medium Priority", "Critical Path Fast-Tracking", "Compress non-dependent civil work packages by scheduling parallel 2-shift operations on high-slack activities."))

# Always add standard baseline recommendations
recs.append(("ℹ️ Standard Practice", "Weekly Risk Board Reviews", "Maintain automated risk scoring updates across all stakeholder syncs."))
recs.append(("ℹ️ Standard Practice", "Documentation Synchronization", "Synchronize Jira / Project Tracker logs with the AI Project Intelligence Knowledge Base."))

for priority, title, desc in recs:
    with st.container(border=True):
        col_t1, col_t2 = st.columns([1, 4])
        with col_t1:
            st.markdown(f"**{priority}**")
        with col_t2:
            st.markdown(f"##### {title}")
            st.write(desc)

# ============================================================
# INTERACTIVE ACTION CHECKLIST
# ============================================================

st.divider()
st.subheader("✅ Executive Mitigation Checklist")

for idx, (priority, title, _) in enumerate(recs):
    st.checkbox(f"Execute: {title}", key=f"rec_chk_{idx}")