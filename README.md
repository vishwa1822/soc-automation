# soc-automation
# 🛡️ AI-Driven SOC Automation System with SOAR, LLM, RAG & Dynamic Deception

## 📌 Overview

AI-powered SOC system for real-time threat detection, investigation, and automated response using ML, LLM, RAG, and dynamic deception techniques. Focused on identity and system logs with lightweight network detection.

---

## 🚧 Project Status

🟢 Near Completion

* SOC pipeline ✔
* Detection engines ✔
* Deception system ✔
* RAG investigation ✔
* SOAR automation ✔
* Dashboard ✔ (UI refining)

---

## 🎯 Core Features

### 🔍 Detection Layer

* ML anomaly detection (**Isolation Forest + Ensemble**)
* Behavioral detection 
* Identity anomaly detection 
* Rule-based network detection 
---

### 🎭 Dynamic Deception System

* Honeytokens (`honeytokens/`)
* Fake endpoints, files, credentials
* **Automatic generation + rotation**
* High-confidence attacker detection

---

### 🧠 AI & Investigation

* RAG engine (`rag_engine.py`) → FAISS-based retrieval
* NLP SOC assistant (`nlp_soc_assistant.py`, `soc_ai_analyst.py`)
* Explainable AI insights

---

### ⚙️ Event-Driven Architecture

* EventBus (`event_bus.py`)
* Asynchronous pipeline
* Scalable detection flow

---

### 🔗 Correlation & Attack Analysis

* Correlation engine 
* Attack correlation 
* Attack graph 
* Timeline analysis 

---

### ⚠️ Risk & Alerting

* Risk engine 
* Alert engine 
* Prioritization + SOAR triggers

---

### 📊 Data Processing

* Log processing 
* Feature engineering
* Batch analysis

---

### 🗄️ Storage & Memory

* PostgreSQL (`database.py`)
* Schemas (`schemas.py`)
* SOC Memory + Vector storage 

---

### 🔬 ML Pipeline

* ML pipeline (`ml_pipeline.py`)
* Model management (`models.py`)

---

## 🏗️ Architecture
Victim Application 
          ↓
HTTP Log Ingestion 
          ↓
Log Processor → Feature Engineering 
          ↓
EventBus (Event-Driven Processing)
          ↓ 
Detection Engines: 
- ML Anomaly Detection
- Behavioral Detection
- Identity Detection
- Deception Detection (Honeytokens)
- Rule-Based Network Detection
          ↓
Correlation & Attack Analysis
          ↓
 Risk Engine
         → Alert Engine
          ↓
   PostgreSQL + SOC Memory + FAISS
           ↓
   RAG Investigation + LLM Analysis
           ↓
   SOAR Automation ↓ Frontend Dashboard

## 🧰 Tech Stack

* Python, FastAPI
* Isolation Forest, Ensemble ML
* LLM, RAG, FAISS
* PostgreSQL
* React + Vite
* Concepts: SOC, SOAR, UEBA, Deception Security

---

## 📂 Project Structure

```text
backend/            # SOC engines & APIs
frontend/           # Dashboard
victim_app/         # Log generator
models/             # ML models
attacks/            # Attack simulation
```

---

## ▶️ Run

### Backend

```bash
uvicorn main:app --reload
```

### Frontend

```bash
npm install
npm run dev
```

### Victim App

```bash
python app.py
```

---

## 🚀 Future Enhancements

* Advanced SOAR automation
* More network log coverage
* Better visualization
* Improved model accuracy

---

## 👨‍💻 Author

Vishwa Vishwa
Cybersecurity & AI Enthusiast
