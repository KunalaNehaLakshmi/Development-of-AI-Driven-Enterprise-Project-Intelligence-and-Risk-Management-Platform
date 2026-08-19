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
    f"Project Dependencies & Critical Chains ({domain_label})",
    "Inspect vendor dependencies, inter-module linkages, and critical path blocking factors."
)

project = st.session_state.get("selected_project")
if not project:
    st.warning("⚠️ No active project found. Please upload a project document or load a demo sample.")
    st.page_link("pages/2_Document_Upload.py", label="📤 Go to Document Upload & Demo Loader")
    st.stop()

# ============================================================
# DEPENDENCY RISK METRICS
# ============================================================

st.subheader("🔗 Dependency Risk Indicators")
features = project.get("features", {})

if is_it:
    vendor_dep = features.get("vendor_dependency_count", 0)
    ext_dep_score = features.get("external_dependency_score", 0)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Vendor API Dependencies", int(vendor_dep))
    with col2:
        st.metric("External Dependency Risk Score", f"{ext_dep_score}/100")
else:
    crit_deps = features.get("critical_dependency_count", 0)
    dep_delay = features.get("dependency_delay", 0)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Critical Path Links", int(crit_deps))
    with col2:
        st.metric("Cascading Supply Chain Delay", f"{dep_delay} days")

# ============================================================
# EXTRACTED DEPENDENCY INVENTORY
# ============================================================

st.divider()
st.subheader("📋 Document-Extracted Dependency Inventory")

dependencies = project.get("dependencies", [])

if dependencies:
    df_dep = pd.DataFrame(dependencies)
    if not df_dep.empty:
        df_dep.columns = [col.title() for col in df_dep.columns]
        
        def highlight_impact(s):
            val = str(s).upper()
            if "CRITICAL" in val or "HIGH" in val:
                return "background-color: rgba(239, 68, 68, 0.35); color: #fee2e2; font-weight: bold;"
            elif "MEDIUM" in val:
                return "background-color: rgba(245, 158, 11, 0.35); color: #fef3c7; font-weight: bold;"
            return "background-color: rgba(16, 185, 129, 0.25); color: #d1fae5;"

        if "Impact" in df_dep.columns:
            st.dataframe(df_dep.style.map(highlight_impact, subset=["Impact"]), use_container_width=True, hide_index=True)
        else:
            st.dataframe(df_dep, use_container_width=True, hide_index=True)
else:
    st.info("No specific external or inter-module dependencies were identified in the uploaded document.")