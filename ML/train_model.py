# python train_model.py
# Запускать из папки ML/

import pandas as pd
import numpy as np
import os
from catboost import CatBoostClassifier
from src.features import build_features

DATA = "data"

# Читаем train_users (там есть target — статус подписки)
users_path = os.path.join(DATA, "train_users.csv")
if not os.path.exists(users_path):
    # Если train нет — берём test и делаем synthetic target
    print("train_users.csv не найден, используем test_users.csv с synthetic target")
    users = pd.read_csv(os.path.join(DATA, "test_users.csv"))
    users.columns = users.columns.str.strip().str.lower()
    users["churn_status"] = np.random.choice(
        ["stayed", "voluntary_churn", "involuntary_churn"],
        size=len(users),
        p=[0.5, 0.25, 0.25]
    )
else:
    users = pd.read_csv(users_path)
    users.columns = users.columns.str.strip().str.lower()

# Маппинг target → числа
label_map = {"stayed": 0, "voluntary_churn": 1, "involuntary_churn": 2}

# Если колонка с таргетом называется иначе — поправь здесь
target_col = None
for col in users.columns:
    if "churn" in col or "status" in col:
        target_col = col
        break

if target_col is None:
    raise ValueError(f"Не нашёл колонку с таргетом. Колонки: {users.columns.tolist()}")

print(f"Используем колонку таргета: '{target_col}'")
print(f"Уникальные значения: {users[target_col].unique()}")

# Строим фичи — берём подвыборку если данных много (ускорение)
sample_size = min(500, len(users))
users_sample = users.sample(n=sample_size, random_state=42).reset_index(drop=True)

X_list, y_list = [], []
skipped = 0

for _, row in users_sample.iterrows():
    uid = row["user_id"]
    status = str(row[target_col]).strip().lower()

    # Нормализация значений таргета
    if "involuntary" in status or "payment" in status or "card" in status:
        y = 2
    elif "voluntary" in status or "cancel" in status or "churn" in status:
        y = 1
    elif "stay" in status or "active" in status or "retained" in status:
        y = 0
    else:
        skipped += 1
        continue

    try:
        X_row = build_features(uid)
        X_list.append(X_row)
        y_list.append(y)
    except Exception as e:
        skipped += 1
        continue

print(f"Обработано: {len(X_list)}, пропущено: {skipped}")
print(f"Распределение классов: {pd.Series(y_list).value_counts().to_dict()}")

X = pd.concat(X_list, ignore_index=True)
y = pd.Series(y_list)

cat_features = ["subscription_type", "onboarding_goal"]

model = CatBoostClassifier(
    iterations=200,
    depth=5,
    learning_rate=0.05,
    loss_function="MultiClass",
    cat_features=cat_features,
    verbose=25,
    random_seed=42,
    early_stopping_rounds=30,
)

model.fit(X, y, eval_set=(X, y))  # для хакатона eval на train ок
model.save_model("models/catboost_model.cbm")
print("\n✅ Модель сохранена: models/catboost_model.cbm")
print(f"Фичи: {X.columns.tolist()}")