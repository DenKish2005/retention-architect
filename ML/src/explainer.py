import shap

def get_top_drivers(model, X, top_n=3):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    pred_class_idx = model.predict(X)[0]
    sv = shap_values[pred_class_idx][0]
    feature_names = X.columns.tolist()
    top_idx = abs(sv).argsort()[-top_n:][::-1]
    return [f"{feature_names[i]} = {X.iloc[0][feature_names[i]]}" for i in top_idx]