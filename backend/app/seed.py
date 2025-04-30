from sqlmodel import Session, select
from app.database import engine
from app.users.models import User, Role
from app.security import hash_pw
import os, sys
from sqlmodel import SQLModel

SEED_ON_STARTUP = os.getenv("SEED_ON_STARTUP", "false").lower() == "true"

def seed() -> None:
    if not SEED_ON_STARTUP:
        return
    SQLModel.metadata.create_all(engine)
    with Session(engine) as sess:
        if not sess.exec(select(User).where(User.username == "admin")).first():
            sess.add(User(
                username="admin",
                password_hash=hash_pw("admin"),
                role=Role.admin,
            ))
            sess.commit()
