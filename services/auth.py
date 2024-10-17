import os
from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    userId: int | None = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(plain_password):
    return pwd_context.hash(plain_password)

def authenticate_user(plain_password, hash_password):
    if not verify_password(plain_password, hash_password):
        return False
    
    return True

def create_access_token(data: dict):
    expires_delta= timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_Id: int = payload.get("userId")
        if user_Id is None:
            return False

        token_data = TokenData(userId=user_Id)
        return token_data
    except JWTError:
        return False