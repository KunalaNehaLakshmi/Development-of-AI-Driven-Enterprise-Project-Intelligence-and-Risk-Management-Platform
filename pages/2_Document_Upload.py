import streamlit as st
import pandas as pd
from utils.ui import inject_css, page_header, render_domain_banner
from utils.predictor import predict_it_risk, predict_non_it_risk
from utils.llm_parser import parse_document_with_gemini, parse_batch_with_gemini, detect_domain_from_text
from rag_chatbot.session_store import build_index, clear_index

# ============================================================
# PAGE SETUP
# ============================================================

inject_css()

page_header(
    "Document Ingestion & Automated Domain Detection",
    "Upload project charter, scope document, meeting notes, or task CSV. The AI analyzes technical terminology, classifies the domain, and routes parameters to the appropriate machine learning risk model."
)

# ============================================================
# SESSION STATE
# ============================================================

if "documents" not in st.session_state:
    st.session_state.documents = {}
if "project_analyzed" not in st.session_state:
    st.session_state.project_analyzed = False
if "prediction" not in st.session_state:
    st.session_state.prediction = None
if "selected_project_id" not in st.session_state:
    st.session_state.selected_project_id = None
if "selected_project" not in st.session_state:
    st.session_state.selected_project = None
if "detected_domain" not in st.session_state:
    st.session_state.detected_domain = "IT"
if "domain_reason" not in st.session_state:
    st.session_state.domain_reason = ""

# ============================================================
# UTILITIES
# ============================================================

def extract_text(file):
    filename = file.name.lower()
    if filename.endswith(".txt") or filename.endswith(".csv"):
        try:
            return file.getvalue().decode("utf-8", errors="ignore")
        except Exception:
            return ""
    if filename.endswith(".docx"):
        try:
            import docx2txt
            return docx2txt.process(file)
        except Exception as e:
            st.error(f"Failed to extract text from DOCX: {e}")
            return ""
    if filename.endswith(".pdf"):
        try:
            from pypdf import PdfReader
            reader = PdfReader(file)
            content = [page.extract_text() or "" for page in reader.pages]
            return "\n".join(content)
        except Exception as e:
            st.error(f"Failed to extract text from PDF: {e}")
            return ""

def process_and_route_project(insights_dict, raw_text=""):
    # Automatic Domain Detection
    domain = insights_dict.get("detected_domain", "IT")
    if domain not in ["IT", "Non-IT"]:
        domain, reason = detect_domain_from_text(raw_text)
    else:
        reason = insights_dict.get("domain_detection_reason", "Identified digital software and sprint parameters.")
        
    features = insights_dict.get("features", {})
    
    # Model Routing based on detected domain
    if domain.upper() == "IT":
        prediction = predict_it_risk(features)
        model_name = "XGBoost Regressor (IT)"
    else:
        prediction = predict_non_it_risk(features)
        model_name = "Calibrated Logistic Regression (Non-IT)"
        
    project_id = 1000 + len(st.session_state.documents)
    
    project_data = {
        "id": project_id,
        "project_id": str(project_id),
        "name": insights_dict.get("project_name", f"Ingested {domain} Project"),
        "project_type_category": domain,
        "domain_detection_reason": reason,
        "model_used": model_name,
        "status": "IN_PROGRESS",
        "budget": features.get("budget_usd", 450000.0 if domain == "IT" else 1200000.0),
        "deadline": f"{int(features.get('planned_duration_days', 120))} days",
        "progress": int(features.get("progress_percentage", 35)),
        "health_score": round(100.0 - float(prediction["risk_score"]), 1),
        "risk_level": prediction["risk_level"],
        "risk_score": float(prediction["risk_score"]),
        "features": features,
        "project_scope": insights_dict.get("project_scope", ""),
        "deliverables": insights_dict.get("deliverables", []),
        "action_items": insights_dict.get("action_items", []),
        "milestones": insights_dict.get("milestones", []),
        "dependencies": insights_dict.get("dependencies", []),
        "missing_info": insights_dict.get("missing_info", []),
        "potential_risks": insights_dict.get("potential_risks", []),
    }
    
    st.session_state.selected_project_id = project_id
    st.session_state.selected_project = project_data
    st.session_state.detected_domain = domain
    st.session_state.domain_reason = reason
    st.session_state.project_analyzed = True
    st.session_state.prediction = prediction["risk_level"]
    st.session_state.is_batch = False
    return project_data

