import streamlit as st
import pandas as pd
from utils.ui import inject_css, page_header

# ============================================================
# PAGE SETUP
# ============================================================

inject_css()

is_it = (st.session_state.get("user_type", "IT") == "IT")
domain_label = "IT Project" if is_it else "Non-IT Project"

page_header(
    f"Schedule Intelligence & Timeline Tracking ({domain_label})",
    "Monitor milestone progress, timeline slippages, and duration overrun forecasts."
)

project = st.session_state.get("selected_project")
if not project:
    st.warning("⚠️ No active project found. Please upload a project document or load a demo sample.")
    st.page_link("pages/2_Document_Upload.py", label="📤 Go to Document Upload & Demo Loader")
    st.stop()

# ============================================================
# TIMELINE & DURATION
# ============================================================

st.subheader("⏱️ Project Timeline & Duration Metrics")

features = project.get("features", {})
planned = features.get("planned_duration_days", 120.0)
actual = features.get("actual_duration_days", 135.0)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Baseline Planned Duration", f"{int(planned)} days")
with col2:
    st.metric("Forecasted / Actual Duration", f"{int(actual)} days")
with col3:
    variance_days = int(actual - planned) if (actual and planned) else 0
    st.metric("Schedule Variance", f"{'+' if variance_days > 0 else ''}{variance_days} days")

# ============================================================
# MILESTONES PROGRESS
# ============================================================

st.divider()
st.subheader("🏁 Key Milestone Completion Status")

milestones = project.get("milestones", [])

if milestones:
    df_m = pd.DataFrame(milestones)
    if not df_m.empty:
        for index, row in df_m.iterrows():
            name = row.iloc[0]
            progress = row.iloc[1]
            try:
                progress_val = float(progress)
            except Exception:
                progress_val = 0.0
                
            col_m1, col_m2 = st.columns([3, 1])
            with col_m1:
                st.write(f"**{name}**")
                st.progress(min(max(progress_val / 100.0, 0.0), 1.0))
            with col_m2:
                st.metric("Progress", f"{progress_val:.0f}%")
else:
    st.info("No explicit milestones were identified in the project documentation.")

# ============================================================
# SCHEDULE OVERRUN RISK (ML BASED)
# ============================================================

st.divider()
st.subheader("📈 Schedule Overrun Risk Assessment (ML)")

if is_it:
    schedule_overrun = features.get("schedule_overrun_pct", 0)
    st.metric("Forecasted Schedule Overrun", f"{schedule_overrun}%")
    if schedule_overrun <= 5:
        st.success("✅ Schedule is currently under control.")
    elif schedule_overrun <= 15:
        st.warning("⚠️ Schedule requires attention. Moderate overrun detected.")
    else:
        st.error("🚨 Severe schedule overrun risk identified! Immediate timeline re-baselining required.")
else:
    delay_days = features.get("delay_days", 0)
    dep_delay = features.get("dependency_delay", 0)
    st.metric("Observed Supply & Physical Delay", f"{delay_days} days (Direct) + {dep_delay} days (Cascading)")
    if delay_days <= 10:
        st.success("✅ Physical works schedule is operating within acceptable buffer limits.")
    elif delay_days <= 25:
        st.warning("⚠️ Work package delays detected on critical installation tasks.")
    else:
        st.error("🚨 Critical path delay exceeds project contingency reserve!")