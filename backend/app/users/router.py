from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.users.models import User, Role
from app.security import get_current_user, admin_required, hash_pw

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[User])
def list_users(session: Session = Depends(get_session),
               user: User = Depends(get_current_user)):
    return session.exec(select(User)).all()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User,
             dependencies=[Depends(admin_required)])
def create_user(data: User, session: Session = Depends(get_session)):
    if session.exec(select(User).where(User.username == data.username)).first():
        raise HTTPException(400, "Username already exists")
    new_user = User(
        username=data.username,
        password_hash=hash_pw(data.password_hash),
        role=data.role or Role.user,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.patch("/{user_id}", response_model=User,
              dependencies=[Depends(admin_required)])
def update_user(user_id: int, data: User,
                session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    if data.password_hash:
        user.password_hash = hash_pw(data.password_hash)
    if data.role:
        user.role = data.role
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.delete("/{user_id}", status_code=204,
               dependencies=[Depends(admin_required)])
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    session.delete(user)
    session.commit()
