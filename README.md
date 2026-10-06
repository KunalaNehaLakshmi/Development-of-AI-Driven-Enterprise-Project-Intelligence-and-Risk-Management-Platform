# AI-Driven Enterprise Project Intelligence & Risk Management Platform

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-1.8%2B-EB5424?style=for-the-badge&logo=xgboost&logoColor=white)
![CatBoost](https://img.shields.io/badge/CatBoost-Ensemble-FDB813?style=for-the-badge&logoColor=black)
![Google GenAI](https://img.shields.io/badge/Generative_AI-Google_GenAI-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![Qdrant](https://img.shields.io/badge/Vector_DB-Qdrant-DC2626?style=for-the-badge&logoColor=white)

An integrated, end-to-end **AI-powered Enterprise Project Intelligence and Risk Management Platform** that combines Machine Learning, Generative AI, Retrieval-Augmented Generation (RAG), graph-based dependency analysis, schedule forecasting, and what-if simulation into a unified project intelligence system.

The platform is designed to support both **IT / Technical Engineering** and **Non-IT / Business Operations** projects by helping teams identify risks early, understand project health, forecast delays, analyze dependencies, simulate potential scenarios, and obtain AI-assisted recommendations.

---

# Live Demo

## Deployed Application

The project is deployed and accessible online:

**Live Application:**
https://ai-project-frontend-a3hp.onrender.com/

The deployed application provides access to the project's interactive Streamlit interface and project intelligence workflows.

> Note: The application may take some time to respond if the hosting service has temporarily put the instance to sleep.

---

# Overview

Enterprise projects generate large amounts of structured and unstructured information such as:

- Project metrics
- Budgets and schedules
- Resource information
- Risk indicators
- Project documentation
- Meeting notes
- Dependencies
- Milestones
- Requirements
- Technical and business constraints

Traditional project management systems often focus on monitoring and reporting. This project extends that approach by introducing predictive and generative AI capabilities.

The platform combines:

**Project Data + Machine Learning + Document Intelligence + RAG + Graph Analytics + Simulation**

into a single project intelligence platform.

---

# Key Features

## 1. Role-Based Project Intelligence

The platform supports dedicated workflows for:

### IT / Technical Engineering Projects

Designed for projects involving:

- Software development
- Technology systems
- Engineering
- Infrastructure
- Technical dependencies
- Complex technical risks

### Non-IT / Business Operations Projects

Designed for:

- Business operations
- Manufacturing
- Supply chain
- Agriculture
- Mining
- Other operational projects

---

## 2. AI Risk Prediction

Machine Learning models analyze project characteristics and historical project data to predict project risk.

The platform supports separate predictive pipelines for:

- IT projects
- Non-IT projects

The prediction system provides:

- Risk classification
- Project health indicators
- Risk probability
- Risk-related metrics
- Risk analysis
- Actionable recommendations

### Machine Learning Models

The platform uses:

- XGBoost
- CatBoost
- Scikit-learn
- Pandas
- NumPy

---

## 3. Schedule Intelligence

The Schedule Intelligence module analyzes project timelines and helps identify potential delays.

Capabilities include:

- Deadline forecasting
- Milestone tracking
- Delay analysis
- Schedule overrun analysis
- Project progress analysis
- Delay impact assessment

---

## 4. Dependency Intelligence

Project dependencies are analyzed using graph-based techniques.

The platform uses **NetworkX** to model project dependencies and identify:

- Critical dependencies
- Bottlenecks
- Dependency chains
- High-impact tasks
- Potential project blockers

---

## 5. What-If Simulation

The What-If Simulation module allows users to safely experiment with project scenarios without modifying the original project data.

Example scenarios include:

- Budget reduction
- Resource reduction
- Increased project duration
- Increased workload
- Dependency changes
- Schedule changes

The system evaluates the potential effect of the scenario on project risk and health.

---

## 6. RAG-Powered AI Assistant

The platform includes an intelligent RAG chatbot capable of answering questions using uploaded project documents.

Supported document types include:

- PDF
- DOCX

The RAG pipeline includes:

1. Document ingestion
2. Text extraction
3. Text chunking
4. Embedding generation
5. Vector storage
6. Semantic retrieval
7. Generative AI response generation

### RAG Technology

- Google GenAI
- Qdrant
- Embedding models
- PyPDF
- docx2txt

The assistant can answer project-specific questions based on the documents supplied to it.

---

## 7. Document Intelligence

Project documents can be uploaded and analyzed to extract useful project intelligence.

The system is designed to identify information such as:

- Project risks
- Milestones
- Dependencies
- Requirements
- Project constraints
- Important project information

---

## 8. Interactive Streamlit Dashboard

The frontend is implemented using **Streamlit**.

The application provides a multi-page interface containing modules for:

- Dashboard
- Document Upload
- Project Analysis
- Risk Intelligence
- Schedule Intelligence
- Dependency Analysis
- What-If Simulation
- Recommendations
- Documentation
- AI Assistant

---

# System Architecture

```text
                         ┌─────────────────────────┐
                         │       User / Client      │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │       Streamlit UI       │
                         │  Dashboard + Workflows   │
                         └────────────┬────────────┘
                                      │
                         HTTP / REST API Requests
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │       FastAPI API        │
                         │     Backend Services     │
                         └────────────┬────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              │                       │                       │
              ▼                       ▼                       ▼
     ┌────────────────┐     ┌─────────────────┐     ┌─────────────────┐
     │ ML Prediction  │     │ Project         │     │ RAG / GenAI     │
     │ Engine         │     │ Intelligence    │     │ Engine          │
     └───────┬────────┘     └────────┬────────┘     └────────┬────────┘
             │                       │                       │
             ▼                       ▼                       ▼
     ┌────────────────┐     ┌─────────────────┐     ┌─────────────────┐
     │ XGBoost        │     │ NetworkX        │     │ Qdrant          │
     │ CatBoost       │     │ Dependency      │     │ Vector Database │
     │ ML Pipelines   │     │ Analysis        │     │ + Google GenAI  │
     └────────────────┘     └─────────────────┘     └─────────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Project Data / Database │
                         └─────────────────────────┘
```

---

# Technology Stack

## Frontend

- Streamlit
- Python
- Requests

## Backend

- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- Uvicorn

## Database

- SQLite for local development
- PostgreSQL supported

## Machine Learning

- Scikit-learn
- XGBoost
- CatBoost
- Pandas
- NumPy

## Graph Analytics

- NetworkX

## Generative AI / RAG

- Google GenAI
- Qdrant
- PyPDF
- docx2txt
- Embedding models

## Deployment / Infrastructure

- Docker
- Docker Compose
- Uvicorn
- Windows batch scripts

---

# Repository Structure

```text
FINAL/
│
├── README.md
│
├── AI_Project_Intelligence_Risk_Management_Platform.pptx
├── final_dataset.xlsx
├── project_risk_dataset.csv
│
├── current/
│   │
│   ├── it/
│   │   ├── Altura_Freight_Project.pdf
│   │   └── Northstar_Clinical_Systems_Project.pdf
│   │
│   ├── non-it/
│   │   ├── Greenfield_Fresh_Produce_Project.pdf
│   │   └── Redwood_Mining_Copper_Expansion_Project.pdf
│   │
│   └── AI_project/
│       │
│       ├── .vscode/
│       │   └── settings.json
│       │
│       └── final_project/
│           │
│           ├── .streamlit/
│           ├── backend/
│           ├── data/
│           ├── documents/
│           ├── ml_models/
│           ├── pages/
│           ├── rag_chatbot/
│           ├── utils/
│           │
│           ├── app.py
│           ├── landing.py
│           ├── database_client.py
│           ├── validators.py
│           ├── users.json
│           ├── requirements.txt
│           ├── README.md
│           │
│           ├── setup_windows.bat
│           ├── start_all.bat
│           ├── start_backend.bat
│           └── start_streamlit.bat
│
└── sample/
    │
    ├── Sample_Project_Alpha.pdf
    ├── Sample_Project_Beta.pdf
    ├── Sample_Project_Delta.pdf
    ├── Sample_Project_Epsilon.pdf
    ├── Sample_Project_Gamma.pdf
    ├── Sample_Project_Zeta.pdf
    └── sample_users.csv
```

---

# Backend Structure

```text
backend/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── app/
│   ├── api/
│   ├── core/
│   ├── ml/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── __init__.py
│   └── main.py
│
├── data/
├── ml_models/
├── scripts/
├── tests/
│
├── .env.example
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Machine Learning Models

The project maintains separate models for IT and Non-IT project risk prediction.

```text
ml_models/
│
├── it_models/
│   ├── catboost_project_risk_model.cbm
│   └── xgb_project_risk_model.json
│
└── non_it_models/
    ├── model_metadata.json
    └── risk_model.joblib
```

---

# RAG Chatbot Architecture

```text
Project Documents
       │
       ▼
Document Parser
       │
       ▼
Text Extraction
       │
       ▼
Chunking
       │
       ▼
Embeddings
       │
       ▼
Qdrant Vector Database
       │
       ▼
Semantic Retrieval
       │
       ▼
Google GenAI
       │
       ▼
Project Intelligence Response
```

---

# Sample Project Demonstration

The repository contains sample project documents for demonstrating the document intelligence and RAG capabilities.

```text
sample/
│
├── Sample_Project_Alpha.pdf
├── Sample_Project_Beta.pdf
├── Sample_Project_Delta.pdf
├── Sample_Project_Epsilon.pdf
├── Sample_Project_Gamma.pdf
├── Sample_Project_Zeta.pdf
└── sample_users.csv
```

Additional example IT and Non-IT project documents are provided under:

```text
current/it/
current/non-it/
```

These files can be used to test:

- Document upload
- Project analysis
- Risk analysis
- RAG question answering
- Dependency intelligence
- Recommendations

---

# Quick Start

## Requirements

Recommended environment:

- Python 3.11+
- Windows / Linux / macOS
- Git
- Internet connection for Generative AI functionality

---

# Windows Setup

## 1. Clone the Repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd <REPOSITORY-FOLDER>
```

---

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```bash
pip install -r current/AI_project/final_project/requirements.txt
```

---

# Run the Application

Navigate to:

```bash
cd current/AI_project/final_project
```

## Option 1 — One-Click Startup

Windows users can run:

```text
start_all.bat
```

This starts the backend and Streamlit frontend.

---

## Option 2 — Start Backend Manually

Open Terminal 1:

```powershell
cd current/AI_project/final_project/backend
$env:PYTHONPATH="."
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Start Streamlit Frontend

Open Terminal 2:

```powershell
cd current/AI_project/final_project
streamlit run app.py
```

Frontend:

```text
http://localhost:8501
```

---

# Environment Configuration

Create a `.env` file locally.

Do not commit real API keys or secrets to GitHub.

Example:

```env
GOOGLE_API_KEY=your_google_api_key_here

DATABASE_URL=sqlite:///./project_risk.db

MODEL_PATH=ml_models/non_it_models/risk_model.joblib
METADATA_PATH=ml_models/non_it_models/model_metadata.json
```

For PostgreSQL deployments, the database URL can be configured accordingly.

Example:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/project_risk_db
```

---

# Backend Environment Configuration

The backend provides an example environment file:

```text
backend/.env.example
```

Example configuration:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/project_risk_db

MODEL_PATH=ml_models/risk_model.joblib
METADATA_PATH=ml_models/model_metadata.json

ENVIRONMENT=development
PORT=8000
HOST=0.0.0.0
CORS_ORIGINS=
```

Actual secrets and local configuration should remain in `.env` and must not be committed.

---

# API Documentation

Once the FastAPI backend is running, interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

The API provides backend services for:

- Project management
- Risk prediction
- Project health
- Schedule intelligence
- Deadline forecasting
- Dependency analysis
- Scenario simulation
- Recommendations
- Document processing
- RAG functionality

---

# Machine Learning Workflow

```text
Historical Project Data
          │
          ▼
Data Preprocessing
          │
          ▼
Feature Engineering
          │
          ▼
Train / Validation Split
          │
          ▼
Model Training
          │
     ┌────┴────┐
     ▼         ▼
 XGBoost    CatBoost
     │         │
     └────┬────┘
          ▼
 Model Evaluation
          │
          ▼
 Model Artifact
          │
          ▼
 FastAPI Prediction Service
          │
          ▼
 Streamlit Risk Dashboard
```

---

# Model Performance

The current project models achieved the following benchmark results during evaluation.

## IT Risk Model

**XGBoost — 24-feature pipeline**

- Accuracy: **93.49%**
- ROC-AUC: **0.9859**
- Precision: **0.9228**
- Recall: **0.8980**

## Non-IT Risk Model

**39-feature tuned ensemble**

- Accuracy: **95.96%**
- ROC-AUC: **0.9939**
- Precision: **0.9462**
- Recall: **0.9440**

These results are dataset-specific evaluation metrics and should not be interpreted as guarantees of real-world prediction performance.

---

# Project Workflow

```text
User Login
    │
    ▼
Role Selection
    │
    ├───────────────┐
    ▼               ▼
 IT Workspace    Non-IT Workspace
    │               │
    └───────┬───────┘
            ▼
      Project Dashboard
            │
     ┌──────┼────────┐
     │      │        │
     ▼      ▼        ▼
   Risk   Schedule  Dependency
 Analysis Intelligence Analysis
     │      │        │
     └──────┼────────┘
            ▼
      What-If Simulation
            │
            ▼
      Recommendations
            │
            ▼
      RAG AI Assistant
```

---

# Main Application Modules

| Module | Purpose |
|---|---|
| Dashboard | Project overview and key project health indicators |
| Document Upload | Upload and process project documents |
| Project Analysis | Analyze project-level information |
| Risk Intelligence | Predict and analyze project risk |
| Schedule Intelligence | Forecast deadlines and identify delays |
| Dependencies | Analyze project dependency relationships |
| What-If Simulation | Test hypothetical project scenarios |
| Recommendations | Generate risk mitigation recommendations |
| Documentation | Access project and system documentation |
| AI Assistant | Ask questions about project documents using RAG |

---

# Security Considerations

The application is designed with separation between application code and sensitive configuration.

The following files should not be committed:

```text
.env
.venv/
venv/
__pycache__/
*.pyc
users.json
local databases
secret keys
API credentials
```

Production deployments should additionally implement:

- Secure authentication
- Password hashing
- Secret management
- HTTPS
- Database access controls
- Proper CORS configuration
- Production-grade logging
- Rate limiting
- Secure API key management

---

# Docker Support

The backend includes:

```text
Dockerfile
docker-compose.yml
```

Docker can be used to provide a reproducible backend environment.

Example:

```bash
docker compose up --build
```

The exact services and environment variables are defined in:

```text
current/AI_project/final_project/backend/docker-compose.yml
```

---

# Project Demonstration Resources

The repository contains resources for demonstrating the complete platform.

## Project Datasets

```text
final_dataset.xlsx
project_risk_dataset.csv
```

## IT Project Documents

```text
current/it/
```

## Non-IT Project Documents

```text
current/non-it/
```

## RAG / Demonstration Documents

```text
sample/
```

These resources allow the application to be demonstrated using predefined project datasets and documents.

---

# Project Presentation

The project presentation is included in the repository:

```text
AI_Project_Intelligence_Risk_Management_Platform.pptx
```

The presentation contains the project's:

- Problem statement
- Proposed solution
- System architecture
- Machine Learning approach
- Generative AI / RAG architecture
- Application workflow
- Results
- Future scope

---

# Future Improvements

Potential future enhancements include:

- Real-time project monitoring
- Advanced time-series forecasting
- Automated project status ingestion
- Enterprise SSO integration
- Cloud deployment
- Kubernetes orchestration
- Advanced model explainability
- SHAP-based feature explanations
- Automated project report generation
- Multi-project portfolio risk analysis
- Real-time notifications
- Advanced agentic project management workflows

---

# Disclaimer

This project is an academic / research-oriented enterprise project intelligence platform.

Machine Learning predictions are dependent on the quality, distribution, and representativeness of the training data. Predictions should be used as decision-support information and should not replace professional project management judgment.

---

# Documentation

Additional application-level technical documentation is available inside:

```text
current/AI_project/final_project/README.md
```

Backend-specific documentation is available inside:

```text
current/AI_project/final_project/backend/README.md
```

---

# Author

**Kunala Neha Lakshmi**

B.Tech — Artificial Intelligence & Data Science
Amrita Vishwa Vidyapeetham

---

# License

This project is intended for academic, educational, and research purposes.
