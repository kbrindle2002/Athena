import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.database import init_db
from app.seed import seed
from app.auth.router import router as auth_router
from app.users.router import router as users_router

app = FastAPI(title="ATHENA API")

@app.on_event("startup")
def _startup() -> None:
    init_db()
    seed()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    return {"status": "pong"}

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

# routers
app.include_router(auth_router)
app.include_router(users_router)
