from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str  = Field(index=True, unique=True)
    password_hash: str
    role: str = Field(default="user")     #  ← NEW (“admin” or “user”)