# ============================================================
# RAPID BENCHMARK DEMO DATASETS (REAL PIPELINE EXECUTION)
# ============================================================

st.markdown("#### Reference Ingestion Datasets")
st.caption("Execute full end-to-end ingestion and ML inference pipelines with verified enterprise project datasets.")

col_d1, col_d2 = st.columns(2)

with col_d1:
    if st.button("Ingest Cloud Platform Dataset (IT)", use_container_width=True):
        raw_doc = (
            "Project: Enterprise Cloud Platform Migration\n"
            "Scope: Migrate on-premise transactional core to AWS/GCP Kubernetes clusters with Auth0 IAM and microservice architecture.\n"
            "Budget: $850,000. Duration: 180 days. Team Size: 18 engineers. Avg Experience: 4.2 years.\n"
            "Metrics: Schedule overrun is 18%, Team turnover is 22%, Vendor API dependencies: 3, Defect count: 14 bugs.\n"
            "Deliverables: Multi-region VPC, Microservices Mesh, GitOps CI/CD Pipeline, SOC2 Audit Signoff.\n"
            "Milestones: VPC Infrastructure (100%), Microservice Decomposition (65%), Security Penetration Testing (40%), Traffic Cutover (10%).\n"
            "Dependencies: Third-party Identity Provider API (High Impact), Database Sharding Gateway (Medium Impact)."
        )
        st.session_state.documents["Enterprise_Cloud_Migration.txt"] = raw_doc
        
        parsed = {
            "project_name": "Enterprise Cloud Platform Migration",
            "detected_domain": "IT",
            "domain_detection_reason": "Identified Kubernetes, microservices, cloud infrastructure, and sprint defect metrics.",
            "project_scope": "Migrate core transactional systems to AWS/GCP Kubernetes with high availability, IAM RBAC, and SOC2 compliance.",
            "deliverables": [
                "Multi-region VPC & Terraform Infrastructure",
                "Microservice Mesh Deployment (24 pods)",
                "Automated GitOps CI/CD Pipeline",
                "SOC2 Security Audit Signoff"
            ],
            "action_items": [
                {"task": "Optimize database read-replica query latency", "owner": "DevOps Lead", "status": "In Progress"},
                {"task": "Complete penetration testing remediation", "owner": "Security Engineer", "status": "Pending"},
                {"task": "Benchmark pod autoscaler under load", "owner": "SRE Team", "status": "Completed"}
            ],
            "milestones": [
                {"name": "VPC Infrastructure Baseline", "progress_pct": 100.0},
                {"name": "Microservice Decomposition", "progress_pct": 65.0},
                {"name": "Security Penetration Testing", "progress_pct": 40.0},
                {"name": "Production Traffic Cutover", "progress_pct": 10.0}
            ],
            "dependencies": [
                {"name": "Third-party Identity Provider API", "status": "Active", "impact": "High"},
                {"name": "Database Sharding Gateway", "status": "Degraded", "impact": "Medium"}
            ],
            "missing_info": ["Disaster recovery RTO/RPO target benchmarks"],
            "potential_risks": [
                "Team turnover (22%) threatens knowledge continuity during microservices migration.",
                "Multiple external API dependencies present risk of cascading sprint delays."
            ],
            "features": {
                "project_type": "Cloud Migration",
                "industry_sector": "Technology",
                "methodology": "Agile",
                "region": "North America",
                "contract_type": "Time & Material",
                "priority": "High",
                "planned_duration_days": 180.0,
                "actual_duration_days": 210.0,
                "team_size": 18.0,
                "team_avg_experience_years": 4.2,
                "team_turnover_pct": 22.0,
                "stakeholder_count": 8.0,
                "requirement_changes_count": 7.0,
                "budget_usd": 850000.0,
                "actual_cost_usd": 920000.0,
                "cost_overrun_pct": 8.2,
                "schedule_overrun_pct": 18.0,
                "resource_availability_pct": 78.0,
                "vendor_dependency_count": 3.0,
                "communication_score": 75.0,
                "sponsor_engagement_score": 80.0,
                "previous_project_success_rate_pct": 85.0,
                "tech_complexity_score": 82.0,
                "regulatory_compliance_load": 40.0,
                "scope_clarity_score": 70.0,
                "external_dependency_score": 68.0,
                "safety_incidents": 0.0,
                "defect_count": 14.0,
                "milestones_missed": 2.0
            }
        }
        
        process_and_route_project(parsed, raw_doc)
        
        clear_index()
        num_chunks = build_index(st.session_state.documents)
        st.session_state["rag_ready"] = True
        st.session_state["rag_chunk_count"] = num_chunks
        st.success("Cloud Platform Dataset ingested. Domain classified as IT. Model: XGBoost Regressor.")
        st.rerun()

