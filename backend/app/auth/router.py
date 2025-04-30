from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from app.database import get_session
from app.users.models import User
from app.security import verify_pw, create_token

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginReq(BaseModel):
    username: str
    password: str

class TokenResp(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResp, summary="Username+password → JWT")
def login(body: LoginReq, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == body.username)).first()
    if not user or not verify_pw(body.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResp(access_token=create_token(user.username))
