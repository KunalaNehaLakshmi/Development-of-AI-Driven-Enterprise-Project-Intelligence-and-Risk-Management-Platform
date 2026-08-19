# AI-Driven Enterprise Project Intelligence & Risk Management Platform

An end-to-end AI-powered platform for **project risk prediction, project intelligence, schedule forecasting, dependency analysis, what-if simulation, document intelligence, and RAG-based assistance**.

The platform combines Machine Learning, Generative AI, Retrieval-Augmented Generation (RAG), and project analytics to help project managers and stakeholders identify risks early and make data-driven decisions.

---

## Overview

Enterprise projects can face risks due to changing requirements, budget overruns, schedule delays, resource constraints, dependencies, technical complexity, and other operational factors.

This platform provides a centralized intelligence layer that can:

- Predict project risk levels
- Analyze project health
- Forecast schedule and deadlines
- Identify critical dependencies
- Perform what-if simulations
- Analyze uploaded project documents
- Generate AI-powered recommendations
- Explain individual risk predictions
- Provide a RAG-powered project intelligence assistant

The application supports separate workflows for **IT and Non-IT projects**.

---

## Key Features

### 1. Role-Based Project Intelligence

Provides dedicated workflows for:

- IT users
- Non-IT users

Users can access project analysis and risk intelligence according to their role.

---

### 2. Machine Learning Risk Prediction

The platform uses machine learning models to predict project risk.

Implemented models include:

- XGBoost
- CatBoost

The system evaluates project-related features such as:

- Budget
- Project duration
- Team size
- Team experience
- Requirement changes
- Stakeholder count
- Resource availability
- Vendor dependencies
- Communication
- Sponsor engagement
- Technical complexity
- Scope clarity
- External dependencies
- Defects
- Milestones missed
- Cost overrun
- Schedule overrun

The prediction pipeline produces a project risk assessment that can be used for further project intelligence and recommendations.

---

### 3. Risk Intelligence

The platform provides risk-focused project analytics including:

- Risk score
- Risk category
- Project health indicators
- Risk factor analysis
- Project progress
- Pending tasks
- Client satisfaction indicators
- Risk-based insights

---

### 4. Individual Prediction Explainability

The system can explain individual project predictions using feature-level contribution analysis.

This helps answer:

> "Why was this project classified as high risk?"

Instead of only providing a prediction, the platform identifies important factors contributing to the prediction.

---

### 5. AI-Powered Recommendations

Based on the identified project risks, the platform generates actionable recommendations.

Examples include recommendations related to:

- Resource allocation
- Schedule management
- Requirement changes
- Budget control
- Dependency management
- Risk mitigation
- Stakeholder communication

---

### 6. Schedule Intelligence

The platform provides schedule-related project intelligence including:

- Deadline forecasting
- Milestone tracking
- Schedule-overrun analysis
- Delay impact analysis
- Project progress monitoring

---

### 7. Dependency Analysis

Project dependencies can create bottlenecks and delays.

The platform uses graph-based analysis with NetworkX to identify and visualize project dependencies and potential bottlenecks.

---

### 8. What-If Simulation

Project managers can test hypothetical scenarios without modifying the original project data.

Examples:

- What if the budget is reduced?
- What if resources become unavailable?
- What if requirements increase?
- What if the project duration changes?
- What if additional dependencies are introduced?

The system evaluates how these changes may affect project risk and health.

---

### 9. Document Intelligence

Project documents can be uploaded for automated analysis.

Supported document types include:

- PDF
- DOCX

The document processing pipeline extracts useful project information such as:

- Risks
- Milestones
- Dependencies
- Project information
- Relevant textual context

---

### 10. RAG-Powered AI Assistant

The platform includes a Retrieval-Augmented Generation (RAG) chatbot for project-specific question answering.

The RAG pipeline uses:

- Google Generative AI
- Vector embeddings
- Qdrant
- Document chunking
- Retrieval
- Context-aware response generation

Users can ask questions about uploaded project documents and receive answers based on the retrieved project context.

---

### 11. Interactive Streamlit Dashboard

The frontend is implemented using Streamlit.

The application contains dedicated pages for:

- Dashboard
- Document Upload
- Project Analysis
- Risk Intelligence
- Schedule Intelligence
- Dependencies
- What-If Simulation
- Recommendations
- Documentation
- AI Assistant

---

# System Architecture

The platform follows a modular architecture consisting of:

```text
                         ┌──────────────────────┐
                         │      Streamlit UI     │
                         │   Interactive Pages   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      API Backend      │
                         │       FastAPI         │
                         └──────────┬───────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
      ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
      │ ML Models   │       │  Project DB  │       │ RAG System  │
      │ XGBoost     │       │ SQLite /     │       │ Documents   │
      │ CatBoost    │       │ PostgreSQL   │       │ Embeddings  │
      └─────────────┘       └─────────────┘       │ Qdrant      │
                                                   │ Google GenAI│
                                                   └─────────────┘
