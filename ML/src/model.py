import joblib
import lightgbm as lgb

def load_model(path):
    return joblib.load(path)

def predict(model, X):
    proba = model.predict_proba(X)[0]
    pred_class_idx = proba.argmax()
    CLASS_NAMES = ["stay","voluntaryChurn","involuntaryChurn"]
    return proba, CLASS_NAMES[pred_class_idx]