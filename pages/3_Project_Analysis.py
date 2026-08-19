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
    f"Project Analysis & Work Packages ({domain_label})",
    "Track extracted action items, verify document completeness, and inspect health score breakdowns."
)

project_id = st.session_state.get("selected_project_id")
project = st.session_state.get("selected_project", {})

if not project_id or not project:
    st.warning("⚠️ No active project found. Please upload a project document or load a demo sample.")
    st.page_link("pages/2_Document_Upload.py", label="📤 Go to Document Upload & Demo Loader")
    st.stop()

# ============================================================
# PROJECT HEALTH & OVERVIEW
# ============================================================

st.subheader("📊 Overall Project Health Index")
health = float(project.get("health_score", 70.0))
st.progress(max(0.0, min(1.0, health / 100.0)))

if health >= 70:
    st.success(f"✅ **Health Index: {health:.1f}/100** — Project execution parameters are within healthy margins.")
elif health >= 45:
    st.warning(f"⚠️ **Health Index: {health:.1f}/100** — Moderate risk detected; monitor critical path dependencies.")
else:
    st.error(f"🚨 **Health Index: {health:.1f}/100** — Critical schedule or resource deficit detected; immediate intervention required.")

# ============================================================
# ACTION ITEMS & TASKS
# ============================================================

st.divider()
st.subheader("📋 Action Items & Task Assignments")
st.write("Identified and structured automatically from project specification, meeting transcripts, or task logs:")

action_items = project.get("action_items", [])
if action_items:
    df_actions = pd.DataFrame(action_items)
    if not df_actions.empty:
        df_actions.columns = [col.title() for col in df_actions.columns]
        st.dataframe(df_actions, use_container_width=True, hide_index=True)
else:
    st.info("No pending action items were identified in the uploaded document.")

# ============================================================
# MISSING INFORMATION & AUDIT GAPS
# ============================================================

st.divider()
st.subheader("📑 Document Information Completeness Gaps")

missing_info = project.get("missing_info", [])
if missing_info:
    st.warning("**The following critical project parameters were not found in the uploaded text:**")
    for info in missing_info:
        st.markdown(f"- ⚠️ **Missing Parameter:** {info}")
    st.caption("ℹ️ Incomplete specification documentation increases uncertainty penalties in the AI risk model.")
else:
    st.success("✅ No critical scope or parameter gaps were detected.")

# ============================================================
# RAW DOCUMENT PREVIEW
# ============================================================

documents = st.session_state.get("documents", {})
if documents:
    st.divider()
    st.subheader("📄 Ingested Document Text Preview")
    for filename, text in documents.items():
        with st.expander(f"📁 {filename} ({len(text):,} characters)"):
            st.text_area("Content Preview", text[:10000] + ("..." if len(text) > 10000 else ""),
                         height=250, disabled=True, key=f"preview_{filename}")