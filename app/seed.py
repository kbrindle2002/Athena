# app/seed.py
from app.users.models import User
from app.database import engine, SQLModel
from sqlmodel import Session
from sqlmodel import select
from app.security import hash_pw


def seed():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as sess:
        if not sess.exec(select(User).where(User.username == "admin")).first():
            sess.add(User(
                username="admin",
                password_hash=hash_pw("admin"),
                role="admin",
            ))
            sess.commit()
