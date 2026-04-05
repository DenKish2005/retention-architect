import numpy as np
import shap

# Правила для читаемых описаний — не зависят от LLM
FEATURE_RULES = {
    "failed_attempts":   ("payment_failures",  "increase", "Несколько неудачных попыток оплаты повышают риск оттока."),
    "fail_rate":         ("payment_fail_rate",  "increase", "Высокая доля отказов платежей — признак involuntary churn."),
    "total_generations": ("low_usage",          "decrease", "Мало генераций указывает на низкую вовлечённость."),
    "active_days":       ("inactivity",         "decrease", "Мало активных дней — пользователь не вовлечён."),
    "total_purchases":   ("purchase_history",   "decrease", "Нет покупок — пользователь не видит ценности."),
    "total_spent":       ("spend_level",        "decrease", "Низкие траты коррелируют с риском отписки."),
    "failed_generations":("failed_content",     "increase", "Много ошибок при генерации снижает удовлетворённость."),
}

ACTIONS = {
    "voluntaryChurn": [
        "Offer a 20% discount on next billing cycle",
        "Send personalized content recommendations",
        "Trigger re-engagement email with usage tips",
    ],
    "involuntaryChurn": [
        "Prompt user to update payment method",
        "Schedule automatic payment retry after 24 hours",
        "Send payment failure notification with recovery link",
    ],
    "stay": [
        "Continue standard engagement flow",
        "Consider upsell opportunity",
    ],
}

def get_top_drivers(model, X, top_n=3) -> list[str]:
    """Возвращает список строк — топ факторов риска."""
    try:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X)

        pred_class_idx = int(model.predict(X)[0])

        # shap_values может быть list[array] или 3d array
        if isinstance(shap_values, list):
            sv = np.array(shap_values[pred_class_idx][0], dtype=float)
        else:
            sv = np.array(shap_values[0, :, pred_class_idx], dtype=float)

        feature_names = X.columns.tolist()
        top_idx = np.argsort(np.abs(sv))[-top_n:][::-1]

        drivers = []
        for i in top_idx:
            fname = feature_names[int(i)]
            fval  = X.iloc[0, int(i)]
            drivers.append(f"{fname} = {fval}")
        return drivers

    except Exception as e:
        # Fallback — не ломаем API из-за SHAP
        return [f"{col} = {X.iloc[0][col]}" for col in X.columns[:top_n]]


def get_explanations(model, X, pred_class: str) -> list[dict]:
    """Возвращает массив explanation объектов по контракту с C#."""
    try:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X)

        pred_class_idx = int(model.predict(X)[0])

        if isinstance(shap_values, list):
            sv = np.array(shap_values[pred_class_idx][0], dtype=float)
        else:
            sv = np.array(shap_values[0, :, pred_class_idx], dtype=float)

        feature_names = X.columns.tolist()
        top_idx = np.argsort(np.abs(sv))[-3:][::-1]

        explanations = []
        for i in top_idx:
            fname = feature_names[int(i)]
            impact_val = float(sv[int(i)])
            direction = "increase" if impact_val > 0 else "decrease"

            if fname in FEATURE_RULES:
                feat_key, _, description = FEATURE_RULES[fname]
            else:
                feat_key = fname
                description = f"Feature '{fname}' influenced the prediction."

            explanations.append({
                "feature":     feat_key,
                "impact":      round(abs(impact_val), 4),
                "direction":   direction,
                "description": description,
            })

        return explanations

    except Exception as e:
        return []


def get_recommended_actions(pred_class: str) -> list[str]:
    return ACTIONS.get(pred_class, ACTIONS["stay"])
