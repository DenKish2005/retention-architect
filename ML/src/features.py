import pandas as pd
import os

# Загружаем один раз при старте — путь относительно ML/
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")

gen_df   = pd.read_csv(os.path.join(DATA, "test_users_generations.csv"),       low_memory=False)
txn_df   = pd.read_csv(os.path.join(DATA, "test_users_transaction_attempts.csv"), low_memory=False)
purch_df = pd.read_csv(os.path.join(DATA, "test_users_purchases.csv"),          low_memory=False)
props_df = pd.read_csv(os.path.join(DATA, "test_users_properties.csv"),         low_memory=False)
quiz_df  = pd.read_csv(os.path.join(DATA, "test_users_quizzes.csv"),            low_memory=False)

for df in [gen_df, txn_df, purch_df, props_df, quiz_df]:
    df.columns = df.columns.str.strip().str.lower()

# Нормализуем user_id в транзакциях — там нет user_id напрямую,
# но есть transaction_id. Джойним через purchases.
# purchases: user_id, transaction_id
# transaction_attempts: transaction_id, failure_code, ...
txn_with_user = txn_df.merge(
    purch_df[["user_id", "transaction_id"]].drop_duplicates(),
    on="transaction_id", how="left"
)

def build_features(user_id: str) -> pd.DataFrame:
    feats = {}

    # --- Generations ---
    u_gen = gen_df[gen_df["user_id"] == user_id]
    feats["total_generations"] = len(u_gen)
    if not u_gen.empty and "created_at" in u_gen.columns:
        dates = pd.to_datetime(u_gen["created_at"], errors="coerce", utc=True)
        feats["active_days"]         = dates.dt.date.nunique()
        feats["failed_generations"]  = u_gen["status"].str.lower().str.contains("fail|nsfw", na=False).sum()
        feats["gen_per_active_day"]  = feats["total_generations"] / max(feats["active_days"], 1)
    else:
        feats["active_days"]        = 0
        feats["failed_generations"] = 0
        feats["gen_per_active_day"] = 0.0

    # --- Transaction attempts (через user_id из purchases) ---
    u_txn = txn_with_user[txn_with_user["user_id"] == user_id]
    feats["total_attempts"]  = len(u_txn)
    feats["failed_attempts"] = u_txn["failure_code"].notna().sum() if "failure_code" in u_txn.columns else 0
    feats["fail_rate"]       = feats["failed_attempts"] / max(feats["total_attempts"], 1)

    # --- Purchases ---
    u_pur = purch_df[purch_df["user_id"] == user_id]
    feats["total_purchases"] = len(u_pur)
    feats["total_spent"]     = float(u_pur["purchase_amount_dollars"].sum()) if not u_pur.empty else 0.0

    # --- Properties ---
    u_prop = props_df[props_df["user_id"] == user_id]
    if not u_prop.empty:
        feats["subscription_type"] = str(u_prop["subscription_plan"].iloc[0]) \
            if pd.notna(u_prop["subscription_plan"].iloc[0]) else "unknown"
    else:
        feats["subscription_type"] = "unknown"

    # --- Quizzes ---
    u_quiz = quiz_df[quiz_df["user_id"] == user_id]
    if not u_quiz.empty and "usage_plan" in u_quiz.columns:
        val = u_quiz["usage_plan"].iloc[0]
        feats["onboarding_goal"] = str(val) if pd.notna(val) else "unknown"
    else:
        feats["onboarding_goal"] = "unknown"

    return pd.DataFrame([feats])