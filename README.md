# 🚀 AI-Driven Enterprise Project Intelligence & Risk Management Platform

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-1.8%2B-EB5424?style=for-the-badge&logoColor=white)
![CatBoost](https://img.shields.io/badge/CatBoost-Ensemble-FDB813?style=for-the-badge&logoColor=black)
![Google GenAI](https://img.shields.io/badge/Generative_AI-Google_GenAI-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![Qdrant](https://img.shields.io/badge/Vector_DB-Qdrant-DC2626?style=for-the-badge&logoColor=white)

An enterprise-grade, end-to-end intelligent platform engineered to predict, analyze, simulate, and mitigate project failure risks across complex **IT & Technical Engineering** and **Non-IT / Business Operations** domains. Powered by dual-pipeline machine learning classifiers (achieving up to **95.96% accuracy** and **0.9939 ROC-AUC**), graph-theoretic dependency tracking (CPM), real-time What-If scenario simulations, and a Retrieval-Augmented Generation (RAG) conversational advisor.

---

## 📑 Table of Contents

- [Executive Summary](#-executive-summary)
- [Key Capabilities & Modules](#-key-capabilities--modules)
- [End-to-End System Architecture](#-end-to-end-system-architecture)
- [Dual-Workspace Domain Architecture](#-dual-workspace-domain-architecture)
- [Machine Learning & Analytical Foundations](#-machine-learning--analytical-foundations)
- [RAG Conversational Assistant](#-rag-conversational-assistant)
- [Streamlit UI & Multi-Page Layout](#-streamlit-ui--multi-page-layout)
- [FastAPI Backend & API Endpoints](#-fastapi-backend--api-endpoints)
- [Repository & File Structure](#-repository--file-structure)
- [Installation & Getting Started](#-installation--getting-started)
- [Demo Credentials & Sample Projects](#-demo-credentials--sample-projects)
- [Environment Configuration](#-environment-configuration)
- [Model Training & Database Seeding](#-model-training--database-seeding)

---

## 🌟 Executive Summary

Enterprise projects routinely encounter schedule slippages, budget overruns, resource bottlenecks, and communication breakdowns. Traditional project management tools provide backward-looking reports rather than predictive risk intelligence.

This platform bridges that gap by combining:
1. **Predictive AI/ML Engines**: High-precision XGBoost and CatBoost models trained on 50,000+ telemetry records to classify project health, delay probabilities, and failure risk before critical milestones are missed.
2. **Deterministic Schedule & Graph Intelligence**: Critical Path Method (CPM) and NetworkX-powered dependency graph analysis to locate bottleneck tasks and single points of failure.
3. **Interactive What-If Simulation**: Dynamic constraint modeling allowing leaders to stress-test scenarios (e.g., turnover spikes, scope changes, budget reductions) in real-time.
4. **Document AI & RAG Chatbot**: Automated extraction of project charter documents (PDF, DOCX, PPTX) linked to a Qdrant vector database and Google GenAI LLM for deep contextual question answering.
5. **Role-Based Access Control (RBAC)**: Domain-isolated workspaces specifically tailored for technical teams (DevOps, Cloud, Software) and operational teams (Mining, Healthcare, Agriculture, Logistics).

---

## ⚡ Key Capabilities & Modules

### 1. 📂 Document Intelligence & Multi-Upload
- Ingests Project Charters, Statements of Work (SOW), and Project Plans in PDF, DOCX, and PPTX formats.
- Supports single-document parsing and batch multi-project uploads with automatic metadata extraction (budget, team size, duration, stakeholders, priority, methodology).
- Fallback heuristic extraction paired with LLM and Vision-based multi-modal parsers.

### 2. 📊 Executive Project Dashboard
- At-a-glance KPI summary: Project Health Index, Risk Category, Schedule Variance, Budget Burn Rate, and Delivery Confidence.
- Multi-dimensional radar charts contrasting planned vs. actual project metrics.
- High-level telemetry distributions across risk tiers (Low, Medium, High, Critical).

### 3. 🔍 Deep Project Analysis & Telemetry
- Granular breakdown of 24 to 39 telemetry parameters including Team Turnover %, Requirement Change Count, Resource Availability %, and Communication Score.
- Automated health metric calculations: Cost Performance Index (CPI), Schedule Performance Index (SPI), and Defect Density.

### 4. 🎯 Risk Forecasting & Explainability
- ML-driven risk probability scores with confidence ratings.
- Categorical risk attribution: Resource Risk, Technical Complexity Risk, Governance Risk, and Vendor Dependency Risk.
- Feature importance visualization showing exact drivers pushing the risk level upward or downward.

### 5. ⏱️ Schedule Intelligence & Milestone Forecasting
- Milestone variance forecasting, timeline drift detection, and delay impact calculations.
- Projected completion dates compared against baseline contractual deadlines.

### 6. 🕸️ Graph-Theoretic Dependency Analysis
- Interactive NetworkX dependency graphs mapping all tasks and work breakdown structures (WBS).
- Automated Critical Path Method (CPM) calculation highlighting blocking bottlenecks and zero-float chains.
- Cycle detection to prevent circular dependency deadlocks.

### 7. 🎛️ Interactive What-If Simulation Engine
- Parameter sliders for dynamic sensitivity analysis:
  - Budget adjustments ($\pm 50\%$)
  - Team size expansion/reduction
  - Turnover spike simulations
  - Requirement volatility and scope creep
  - Resource availability adjustments
- Instant ML recalculation displaying Delta Risk ($\Delta$) and new projected project health status.

### 8. 💡 Automated Preventive Mitigation & Recommendations
- AI-synthesized, prioritized action items categorized by urgency (Immediate, Short-term, Long-term).
- Tailored strategies addressing identified bottlenecks (e.g., buffer adjustments, vendor SLA enforcement, scope freeze).

### 9. 🤖 RAGBot AI Assistant
- Context-aware chatbot grounded directly in uploaded project documents and active database telemetry.
- Semantic vector retrieval using Qdrant and Google GenAI embeddings.
- Full citation grounding with source page and section referencing.

---

## 🏗️ End-to-End System Architecture

```mermaid
graph TB
    subgraph UI_Layer [Frontend Layer - Streamlit Multi-Page]
        Auth[RBAC / Authentication Gate]
        WS[Workspace Selector: IT vs Non-IT]
        Upload[Document Upload & Parser]
        Dash[Executive Dashboard]
        Analysis[Project Telemetry Analysis]
        Risk[Risk Intelligence & ML Radar]
        Sched[Schedule Intelligence & CPM]
        Graph[Dependency & Bottleneck Graph]
        Sim[What-If Simulation Engine]
        RAGUI[RAGBot AI Assistant]
    end

    subgraph API_Layer [API Layer - FastAPI Service :8000]
        Router[API Gateway /api/v1]
        AuthAPI[/auth]
        ProjAPI[/projects]
        TaskAPI[/tasks & /dependencies]
        RiskAPI[/risk & /health]
        SimAPI[/scenario]
        DocAPI[/documents]
        ChatAPI[/chats]
        RecomAPI[/recommendations]
    end

    subgraph Intelligence_Layer [Data & AI Intelligence Core]
        XGB_IT[IT XGBoost Model<br/>Accuracy: 93.49% | AUC: 0.9859]
        XGB_NonIT[Non-IT XGBoost Ensemble<br/>Accuracy: 95.96% | AUC: 0.9939]
        CPM_Engine[NetworkX CPM Engine]
        Qdrant_DB[(Qdrant Vector DB)]
        LLM[Google GenAI / Gemini API]
        SQLite[(SQLite / PostgreSQL DB)]
    end

    %% Interactions
    Auth --> WS
    WS --> Upload --> Dash --> Analysis --> Risk --> Sched --> Graph --> Sim --> RAGUI

    UI_Layer <==> |REST HTTP & JSON| Router

    Router --> AuthAPI --> SQLite
    Router --> ProjAPI --> SQLite
    Router --> TaskAPI --> SQLite
    Router --> TaskAPI --> CPM_Engine
    Router --> RiskAPI --> XGB_IT
    Router --> RiskAPI --> XGB_NonIT
    Router --> SimAPI --> XGB_IT
    Router --> SimAPI --> XGB_NonIT
    Router --> DocAPI --> Qdrant_DB
    Router --> DocAPI --> SQLite
    Router --> ChatAPI --> SQLite
    
    RAGUI <==> |Semantic Retrieval & Embeddings| Qdrant_DB
    RAGUI <==> |Contextual Prompting| LLM
```

---

## 🏢 Dual-Workspace Domain Architecture

The platform provides two specialized workspace domains to ensure accurate domain-specific risk modeling:

| Dimension | 💻 IT & Technical Engineering | 🏭 Non-IT & Business Operations |
| :--- | :--- | :--- |
| **Target Domains** | Software, Cloud Migration, DevOps, Cybersecurity, Microservices | Infrastructure, Mining, Logistics, Healthcare, Agriculture, Supply Chain |
| **Core ML Model** | XGBoost & CatBoost (24 Features) | Tuned XGBoost & Stacking Ensemble (39 Engineered Features) |
| **Model Accuracy** | **93.49%** (Precision: 92.28%, Recall: 89.80%) | **95.96%** (Precision: 94.62%, Recall: 94.40%) |
| **ROC-AUC Score** | **0.9859** | **0.9939** |
| **Key Telemetry Focus** | Tech Complexity, Defect Count, Requirement Churn, Sprint Velocity | Safety Incidents, Regulatory Load, Vendor Dependencies, Logistics Lead Times |
| **Pages Range** | Pages 1–10 (`1_Dashboard.py` to `10_AI_Assistant.py`) | Pages 11–20 (`11_Non_IT_Dashboard.py` to `20_Non_IT_AI_Assistant.py`) |

---

## 🧪 Machine Learning & Analytical Foundations

### Feature Telemetry Matrix
The models evaluate comprehensive multidimensional project signals:

- **Organizational & Team Dynamics**: `team_size`, `team_avg_experience_years`, `team_turnover_pct`, `stakeholder_count`, `communication_score`, `sponsor_engagement_score`.
- **Scope & Volatility**: `planned_duration_days`, `requirement_changes_count`, `scope_clarity_score`, `budget_usd`.
- **Execution & Complexity**: `tech_complexity_score`, `regulatory_compliance_load`, `external_dependency_score`, `resource_availability_pct`, `vendor_dependency_count`.
- **Quality & Incident Telemetry**: `defect_count`, `safety_incidents`, `milestones_missed`, `previous_project_success_rate_pct`.
- **Engineered Non-IT Interaction Ratios**: `milestone_stress_ratio`, `turnover_experience_risk`, `defect_per_k_budget`, `governance_score`, `complexity_pressure`, `vendor_safety_risk`, `req_change_intensity`, `risk_multiplier`.

### Model Evaluation Benchmarks

```
IT Model (XGBoost 24-Feature Pipeline):
├── Training Samples: 22,500 records
├── Testing Samples:   7,500 records
├── Accuracy:          93.49%
├── Precision:         92.28%
├── Recall:            89.80%
├── F1-Score:          91.02%
└── ROC-AUC:           0.9859

Non-IT Model (39-Feature Tuned Ensemble):
├── Training Samples: 37,500 records
├── Testing Samples:  12,500 records
├── Accuracy:          95.96%
├── Precision:         94.62%
├── Recall:            94.40%
├── F1-Score:          94.51%
├── ROC-AUC:           0.9939
└── Decision Cutoff:   0.48 (Optimal F1 threshold)
```

---

## 💬 RAG Conversational Assistant

The platform integrates an enterprise-grade Retrieval-Augmented Generation (RAG) system located under `rag_chatbot/`:

```
Uploaded Document (PDF / DOCX / PPTX)
                 │
                 ▼
        [Document Chunker]
  (Recursive character splitting: 500-1000 tokens)
                 │
                 ▼
     [Vector Embeddings Generator]
 (Google GenAI / Local Embedding Fallbacks)
                 │
                 ▼
      [(Qdrant Vector Database)]
                 │
  User Query ──► [Semantic Hybrid Search] ──► [Grounding Engine] ──► [LLM Generation]
                                                                          │
                                                                          ▼
                                                              Answer + Citations + Page #
```

- **Zero Hallucination Guardrails**: The grounding engine injects strict context boundaries and cites source document metadata.
- **Persistent Session Storage**: Chat sessions are stored per project and user in SQLite/PostgreSQL.

---

## 🖥️ Streamlit UI & Multi-Page Layout

The frontend is structured into an intuitive multi-page layout with role-based routing:

```
current/AI_project/final_project/
├── app.py                            # Authentication & Main Session Gateway
├── landing.py                        # Landing Page Layout
└── pages/
    ├── 1_Dashboard.py                # IT Executive Overview
    ├── 2_Document_Upload.py          # IT Document Parser & Multi-Upload
    ├── 3_Project_Analysis.py         # IT Detailed Telemetry Analysis
    ├── 4_Risk_Intelligence.py        # IT ML Risk Forecasting & Explanations
    ├── 5_Schedule_Intelligence.py    # IT Schedule Forecasting & Milestones
    ├── 6_Dependencies.py             # IT NetworkX Dependency Graph & CPM
    ├── 7_What_If_Simulation.py       # IT Dynamic Scenario Simulator
    ├── 8_Recommendations.py          # IT AI-Driven Mitigations
    ├── 9_Documentation.py            # IT Risk Report Generator & Export
    ├── 10_AI_Assistant.py            # IT Grounded RAGBot Chatbot
    │
    ├── 11_Non_IT_Dashboard.py        # Non-IT Operations Dashboard
    ├── 12_Non_IT_Document_Upload.py  # Non-IT Document Processing
    ├── 13_Non_IT_Project_Analysis.py # Non-IT Telemetry Analysis
    ├── 14_Non_IT_Risk_Intelligence.py# Non-IT Risk Forecasting
    ├── 15_Non_IT_Schedule_Intelligence.py # Non-IT Milestone Drift
    ├── 16_Non_IT_Dependencies.py     # Non-IT Operational Dependency Trees
    ├── 17_Non_IT_What_If_Simulation.py    # Non-IT Scenario Simulator
    ├── 18_Model_Intelligence.py      # ML Model Evaluation & Transparency
    ├── 19_Non_IT_Documentation.py    # Non-IT Governance & Export
    └── 20_Non_IT_AI_Assistant.py     # Non-IT Operational RAGBot
```

---

## 🔌 FastAPI Backend & API Endpoints

The backend is built with FastAPI and OpenAPI Swagger docs available at `http://127.0.0.1:8000/docs`.

| Endpoint | Method | Tag | Description |
| :--- | :---: | :--- | :--- |
| `/health` | `GET` | System Health | Service health and version check |
| `/api/v1/auth/login` | `POST` | Authentication | Authenticate user credentials and return JWT token |
| `/api/v1/projects/` | `GET` / `POST` | Projects | Retrieve and create project records |
| `/api/v1/tasks/` | `GET` / `POST` | Tasks | Query and update task schedules and milestones |
| `/api/v1/dependencies/` | `GET` / `POST` | Dependencies | Dependency edges and critical path calculation |
| `/api/v1/metrics/{id}` | `GET` | Metrics | Performance metrics (CPI, SPI, Burn rate) |
| `/api/v1/risk/predict` | `POST` | Risk Forecasting | Execute ML risk inference for a given project |
| `/api/v1/health/evaluate` | `POST` | Health Assessment | Score overall project health index |
| `/api/v1/deadline/forecast`| `POST` | Deadline Analysis | Forecast delay probabilities and slip dates |
| `/api/v1/scenario/simulate`| `POST` | What-If Simulation | Compute delta risk under simulated parameter shifts |
| `/api/v1/recommendations/`| `GET` | Recommendations | Fetch prioritized risk mitigation actions |
| `/api/v1/documents/upload` | `POST` | Documents | Ingest, parse, and vectorize project documents |
| `/api/v1/chats/` | `GET` / `POST` | Chat History | Fetch and append conversational RAG sessions |

---

## 📁 Repository & File Structure

```
FINAL/
├── AI_Project_Intelligence_Risk_Management_Platform (1).pptx  # Architecture & Executive Presentation
├── final_dataset.xlsx                                         # Curated multi-industry telemetry benchmark
├── project_risk_dataset.csv                                   # 50,000-row historical training dataset
├── current/
│   ├── it/                                                    # Sample IT project documents
│   │   ├── Altura_Freight_Project.pdf
│   │   └── Northstar_Clinical_Systems_Project.pdf
│   ├── non-it/                                                # Sample Non-IT project documents
│   │   ├── Greenfield_Fresh_Produce_Project.pdf
│   │   └── Redwood_Mining_Copper_Expansion_Project.pdf
│   └── AI_project/
│       ├── AI_Project_Risk_Forecasting_System_Combined_KnowledgeBase.pdf
│       └── final_project/                                     # 🌟 Primary Application Codebase
│           ├── app.py                                         # Streamlit UI Entrypoint
│           ├── landing.py                                     # Landing Page UI
│           ├── users.json                                     # Default accounts database
│           ├── database_client.py                             # Database connector
│           ├── validators.py                                  # Input data validation schemas
│           ├── requirements.txt                               # All dependencies
│           ├── setup_windows.bat                              # 1-click Windows environment setup
│           ├── start_all.bat                                  # 1-click Start (Backend + Frontend)
│           ├── start_backend.bat                              # Start FastAPI backend only
│           ├── start_streamlit.bat                            # Start Streamlit frontend only
│           ├── backend/                                       # FastAPI API Service
│           │   ├── app/
│           │   │   ├── api/                                   # REST Endpoint Routers
│           │   │   ├── core/                                  # Config, DB, Security
│           │   │   ├── ml/                                    # Training and Inference scripts
│           │   │   ├── models/                                # SQLAlchemy ORM Models
│           │   │   ├── schemas/                               # Pydantic Schemas
│           │   │   └── services/                              # Business Logic Engines
│           │   ├── scripts/                                   # Database seeders & data generators
│           │   └── project_risk.db                            # SQLite Local Database
│           ├── ml_models/                                     # Serialized ML Models & Metadata
│           │   ├── it_models/                                 # XGBoost IT model & metadata
│           │   └── non_it_models/                             # Stacking XGBoost Non-IT model
│           ├── rag_chatbot/                                   # RAG Engine & Qdrant Integration
│           │   ├── chatbot.py
│           │   ├── chunking.py
│           │   ├── embeddings.py
│           │   ├── grounding.py
│           │   └── session_store.py
│           ├── pages/                                         # Streamlit Multi-Page Views (1–20)
│           └── utils/                                         # Shared client & UI utilities
└── sample/                                                    # Sample test projects (Alpha to Zeta)
    ├── Sample_Project_Alpha.pdf
    ├── Sample_Project_Beta.pdf
    ├── Sample_Project_Delta.pdf
    ├── Sample_Project_Epsilon.pdf
    ├── Sample_Project_Gamma.pdf
    ├── Sample_Project_Zeta.pdf
    └── sample_users.csv
```

---

## 🚀 Installation & Getting Started

### Prerequisites
- Windows, macOS, or Linux
- Python 3.11 or higher (Anaconda / Miniconda recommended)

---

### Option A: One-Click Startup (Windows)

Navigate to `current/AI_project/final_project/` and run:

1. **First-time setup:**
   ```bat
   setup_windows.bat
   ```
2. **Launch full platform (Backend + Frontend):**
   ```bat
   start_all.bat
   ```

---

### Option B: Manual Step-by-Step Setup

#### 1. Clone & Navigate to Project
```bash
cd current/AI_project/final_project
```

#### 2. Create and Activate Virtual Environment
Using Conda:
```bash
conda create -n project_ai python=3.11 -y
conda activate project_ai
```
Or using standard Python `venv`:
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate
```

#### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Launch FastAPI Backend Service
In Terminal 1:
```bash
cd backend
set PYTHONPATH=.    # On Linux/macOS: export PYTHONPATH=.
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
- **Backend API URL**: `http://127.0.0.1:8000`
- **Interactive OpenAPI Documentation**: `http://127.0.0.1:8000/docs`

#### 5. Launch Streamlit Frontend Application
In Terminal 2 (with environment activated):
```bash
cd current/AI_project/final_project
streamlit run app.py
```
- **Streamlit Web Application**: `http://localhost:8501`

---

## 👥 Demo Credentials & Sample Projects

### Pre-Configured Users (`users.json`)

| Username | Password | Role / Workspace Domain | Description |
| :--- | :--- | :--- | :--- |
| `it_user` | `it123` | **IT** | Technical engineering, software & cloud systems |
| `nonit_user` | `nonit123` | **Non-IT** | Business operations, logistics, mining, agriculture |
| `Dk` | `1234` | **IT** | Senior IT engineering access |

*You can also create new accounts with custom job roles directly on the login screen.*

### Sample Test Projects Available
- **IT Domain**: `current/it/Altura_Freight_Project.pdf`, `current/it/Northstar_Clinical_Systems_Project.pdf`
- **Non-IT Domain**: `current/non-it/Greenfield_Fresh_Produce_Project.pdf`, `current/non-it/Redwood_Mining_Copper_Expansion_Project.pdf`
- **Benchmark Suite**: `sample/Sample_Project_Alpha.pdf` through `Sample_Project_Zeta.pdf`

---

## 🔑 Environment Configuration

Create a `.env` file in `current/AI_project/final_project/` (or copy from `backend/.env.example`):

```ini
# Google Generative AI (Required for RAGbot & LLM extraction)
GOOGLE_API_KEY=your_google_api_key_here

# Backend API Configuration
API_BASE_URL=http://127.0.0.1:8000
ENVIRONMENT=development
DATABASE_URL=sqlite:///./project_risk.db

# Qdrant Vector Search (Defaults to in-memory / local SQLite if not hosted)
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

---

## 🔄 Model Training & Database Seeding

To retrain the ML models on the 50,000-row telemetry dataset or re-seed the SQLite database:

```bash
cd current/AI_project/final_project/backend
set PYTHONPATH=.

# 1. Regenerate synthetic training data (optional)
python scripts/generate_training_data.py

# 2. Retrain ML models
python -m app.ml.train

# 3. Seed demo projects into the database
python scripts/seed.py
```

---

## 📊 Summary Table of Machine Learning Models

| Model Name | Target Workspace | Algorithm | Features | Accuracy | Precision | Recall | ROC-AUC |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **IT Risk Predictor** | IT & Technical Engineering | XGBoost Classifier | 24 core telemetry metrics | **93.49%** | **92.28%** | **89.80%** | **0.9859** |
| **Non-IT Risk Ensemble** | Non-IT & Business Operations | Tuned XGBoost + Stacking | 39 engineered domain features | **95.96%** | **94.62%** | **94.40%** | **0.9939** |

---

## 🛡️ License & Acknowledgements

- **License**: MIT License
- Developed as an enterprise risk intelligence and project analytics platform.
