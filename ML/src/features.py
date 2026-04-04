import pandas as pd

# Загружаем CSV один раз при импорте
gen_df = pd.read_csv("data/test_users_generations.csv")
txn_df = pd.read_csv("data/test_users_transaction_attempts.csv")
purch_df = pd.read_csv("data/test_users_purchases.csv")
props_df = pd.read_csv("data/test_users_properties.csv")
quiz_df = pd.read_csv("data/test_users_quizzes.csv")

# Приведение колонок к нижнему регистру и strip
for df in [gen_df, txn_df, purch_df, props_df, quiz_df]:
    df.columns = df.columns.str.strip().str.lower()

def build_features(user_id):
    feats = {}

    # --- Generations ---
    u_gen = gen_df[gen_df["user_id"] == user_id]
    if not u_gen.empty:
        created_dates = pd.to_datetime(u_gen["created_at"], errors='coerce').dt.tz_convert(None)
        feats["total_generations"] = len(u_gen)
        feats["active_days"] = created_dates.dt.date.nunique()
        feats["days_since_last_gen"] = (pd.Timestamp.now() - created_dates.max()).days
        feats["failed_generations"] = u_gen['status'].str.contains('failed', na=False).sum()
    else:
        feats["total_generations"] = 0
        feats["active_days"] = 0
        feats["days_since_last_gen"] = 0
        feats["failed_generations"] = 0

    # --- Transactions ---
    feats["total_attempts"] = len(txn_df)
    feats["failed_attempts"] = txn_df['failure_code'].notnull().sum()
    feats["fail_rate"] = feats["failed_attempts"] / max(1, feats["total_attempts"])
    feats["unique_payment_methods"] = txn_df['payment_method_type'].nunique() if 'payment_method_type' in txn_df.columns else 0

    # --- Purchases ---
    u_pur = purch_df[purch_df["user_id"] == user_id]
    feats["total_purchases"] = len(u_pur)
    feats["total_spent"] = u_pur["purchase_amount_dollars"].sum() if not u_pur.empty else 0.0

    # --- Properties ---
    u_prop = props_df[props_df["user_id"] == user_id]
    if not u_prop.empty:
        feats["subscription_type"] = str(u_prop["subscription_plan"].values[0]) if pd.notna(u_prop["subscription_plan"].values[0]) else "unknown"
        start_date = pd.to_datetime(u_prop["subscription_start_date"], errors='coerce')
        if pd.api.types.is_datetime64tz_dtype(start_date):
            start_date = start_date.dt.tz_convert(None)
        feats["days_since_start"] = (pd.Timestamp.now() - start_date.max()).days
    else:
        feats["subscription_type"] = "unknown"
        feats["days_since_start"] = 0

    # --- Quizzes ---
    u_quiz = quiz_df[quiz_df["user_id"] == user_id]
    if not u_quiz.empty:
        feats["onboarding_goal"] = str(u_quiz["usage_plan"].values[0]) if "usage_plan" in u_quiz.columns and pd.notna(u_quiz["usage_plan"].values[0]) else "unknown"
    else:
        feats["onboarding_goal"] = "unknown"

    return pd.DataFrame([feats])