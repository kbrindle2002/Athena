from fastapi import FastAPI, responses
from pathlib import Path

app = FastAPI(title="ATHENA API")

# ── 1) Friendly JSON “health” endpoint  ────────────────────────────
@app.get("/")
def health():
    return {"athena": "API online", "status": "ok"}

# ── 2) Optional: serve the landing page on /home  ───────────────────
landing_html = (
    Path(__file__)
    .resolve()                            # backend/
    .parent                               # backend
    .parent                               # ATHENA
    / "frontend"
    / "LaunchLandingPage.html"
)

@app.get("/home", response_class=responses.HTMLResponse)
def landing_page():
    return landing_html.read_text(encoding="utf-8")

# ── 3) Existing demo endpoint  ──────────────────────────────────────
@app.post("/process_task/")
async def process_task(task: dict):
    complexity = task.get("complexity", 0)
    if complexity > 80:
        return {"mode": "quantum", "detail": "Routed to quantum backend"}
    return {"mode": "classical", "detail": "Processed classically"}
