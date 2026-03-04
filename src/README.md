ANVAYA AI OPERATOR – NILM & MOTOR HEALTH R&D

AI-based Electricity Intelligence Platform for Hotels

🔷 PROJECT OVERVIEW

This repository contains two major intelligence layers:

1️⃣ Low Sampling NILM (1 Hz)

Appliance disaggregation from aggregate power

AC detection

Runtime estimation

Energy attribution

Behavioral anomaly detection

Health scoring

2️⃣ High Sampling Motor Health (5–10 kHz)

HVAC compressor health monitoring

Bearing fault detection

Harmonic distortion tracking

Startup transient modeling

Hybrid real-time health engine

🔷 SYSTEM ARCHITECTURE
🔹 Low Sampling Layer (Room / Phase Meter – 1 Hz)

Hardware → CSV → Cleaning → Event Detection → State Clustering → Appliance Runtime & Energy → Health Scoring → API Output

Used for:

AC energy tracking

Usage analytics

Behavioral anomaly detection

🔹 High Sampling Layer (Main HVAC Line – 5–10 kHz)

Waveform → Sliding Window → Signal Processing → Health Index → Edge Output → Cloud Diagnostics

Used for:

Compressor health

Bearing fault detection

Harmonic tracking

Predictive maintenance

🔷 HIGH SAMPLING METHODS (PHASE 1)

Implemented and evaluated:

Method A — VMD (Variational Mode Decomposition)

Intrinsic mode energy redistribution

Cloud-grade deep diagnostics

Strong fault separation

Method B — Envelope + Hilbert Transform

Amplitude modulation detection

Strongest steady-state bearing fault detection

Edge deployable

Method C — FFT Harmonic Tracking

Harmonic & sideband energy monitoring

Lightweight embedded implementation

Method D — Startup Transient Modeling

Inrush peak & decay analysis

Early-stage fault detection

Very low computational cost

Method E — Hybrid (Envelope + FFT Fusion)

Moderate-cost optimized fusion engine

Balanced performance & efficiency

Recommended edge-level steady-state solution

🔷 TECH STACK

Python 3.14
Pandas / NumPy
Scikit-Learn (KMeans clustering)
Scipy (Signal Processing)
FastAPI (backend)
InfluxDB (optional time-series storage)
Docker (Infrastructure layer)

🔷 RESULTS
🔹 Real NILM (1 Hz – Room Phase)

AC Mean Power: 2891 W
AC Runtime: 24.42 hrs
AC Energy: 70.62 kWh
Total Room Energy: 86.17 kWh
AC Contribution: 81.96%
AC Cycles: 103

Health score model implemented with anomaly detection.

🔹 High Sampling HVAC Health (5 kHz – Simulated)

Separation Performance (Healthy vs Fault):

Envelope Method → Strongest separation
VMD → Deep diagnostic separation
Hybrid → Balanced moderate-cost solution
FFT → Lightweight baseline monitoring
Startup → Early anomaly detection

Hybrid architecture validated for edge + cloud deployment.

🔷 FOLDER STRUCTURE
core/ → ingestion + simulation engine  
real_nilm/ → 1 Hz appliance disaggregation  
high_sampling_nilm/ → 5 kHz motor health R&D  
backend/ → FastAPI metrics endpoint  
data/ → cleaned datasets  
docs/ → technical documentation  
🔷 HOW TO RUN
Install Dependencies
pip install -r requirements.txt
Run Real NILM (1 Hz)
python real_nilm_phase1.py  
python real_nilm_state_clustering.py  
python real_nilm_ac_metrics.py  
python ac_daily_health_score.py  
Run High Sampling Methods

Example:

export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python -m high_sampling_nilm.methods.method_envelope.run_envelope
Run Backend
cd backend  
uvicorn main:app --reload
🔷 PRODUCTION ROADMAP

Real-time MQTT ingestion

Embedded DSP implementation (Envelope + FFT)

Cloud deep diagnostics (VMD layer)

Multi-appliance separation

AWS deployment

Full Native AI Electricity Operator pipeline

Built by Anvaya Enertech
Electricity Intelligence Platform