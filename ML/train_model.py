# python train_model.py

import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
from src.features import build_features

# Берём подвыборку 200 пользователей для теста
users = pd.read_csv("data/test_users.csv").head(200)

X_list, y_list = [], []
for uid in users['user_id']:
    X_list.append(build_features(uid))
    y_list.append(np.random.choice([0,1,2]))  # фиктивный target

X = pd.concat(X_list, ignore_index=True)
y = pd.Series(y_list)

cat_features = ["subscription_type", "onboarding_goal"]

model = CatBoostClassifier(
    iterations=50,
    depth=4,
    learning_rate=0.05,
    loss_function='MultiClass',
    cat_features=cat_features
)

model.fit(X, y)
model.save_model("models/catboost_model.cbm")
print("Model saved to models/catboost_model.cbm")