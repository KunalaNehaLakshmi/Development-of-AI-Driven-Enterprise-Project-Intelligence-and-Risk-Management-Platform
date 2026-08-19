import os
import json
import joblib
import pandas as pd
import numpy as np

# IT model setup
import xgboost as xgb

IT_MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml_models", "it_models", "xgb_project_risk_model.json")
NON_IT_MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml_models", "non_it_models", "risk_model.joblib")

# Caching models
_it_model = None
_non_it_model = None
_it_feature_names = []
_it_feature_types = []

def load_it_model():
    global _it_model, _it_feature_names, _it_feature_types
    if _it_model is None and os.path.exists(IT_MODEL_PATH):
        with open(IT_MODEL_PATH, "r") as f:
            d = json.load(f)
            _it_feature_names = d['learner']['feature_names']
            _it_feature_types = d['learner']['feature_types']
        _it_model = xgb.Booster()
        _it_model.load_model(IT_MODEL_PATH)
    return _it_model

def load_non_it_model():
    global _non_it_model
    if _non_it_model is None and os.path.exists(NON_IT_MODEL_PATH):
        _non_it_model = joblib.load(NON_IT_MODEL_PATH)
    return _non_it_model

def get_risk_level(score):
    if score < 30: return "Low"
    if score < 55: return "Medium"
    if score < 75: return "High"
    return "Critical"

def predict_it_risk(features_dict):
    """
    Predicts risk for IT projects using XGBoost regression model.
    """
    model = load_it_model()
    if not model:
        return {"risk_score": 50.0, "risk_level": "Medium"} # Fallback

    # Ensure all categorical features are treated as pandas Categorical
    df = pd.DataFrame([features_dict])
    
    # The first 6 features are categorical according to earlier discovery: 
    # 'project_type', 'industry_sector', 'methodology', 'region', 'contract_type', 'priority'
    cat_cols = [c for c, t in zip(_it_feature_names, _it_feature_types) if t == "c"]
    
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype("category")

    # Order columns
    missing_cols = [c for c in _it_feature_names if c not in df.columns]
    for col in missing_cols:
        if col in cat_cols:
            df[col] = pd.Series(["Unknown"], dtype="category")
        else:
            df[col] = 0.0

    df = df[_it_feature_names]
    
    dmat = xgb.DMatrix(df, enable_categorical=True)
    pred = model.predict(dmat)[0]
    
    # Cap score
    score = float(max(0, min(100, pred)))
    
    return {
        "risk_score": round(score, 1),
        "risk_level": get_risk_level(score)
    }

def predict_non_it_risk(features_dict):
    """
    Predicts risk for Non-IT projects using the Logistic Regression pipeline.
    """
    model = load_non_it_model()
    if not model:
        return {"risk_score": 50.0, "risk_level": "Medium"}
        
    df = pd.DataFrame([features_dict])
    
    # Ensure all required features are present
    required_features = [
        "progress_percentage", "pending_task_ratio", "delay_days", "budget_utilization",
        "resource_availability", "bugs_per_task", "testing_progress", "testing_failure_rate",
        "requirement_change_rate", "team_productivity", "dependency_delay", "critical_dependency_count",
        "security_audit_progress", "external_risk_score", "schedule_variance", "resource_pressure",
        "dependency_risk_score"
    ]
    
    for col in required_features:
        if col not in df.columns:
            df[col] = 0.0
            
    df = df[required_features]
    
    try:
        # LogisticRegression pipeline predicts 0 or 1, and proba
        proba = model.predict_proba(df)[0][1] # Probability of high risk
        score = float(proba * 100)
    except Exception as e:
        score = 50.0

    return {
        "risk_score": round(score, 1),
        "risk_level": get_risk_level(score)
    }
