from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import User
from app.security import hash_pw, get_current_user

router = APIRouter(prefix="/users", tags=["users"])

# ───── helper ───────────────────────────────────────────────
def _require_admin(current: str):
    if current != "admin":                # <— simple demo check
        raise HTTPException(status_code=403, detail="Admins only")


# ───── Schemas (Pydantic via SQLModel) ──────────────────────
class UserRead(User):
    id: int


class UserCreate(User):
    password: str


class UserUpdate(UserCreate):
    username: Optional[str] = None
    password: Optional[str] = None


# ───── CRUD endpoints ───────────────────────────────────────
@router.get("/", response_model=List[UserRead])
def list_users(session: Session = Depends(get_session),
               current: str = Depends(get_current_user)):
    return session.exec(select(User)).all()


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int,
             session: Session = Depends(get_session),
             current: str = Depends(get_current_user)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(body: UserCreate,
                session: Session = Depends(get_session),
                current: str = Depends(get_current_user)):
    _require_admin(current)
    if session.exec(select(User).where(User.username == body.username)).first():
        raise HTTPException(400, "Username taken")

    user = User(username=body.username,
                password_hash=hash_pw(body.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.put("/{user_id}", response_model=UserRead)
def replace_user(user_id: int, body: UserCreate,
                 session: Session = Depends(get_session),
                 current: str = Depends(get_current_user)):
    _require_admin(current)
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    user.username = body.username
    user.password_hash = hash_pw(body.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, body: UserUpdate,
                session: Session = Depends(get_session),
                current: str = Depends(get_current_user)):
    _require_admin(current)
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    if body.username:
        user.username = body.username
    if body.password:
        user.password_hash = hash_pw(body.password)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int,
                session: Session = Depends(get_session),
                current: str = Depends(get_current_user)):
    _require_admin(current)
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    session.delete(user)
    session.commit()
