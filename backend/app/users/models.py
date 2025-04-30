from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field

class Role(str, Enum):
    admin = "admin"
    user  = "user"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str     = Field(index=True, unique=True)
    password_hash: str
    role: Role        = Field(default=Role.user)
