# ANVAYA AI OPERATOR – NILM R&D

AI-based Non-Intrusive Load Monitoring (NILM) system for hotel electricity intelligence.

---

## 🔷 PROJECT OVERVIEW

This repository contains:

1. Simulated NILM Research (Seq2Point + VMD)
2. Real Hardware NILM (AC detection & health)
3. AC runtime, energy, and anomaly detection
4. Backend API for dashboard integration

---

## 🔷 ARCHITECTURE

Hardware → CSV → Cleaning → Event Detection → 
State Clustering (KMeans) → 
AC Runtime & Energy → 
Health Scoring → API Output

---

## 🔷 TECH STACK

- Python 3.14
- Pandas / NumPy
- Scikit-Learn (KMeans clustering)
- FastAPI (backend)
- InfluxDB (optional time-series storage)
- Docker (Infra layer)

---

## 🔷 RESULTS (REAL DATA – PHASE 1)

AC Mean Power: 2891 W  
AC Runtime: 24.42 hrs  
AC Energy: 70.62 kWh  
Total Room Energy: 86.17 kWh  
AC Contribution: 81.96%  
AC Cycles: 103  

Health Score model implemented with anomaly detection.

---

## 🔷 FOLDER STRUCTURE

core/ → ingestion + simulation engine  
research/ → Seq2Point + VMD experiments  
real_nilm/ → real data NILM pipeline  
backend/ → FastAPI metrics endpoint  
data/ → cleaned datasets  

---

## 🔷 HOW TO RUN

Install dependencies:
pip install -r requirements.txt

Run real NILM:
python real_nilm_phase1.py
python real_nilm_state_clustering.py
python real_nilm_ac_metrics.py
python ac_daily_health_score.py

Run backend:
cd backend
uvicorn main:app --reload

---

## 🔷 FUTURE WORK

- Real-time MQTT ingestion
- AWS deployment
- Multi-appliance detection
- VMD + Deep NILM hybrid model
- Production-grade streaming pipeline

---

Built by Anvaya Enertech – Electricity Intelligence Platform
