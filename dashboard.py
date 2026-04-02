import streamlit as st
import requests
import pandas as pd
import sqlite3

st.set_page_config(page_title="Sentinel Forensic Dashboard", layout="wide")
st.title("🛡️ Sentinel Forensic: Fraud Investigation Console")

# --- Session State Initialization ---
if 'amt' not in st.session_state: st.session_state['amt'] = 100.0
if 'loc_idx' not in st.session_state: st.session_state['loc_idx'] = 0
if 'dev_idx' not in st.session_state: st.session_state['dev_idx'] = 0

# --- Sidebar: Inputs ---
st.sidebar.header("📡 Live Transaction Feed")

# Load Fraud Sample Sync
if st.sidebar.button("🚨 Load Real Fraud Sample"):
    df = pd.read_csv("creditcard.csv")
    fraud_row = df[df['Class'] == 1].sample(1).iloc[0]
    st.session_state['full_row'] = fraud_row.to_dict()
    st.session_state['amt'] = float(fraud_row['Amount'])
    # Sync UI for Fraud Simulation
    st.session_state['loc_idx'] = 2 # International
    st.session_state['dev_idx'] = 2 # Unknown/Emulator
    st.rerun()

# Dynamic Inputs
amt_input = st.sidebar.number_input("Transaction Amount ($)", value=st.session_state['amt'])
loc_list = ["Home City", "New City", "International (High Risk)"]
location = st.sidebar.selectbox("Location Status", loc_list, index=st.session_state['loc_idx'])
dev_list = ["Trusted Device", "New Device", "Unknown/Emulator"]
device = st.sidebar.selectbox("Device Identity", dev_list, index=st.session_state['dev_idx'])
network = st.sidebar.radio("Network Security", ["Secure Home/Work", "Public Wi-Fi", "VPN/Proxy"])

if st.sidebar.button("🔍 Run Forensic Analysis", type="primary"):
    payload = {
        "amount": amt_input, "location": location, "device": device,
        "network": network, "is_manual": 'full_row' not in st.session_state
    }
    if 'full_row' in st.session_state: payload.update(st.session_state['full_row'])

    try:
        r = requests.post("http://127.0.0.1:8000/predict", json=payload)
        res = r.json()
        
        if res.get("is_fraud"):
            st.error(f"## 🚨 FRAUD DETECTED")
            st.warning(f"**Forensic Reason:** {res['reason']}")
            st.info(f"**ML Confidence:** {res['confidence']:.2%}")
        else:
            st.success(f"## ✅ TRANSACTION APPROVED")
            st.write("Pattern Analysis: Trusted Profile")
        
        # Clear sample after test to allow manual testing again
        if 'full_row' in st.session_state: del st.session_state['full_row']
    except:
        st.error("Backend Connection Error")

# --- Analytics ---
st.divider()
conn = sqlite3.connect('transactions.db')
history_df = pd.read_sql_query("SELECT * FROM history ORDER BY timestamp DESC LIMIT 10", conn)
st.subheader("📜 Recent Forensic Activity")
st.dataframe(history_df, width=1200)