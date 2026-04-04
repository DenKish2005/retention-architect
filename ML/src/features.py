import pandas as pd

def build_features(user_id):
    # Загрузка CSV из ML/data
    gen_df = pd.read_csv("data/test_users_generations.csv")
    txn_df = pd.read_csv("data/test_users_transaction_attempts.csv")
    purch_df = pd.read_csv("data/test_users_purchases.csv")
    props_df = pd.read_csv("data/test_users_properties.csv")
    quiz_df = pd.read_csv("data/test_users_quizzes.csv")
    
    feats = {}
    # --- generations ---
    u_gen = gen_df[gen_df.user_id == user_id]
    feats["total_generations"] = len(u_gen)
    feats["active_days"] = u_gen["date"].nunique()
    # --- transactions ---
    u_txn = txn_df[txn_df.user_id == user_id]
    feats["total_attempts"] = len(u_txn)
    feats["failed_attempts"] = (u_txn["status"]=="failed").sum()
    feats["fail_rate"] = feats["failed_attempts"]/max(1, feats["total_attempts"])
    # --- purchases ---
    u_pur = purch_df[purch_df.user_id == user_id]
    feats["total_purchases"] = len(u_pur)
    feats["total_spent"] = u_pur["amount"].sum()
    # --- properties ---
    u_prop = props_df[props_df.user_id == user_id].iloc[0]
    feats["subscription_type"] = u_prop["subscription_type"]
    # --- quizzes ---
    u_quiz = quiz_df[quiz_df.user_id == user_id]
    feats["onboarding_goal"] = u_quiz["goal"].values[0] if len(u_quiz) else "unknown"
    
    return pd.DataFrame([feats])