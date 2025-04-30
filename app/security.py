from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, Header, HTTPException
from argon2 import PasswordHasher
from passlib.context import CryptContext

from sqlmodel import Session, select
from app.database import get_session
from app.users.models import User

# ───────── JWT constants ─────────
SECRET_KEY = "CHANGE_ME_IN_PROD"
ALGORITHM = "HS256"
ACCESS_EXPIRES_MIN = 30

# ───────── password hashing ──────
ph = PasswordHasher()  # argon2
legacy_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")  # keep old hashes

def hash_pw(password: str) -> str:
    return ph.hash(password)

def verify_pw(plain: str, hashed: str) -> bool:
    try:
        ph.verify(hashed, plain)
        return True
    except Exception:
        return legacy_ctx.verify(plain, hashed)

# ───────── JWT helpers ───────────
def create_token(sub: str) -> str:
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRES_MIN)
    return jwt.encode({"sub": sub, "exp": exp}, SECRET_KEY, algorithm=ALGORITHM)

# ───────── auth dependencies ─────
def get_current_user(
    authorization: str = Header(...),
    session: Session = Depends(get_session),
) -> User:
    try:
        _, _, token = authorization.partition(" ")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload["sub"]
        user = session.exec(select(User).where(User.username == username)).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def admin_required(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return user
