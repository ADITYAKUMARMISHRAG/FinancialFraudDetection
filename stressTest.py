import pandas as pd
import requests
import time
import random

def run_test(n=50):
    url = "http://127.0.0.1:8000/predict"
    
    try:
        # 1. Kaggle CSV load karo taaki real samples bhej sakein
        df = pd.read_csv("creditcard.csv")
        
        # Mix of Fraud and Safe transactions for better testing
        fraud_samples = df[df['Class'] == 1]
        safe_samples = df[df['Class'] == 0].sample(n)
        
        # Dono ko combine karke shuffle kar do
        test_samples = pd.concat([fraud_samples.sample(min(len(fraud_samples), n//2)), 
                                 safe_samples.sample(n//2)]).sample(frac=1)
        
        print(f"🚀 Starting Stress Test with {len(test_samples)} real samples...")

        for i, (_, row) in enumerate(test_samples.iterrows()):
            # Naye app.py logic ke hisaab se sirf amount bhej rahe hain
            # (Baaki V1-V28 backend placeholder se handle ho rahe hain)
            payload = {
                "amount": float(row['Amount'])
            }
            
            try:
                start_time = time.time()
                response = requests.post(url, json=payload)
                latency = (time.time() - start_time) * 1000 # Milliseconds mein
                
                if response.status_code == 200:
                    res_data = response.json()
                    status = "🚨 FRAUD" if res_data.get('is_fraud') else "✅ SAFE"
                    actual = "FRAUD" if row['Class'] == 1 else "SAFE"
                    
                    print(f"[{i+1}] Amt: {row['Amount']:>8.2f} | Pred: {status} | Actual: {actual} | Latency: {latency:.2f}ms")
                else:
                    print(f"❌ Failed at {i+1}: Server Error {response.status_code}")
            
            except Exception as e:
                print(f"🚫 Connection Error at {i+1}: {e}")
            
            time.sleep(0.1) # Realistic gap

    except FileNotFoundError:
        print("Error: 'creditcard.csv' nahi mili! Data file same folder mein rakho.")

if __name__ == "__main__":
    run_test(50)