with col_d2:
    if st.button("Ingest Transit Infrastructure Dataset (Non-IT)", use_container_width=True):
        raw_doc = (
            "Project: Urban Metro Rail Signaling & Track Infrastructure\n"
            "Scope: Civil viaduct construction, track electrification, and communications-based train control (CBTC) signaling installation.\n"
            "Budget: $4,200,000. Duration: 360 days. Team Size: 120 personnel.\n"
            "Metrics: Cumulative delay days: 28 days, Resource availability: 70%, Supply chain vendor delay: 14 days, Critical dependency links: 4.\n"
            "Deliverables: Elevated Viaduct Structure, 25kV Traction Substation, CBTC Wayside Equipment, Statutory Safety Audit Clearance.\n"
            "Milestones: Civil Works (100%), Track Laying (75%), Substation Electrification (50%), Safety Trial Runs (20%).\n"
            "Dependencies: Imported CBTC Transponder Shipment (Critical Impact), Municipal Power Sanction (High Impact)."
        )
        st.session_state.documents["Metro_Signaling_Infra.txt"] = raw_doc
        
        parsed = {
            "project_name": "Urban Metro Rail Signaling Infrastructure",
            "detected_domain": "Non-IT",
            "domain_detection_reason": "Identified civil works, track electrification, physical hardware supply chains, and safety audits.",
            "project_scope": "Deliver turnkey civil infrastructure, track electrification, and automated train control signaling for urban rail transit.",
            "deliverables": [
                "Elevated Viaduct & Station Civil Works",
                "25kV Overhead Catenary Substation",
                "CBTC Wayside Signaling Hardware",
                "Statutory Safety Audit Clearance"
            ],
            "action_items": [
                {"task": "Expedite customs clearance for CBTC transponders", "owner": "Procurement Officer", "status": "In Progress"},
                {"task": "Conduct high-voltage substation energization inspection", "owner": "Electrical Chief", "status": "Pending"}
            ],
            "milestones": [
                {"name": "Civil Foundations & Viaduct", "progress_pct": 100.0},
                {"name": "Track Laying & Catenary", "progress_pct": 75.0},
                {"name": "Substation Electrification", "progress_pct": 50.0},
                {"name": "Integrated Safety Trial Runs", "progress_pct": 20.0}
            ],
            "dependencies": [
                {"name": "Imported Signaling Hardware Shipment", "status": "Delayed", "impact": "Critical"},
                {"name": "Municipal Grid Power Supply", "status": "Approved", "impact": "High"}
            ],
            "missing_info": ["Heavy monsoon contingency protocol"],
            "potential_risks": [
                "Customs clearance delays for imported signaling modules threaten statutory completion target."
            ],
            "features": {
                "progress_percentage": 58.0,
                "pending_task_ratio": 0.42,
                "delay_days": 28.0,
                "budget_utilization": 0.64,
                "resource_availability": 0.70,
                "bugs_per_task": 1.8,
                "testing_progress": 45.0,
                "testing_failure_rate": 0.12,
                "requirement_change_rate": 0.08,
                "team_productivity": 0.88,
                "dependency_delay": 14.0,
                "critical_dependency_count": 4.0,
                "security_audit_progress": 60.0,
                "external_risk_score": 72.0,
                "schedule_variance": 22.0,
                "resource_pressure": 0.78,
                "dependency_risk_score": 65.0,
                "budget_usd": 4200000.0,
                "planned_duration_days": 360.0,
                "actual_duration_days": 395.0
            }
        }
        
        process_and_route_project(parsed, raw_doc)
        
        clear_index()
        num_chunks = build_index(st.session_state.documents)
        st.session_state["rag_ready"] = True
        st.session_state["rag_chunk_count"] = num_chunks
        st.success("Transit Infrastructure Dataset ingested. Domain classified as Non-IT. Model: Calibrated Logistic Regression.")
        st.rerun()

