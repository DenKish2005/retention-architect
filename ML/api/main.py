from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from src.features import build_features
from src.model import load_model, predict
from src.explainer import get_top_drivers

app = FastAPI()
model = load_model("models/lgbm_model.pkl")

class PredictRequest(BaseModel):
    user_id: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict_user")
def predict_user(req: PredictRequest):
    feats = build_features(req.user_id)
    proba, pred_class = predict(model, feats)
    drivers = get_top_drivers(model, feats)
    actions = get_recommendations(pred_class, drivers)
    return {
        "userId": req.user_id,
        "churnProbability": float(max(proba)),
        "predictedClass": pred_class,
        "classProbabilities": dict(zip(["stay","voluntaryChurn","involuntaryChurn"], proba)),
        "topDrivers": drivers,
        "recommendedActions": actions
    }

def get_recommendations(pred_class, drivers):
    # Rule-based mapping
    if pred_class == "voluntaryChurn":
        return ["Notify user", "Offer content/promo", "Send personalized tip"]
    elif pred_class == "involuntaryChurn":
        return ["Retry payment", "Update payment method", "Fallback route"]
    else:
        return []