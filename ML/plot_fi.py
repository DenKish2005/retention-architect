from catboost import CatBoostClassifier
import matplotlib.pyplot as plt

model = CatBoostClassifier()
model.load_model("models/catboost_model.cbm")

fi = model.get_feature_importance()
fn = model.feature_names_

plt.figure(figsize=(10,6))
plt.barh(fn, fi, color='#e63946')
plt.title("Feature Importance — Churn Drivers")
plt.tight_layout()
plt.savefig("feature_importance.png", dpi=150)
print("Saved!")