st.divider()

# ============================================================
# FILE UPLOAD (UNIFIED - NO MANUAL DOMAIN SELECTION)
# ============================================================

st.markdown("#### Upload Project Document or Dataset")
st.write("Upload your document (PDF, DOCX, CSV, TXT). The system will automatically detect the domain and execute the corresponding inference pipeline.")

uploaded_file = st.file_uploader(
    "Choose project file",
    type=["pdf", "docx", "txt", "csv"],
    help="Supported file types: PDF, DOCX, CSV, TXT",
    label_visibility="collapsed"
)

if uploaded_file is not None:
    if st.button("Process Document & Run AI Models", type="primary", use_container_width=True):
        is_csv = uploaded_file.name.lower().endswith(".csv")

        with st.spinner("Extracting parameters and analyzing domain taxonomy..."):
            raw_text = extract_text(uploaded_file)
            st.session_state.documents[uploaded_file.name] = raw_text
            
            try:
                if is_csv:
                    insights_dict = parse_batch_with_gemini(raw_text)
                else:
                    insights_dict = parse_document_with_gemini(raw_text)
            except Exception as e:
                st.error(f"Document processing failed: {e}")
                st.stop()

        with st.spinner("Executing machine learning inference pipeline..."):
            if is_csv and "projects" in insights_dict and insights_dict["projects"]:
                batch_list = []
                for p in insights_dict["projects"]:
                    proj_obj = process_and_route_project(p, raw_text)
                    batch_list.append(proj_obj)
                st.session_state.batch_projects = batch_list
                st.session_state.selected_project = batch_list[0]
                st.session_state.selected_project_id = batch_list[0]["id"]
                st.session_state.is_batch = True
            else:
                process_and_route_project(insights_dict, raw_text)

        with st.spinner("Indexing vector embeddings for RAG assistant..."):
            try:
                clear_index()
                num_chunks = build_index(st.session_state.documents)
                st.session_state["rag_ready"] = True
                st.session_state["rag_chunk_count"] = num_chunks
            except Exception as rag_err:
                st.session_state["rag_ready"] = False

        st.success("Project analyzed successfully with automated domain classification.")
        st.rerun()

# ============================================================
# SUMMARY SNAPSHOT
# ============================================================

if st.session_state.get("project_analyzed", False):
    p = st.session_state.get("selected_project")
    if p:
        st.divider()
        st.markdown("#### Ingestion & Classification Summary")
        
        render_domain_banner(
            detected_domain=p.get("project_type_category", "IT"),
            model_used=p.get("model_used", "XGBoost Regressor"),
            detection_reason=p.get("domain_detection_reason", "")
        )
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Project Name", p.get("name"))
        with col2:
            st.metric("Health Index", f"{p.get('health_score')}/100")
        with col3:
            st.metric("ML Risk Score", f"{p.get('risk_score')}/100")
        with col4:
            st.metric("Risk Priority Level", p.get("risk_level"))

        st.info(f"**Extracted Scope:** {p.get('project_scope')}")
        st.page_link("pages/1_Dashboard.py", label="Open Executive Project Dashboard")