from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.router import router as auth_router
from app.router import router as demo_router          # <-- add this line
from app.users.router import router as users_router
from core.module_loader import load_enabled_modules
from app.database import init_db
from app.seed import seed



app = FastAPI(title="ATHENA API")
init_db()
seed()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
def ping():
    return {"status": "pong"}

# register routers
app.include_router(auth_router)
app.include_router(demo_router)  
app.include_router(users_router)
                     # <-- and this line

for r in load_enabled_modules():
    app.include_router(r)
