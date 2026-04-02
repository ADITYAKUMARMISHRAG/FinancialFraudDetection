import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE 
import joblib
import shap

def train():
    # 1. Load Kaggle Data
    print("📂 Loading dataset...")
    try:
        df = pd.read_csv("creditcard.csv")
    except FileNotFoundError:
        print("❌ Error: 'creditcard.csv' nahi mili! File check karo.")
        return

    # 2. Preprocessing
    scaler = StandardScaler()
    df['normAmount'] = scaler.fit_transform(df['Amount'].values.reshape(-1, 1))
    df = df.drop(['Time', 'Amount'], axis=1)
    
    X = df.drop('Class', axis=1) 
    y = df['Class']
    
    # 3. Train-Test Split (Stratify use kar rahe hain taaki fraud distribution sahi rahe)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 4. SMOTE (Handling Imbalance)
    print("🔄 Balancing dataset with SMOTE (Fraud samples badha rahe hain)...")
    sm = SMOTE(random_state=42)
    X_train_res, y_train_res = sm.fit_resample(X_train, y_train)
    
    # 5. Training
    print("🚀 Training Random Forest Model...")
    model = RandomForestClassifier(n_estimators=100, max_depth=10, n_jobs=-1, random_state=42)
    model.fit(X_train_res, y_train_res)
    
    # 6. SHAP Explainer (Explainability ke liye)
    print("⏳ Generating SHAP Explainer (It might take a minute)...")
    explainer = shap.TreeExplainer(model)
    
    # 7. Assets Save Karo
    print("💾 Saving assets...")
    joblib.dump(model, "fraud_model.joblib")
    joblib.dump(scaler, "scaler.joblib")
    joblib.dump(list(X.columns), "features.joblib")
    joblib.dump(explainer, "explainer.joblib")
    
    print("✅ All assets saved successfully! Ab app.py chala sakte ho.")

if __name__ == "__main__":
    train()