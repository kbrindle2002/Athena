# ATHENA

**Stories of Humanity.**

ATHENA preserves human memories and emotional wisdom across generations using a hybrid Quantum‑Classical architecture.

## Structure
- `frontend/` — public portal (landing page, story upload, beta signup)
- `backend/` — dispatcher & story intake APIs
- `quantum_backend/` — Azure Quantum submission + Qiskit simulator
- `whitepaper/` — ATHENA Whitepaper
- `founder_certificate/` — Founder Certificate (PDF/PNG)

## Quick start
```bash
pip install fastapi uvicorn azure-quantum qiskit
uvicorn backend.dispatcher_api:app --reload
```
