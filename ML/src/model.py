# from catboost import CatBoostClassifier

# MODEL_PATH = "models/catboost_model.cbm"

# def load_model():
#     model = CatBoostClassifier()
#     model.load_model(MODEL_PATH)
#     return model

# def predict(model, X):
#     proba = model.predict_proba(X)[0]
#     class_idx = proba.argmax()
#     CLASS_NAMES = ["stay", "voluntaryChurn", "involuntaryChurn"]
#     return proba, CLASS_NAMES[class_idx]

# src/model.py
import numpy as np

def load_model():
    class DummyModel:
        def predict_proba(self, X):
            return np.array([[0.5, 0.3, 0.2]] * len(X))
        def predict(self, X):
            return np.array([0] * len(X))
    return DummyModel()

def predict(model, X):
    proba = model.predict_proba(X)[0]
    class_idx = proba.argmax()
    CLASS_NAMES = ["stay", "voluntaryChurn", "involuntaryChurn"]
    return proba, CLASS_NAMES[class_idx]