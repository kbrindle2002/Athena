from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.router import router as demo_router          # <-- add this line
from core.module_loader import load_enabled_modules

app = FastAPI(title="ATHENA API")

@app.get("/ping")
def ping():
    return {"status": "pong"}

# register routers
app.include_router(auth_router)
app.include_router(demo_router)                       # <-- and this line

for r in load_enabled_modules():
    app.include_router(r)
