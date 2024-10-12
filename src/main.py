from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from typing import Annotated
from . import models
from . import database
from sqlalchemy.orm import Session
import re
import bcrypt

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

class UserBase(BaseModel):
    username    : str
    email       : EmailStr
    password    : str

class ItemBase(BaseModel):
    title       : str
    content     : str
    user_id     :int

def get_db():
   db = database.SessionLocal()
   try:
       yield db
   finally:
       db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get('/', status_code=status.HTTP_200_OK)
def home():
    return { "message": "Hello You!" }

@app.post('/user', status_code=status.HTTP_201_CREATED)
async def user_create(user: UserBase, db: db_dependency):
    # Validasi username untuk hanya mengizinkan a-z, A-Z, dan 0-9
    if not re.match("^[a-zA-Z0-9]*$", user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username must be alphanumeric and cannot contain special characters.")
    
    # Cek apakah username sudah digunakan
    existing_user = db.query(models.User).filter((models.User.username == user.username) | (models.User.email == user.email)).first()
    if existing_user:
        if existing_user.username == user.username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is already taken.")
        if existing_user.email == user.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already in use.")

    # Hash password menggunakan bcrypt
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    # Buat objek User baru
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password.decode('utf-8')  # Decode byte ke string
    )

    # Simpan user ke dalam database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user_id": new_user.id}

@app.get('/user/{user_id}', status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: db_dependency):
    # Query untuk mendapatkan user berdasarkan user_id
    user = db.query(models.User).filter(models.User.id == user_id).first()
    print(user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user
