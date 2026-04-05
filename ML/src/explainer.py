import shap
import numpy as np


def get_top_drivers(model, X, top_n=3):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    pred_class_idx = model.predict(X)[0]
    sv = shap_values[pred_class_idx]  # (n_samples, n_features)

    sv_row = np.ravel(sv[0]).astype(float)  # flatten first sample

    feature_names = X.columns.tolist()
    n_features = len(feature_names)

    # Clip top indices to valid range
    top_idx = np.argsort(np.abs(sv_row))[-top_n:][::-1]
    top_idx = [min(int(i), n_features-1) for i in top_idx]

    drivers = []
    for i_int in top_idx:
        drivers.append(f"{feature_names[i_int]} = {X.iloc[0, i_int]}")
    return drivers

def get_explanations(model, X):
    top_features = get_top_drivers(model, X)
    explanations = []
    
    for feat in top_features:
        if "fail" in feat.lower() or "attempts" in feat.lower():
            explanations.append({
                "feature": "payment_failures",
                "impact": 0.3,
                "direction": "increase",
                "description": "Причина: Отказ платежа. Рекомендация: Повтор через 3 дня или скидка на другой метод оплаты"
            })
    return explanations