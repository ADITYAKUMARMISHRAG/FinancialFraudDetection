# FinancialFraudDetection
uvicorn app:app --reload
streamlit run dashboard.py


# 💳 Real-Time Fraud Detection System (FinTech)

A scalable end-to-end **Machine Learning pipeline** for **real-time fraud detection** in financial transactions.  
This project simulates a production-style FinTech system where incoming transactions are processed, transformed into meaningful features, and passed through a trained ML model for **instant fraud prediction**.

---

## 🚀 Project Highlights

- ⚡ **Real-time fraud prediction** using a low-latency REST API
- 🧠 **Machine Learning pipeline** built with **Python** and **Scikit-learn**
- 🏗️ **Production-ready modular architecture**
- 📊 **Feature engineering** for transaction risk profiling
- 🔁 **Streaming-style simulation** for live transaction scoring
- 🎯 Achieved **94% model accuracy**
- 🌐 **Flask API** for serving fraud predictions in real time

---

## 📌 Problem Statement

Digital payment systems process millions of transactions every day, making them vulnerable to fraudulent activity.  
Traditional fraud checks are often delayed or rule-based, which can fail to detect evolving fraud patterns.

This project addresses the problem by building a **real-time ML-based fraud detection system** that can:

- detect suspicious transactions instantly,
- scale with incoming transaction streams,
- and serve predictions through an API suitable for integration into FinTech platforms.

---

## 🛠️ Tech Stack

### **Languages & Libraries**
- **Python**
- **Scikit-learn**
- **Pandas**
- **NumPy**
- **Joblib**

### **Backend / Deployment**
- **Flask**
- **REST API**

### **ML / Data Pipeline**
- Data preprocessing
- Feature engineering
- Model training & evaluation
- Real-time inference

---

## 🧠 ML Workflow

The system follows a complete machine learning lifecycle:

### 1. **Data Ingestion**
Transaction data is loaded and validated before entering the training/inference pipeline.

### 2. **Preprocessing**
- Missing value handling
- Encoding categorical variables
- Feature scaling / transformation
- Data cleaning

### 3. **Feature Engineering**
Custom transaction-level risk features are engineered to improve fraud detection performance, such as:

- transaction amount behavior
- merchant/category patterns
- time-based activity signals
- customer-level spending anomalies
- frequency-based suspicious behavior

### 4. **Model Training**
A supervised ML classifier is trained to distinguish between **fraudulent** and **legitimate** transactions.

### 5. **Evaluation**
The model is evaluated using classification metrics to ensure strong fraud detection performance.

### 6. **Model Serving**
The trained model is deployed using **Flask**, exposing an API endpoint for real-time fraud scoring.

---

## 📈 Model Performance

| Metric        | Score |
|--------------|-------|
| Accuracy     | **94%** |
| Inference    | **Low Latency** |
| Deployment   | **REST API Enabled** |

> **Note:** In fraud detection, metrics like **Precision**, **Recall**, **F1-score**, and **ROC-AUC** are often more meaningful than accuracy alone due to class imbalance.

---

## 🏗️ System Architecture

```text
Incoming Transaction
        │
        ▼
Data Validation / Parsing
        │
        ▼
Feature Engineering
        │
        ▼
Preprocessing Pipeline
        │
        ▼
Trained ML Model
        │
        ▼
Fraud / Not Fraud Prediction
        │
        ▼
REST API Response
