from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, sys

# Чтобы работало и из папки ML/ и из корня
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.features import build_features
from src.model import load_model, predict
from src.explainer import get_top_drivers, get_explanations, get_recommended_actions

app = FastAPI(title="Retention Architect ML Service")

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "catboost_model.cbm")
model = load_model(MODEL_PATH)

# ── Schemas ────────────────────────────────────────────────────────────────────

class PredictUserRequest(BaseModel):
    userId: str

class PredictBatchRequest(BaseModel):
    userIds: list[str]

# ── Health ─────────────────────────────────────────────────────────────────────

@app.get("/api/Prediction/health")
def health():
    return {"status": "OK"}

@app.get("/api/Prediction/health/ml")
def health_ml():
    return {"status": "ML OK", "model": MODEL_PATH}

# ── Core predict logic ─────────────────────────────────────────────────────────

def _predict_one(user_id: str) -> dict:
    try:
        X = build_features(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feature building failed for {user_id}: {e}")

    proba, pred_class = predict(model, X)
    drivers      = get_top_drivers(model, X)
    explanations = get_explanations(model, X, pred_class)
    actions      = get_recommended_actions(pred_class)

    return {
        "userId":            user_id,
        "churnProbability":  round(float(max(proba)), 4),
        "predictedClass":    pred_class,
        "classProbabilities": {
            "stay":             round(float(proba[0]), 4),
            "voluntaryChurn":   round(float(proba[1]), 4),
            "involuntaryChurn": round(float(proba[2]), 4),
        },
        "topDrivers":        drivers,
        "explanations":      explanations,
        "recommendedActions": actions,
    }

# ── Endpoints ──────────────────────────────────────────────────────────────────

@app.post("/api/Prediction/user")
def predict_user(req: PredictUserRequest):
    return _predict_one(req.userId)

@app.post("/api/Prediction/batch")
def predict_batch(req: PredictBatchRequest):
    return [_predict_one(uid) for uid in req.userIds]