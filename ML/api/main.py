from fastapi import FastAPI
from pydantic import BaseModel
from src.features import build_features
from src.model import load_model, predict
from src.explainer import get_top_drivers, get_explanations

app = FastAPI()
model = load_model()

class PredictRequest(BaseModel):
    userId: str

class PredictBatchRequest(BaseModel):
    userIds: list[str]

@app.get("/api/Prediction/health")
def health():
    return {"status": "OK"}

@app.get("/api/Prediction/health/ml")
def health_ml():
    return {"status": "ML OK"}

@app.post("/api/Prediction/user")
def predict_user(req: PredictRequest):
    X = build_features(req.userId)
    proba, pred_class = predict(model, X)
    drivers = get_top_drivers(model, X)
    explanations = get_explanations(model, X)
    actions = [exp["description"] for exp in explanations]
    return {
        "userId": req.userId,
        "churnProbability": float(max(proba)),
        "predictedClass": pred_class,
        "classProbabilities": dict(zip(["stay","voluntaryChurn","involuntaryChurn"], proba)),
        "topDrivers": drivers,
        "explanations": explanations,
        "recommendedActions": actions
    }

@app.post("/api/Prediction/batch")
def predict_batch(req: PredictBatchRequest):
    results = []
    for uid in req.userIds:
        X = build_features(uid)
        proba, pred_class = predict(model, X)
        drivers = get_top_drivers(model, X)
        explanations = get_explanations(model, X)
        actions = [exp["description"] for exp in explanations]
        results.append({
            "userId": uid,
            "churnProbability": float(max(proba)),
            "predictedClass": pred_class,
            "classProbabilities": dict(zip(["stay","voluntaryChurn","involuntaryChurn"], proba)),
            "topDrivers": drivers,
            "explanations": explanations,
            "recommendedActions": actions
        })
    return results