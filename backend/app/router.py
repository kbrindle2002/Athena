from fastapi import APIRouter, Depends
from app.security import get_current_user   # ✅ import from security

router = APIRouter(tags=["demo"])

@router.get("/protected")
def protected(user: str = Depends(get_current_user)):
    return {"hello": user}