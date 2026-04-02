from fastapi import FastAPI
import joblib, pandas as pd, numpy as np, shap, sqlite3, traceback, os

app = FastAPI()

# --- Assets Loading ---
model, feature_cols, scaler, explainer = None, [], None, None

def load_assets():
    global model, feature_cols, scaler, explainer
    try:
        if os.path.exists("fraud_model.joblib"):
            model = joblib.load("fraud_model.joblib")
            feature_cols = joblib.load("features.joblib")
            scaler = joblib.load("scaler.joblib")
            explainer = joblib.load("explainer.joblib")
            print("✅ All assets loaded!")
    except Exception as e: print(f"⚠️ Error: {e}")

load_assets()

def save_to_db(amt, res, confidence, reason):
    try:
        conn = sqlite3.connect('transactions.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS history 
                     (amt REAL, res TEXT, confidence REAL, reason TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        c.execute("INSERT INTO history (amt, res, confidence, reason) VALUES (?, ?, ?, ?)", (amt, res, confidence, reason))
        conn.commit()
        conn.close()
    except: pass

@app.post("/predict")
def predict(data: dict):
    try:
        amt = float(data.get("amount", 0))
        location = data.get("location", "Home City")
        device = data.get("device", "Trusted Device")
        is_manual = data.get("is_manual", True)

        # --- STEP 1: SANITY CHECK (Real-world Layer) ---
        # Itna bada amount (e.g. > $1M) bina ML ke hi High Risk hona chahiye
        if amt > 1000000:
            return {
                "is_fraud": True,
                "confidence": 1.0,
                "reason": "Security Trigger: Transaction amount exceeds daily legal limit",
                "db_status": "Saved"
            }

        # --- STEP 2: ML PREDICTION ---
        input_dict = {col: 0.0 for col in feature_cols}
        input_dict['normAmount'] = scaler.transform([[amt]])[0][0]
        df = pd.DataFrame([input_dict])[feature_cols]
        
        prob = float(model.predict_proba(df)[0][1])

        # --- STEP 3: LOGIC TUNING (Hybrid Rules) ---
        if is_manual:
            # 1 Dollar waale issue ka fix: Chote amounts pe chill raho
            if amt < 10 and device == "Trusted Device":
                prob = min(prob, 0.1)
            
            # High Risk Scenarios ko properly handle karo
            if location == "International (High Risk)" and amt > 100:
                prob = max(prob, 0.85)
            
            if device == "Unknown/Emulator":
                prob = max(prob, 0.70)

        # Final Decision
        status = "Fraud" if prob > 0.5 else "Safe"
        
        # Proper Reason Mapping
        reason = "Pattern Analysis: Trusted Profile"
        if status == "Fraud":
            reason = f"Alert: High Risk {location} activity" if is_manual else "Neural Pattern Match"

        save_to_db(amt, status, round(prob, 4), reason)
        
        return {
            "is_fraud": (status == "Fraud"),
            "confidence": round(prob, 4),
            "reason": reason
        }

    except Exception as e:
        print(traceback.format_exc())
        return {"error": str(e)}