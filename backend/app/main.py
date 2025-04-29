from fastapi import FastAPI
from app.auth.router import router as auth_router
from core.module_loader import load_enabled_modules

app = FastAPI(title="ATHENA API")

@app.get("/ping")
def ping():
    return {"status": "pong"}

app.include_router(auth_router)

for r in load_enabled_modules():
    app.include_router(r)
