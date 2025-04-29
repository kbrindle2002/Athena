from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "CHANGE_ME_IN_PROD"
ALGORITHM = "HS256"
ACCESS_EXPIRES_MIN = 30

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pw(password: str) -> str:
    return pwd_ctx.hash(password)

def verify_pw(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)

def create_token(sub: str) -> str:
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRES_MIN)
    return jwt.encode({"sub": sub, "exp": exp}, SECRET_KEY, algorithm=ALGORITHM)
from jose import JWTError, jwt
from fastapi import Header, HTTPException

# ... SECRET_KEY, ALGORITHM, etc. already defined above ...

def get_current_user(authorization: str = Header(...)):
    try:
        scheme, _, token = authorization.partition(" ")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
