import numpy as np
from catboost import CatBoostClassifier

CLASS_NAMES = ["stay", "voluntaryChurn", "involuntaryChurn"]

def load_model(path: str = "models/catboost_model.cbm"):
    model = CatBoostClassifier()
    model.load_model(path)
    return model

def predict(model, X):
    proba = model.predict_proba(X)[0]
    class_idx = int(proba.argmax())
    return proba, CLASS_NAMES[class_idx]
