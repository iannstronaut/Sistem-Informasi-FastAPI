# app/routers/user_router.py
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import re
import bcrypt
from models.users_model import UserBase, User
from services.database import db
from typing import Annotated
from services.auth import Token, TokenData, UserLogin, get_password_hash, authenticate_user, create_access_token, get_current_user

router = APIRouter()

db_dependency = Annotated[Session, Depends(db.get_db)]

@router.get('/', status_code=status.HTTP_200_OK)
def home():
    return { "message": "Hello You!" }

@router.post('/regist', status_code=status.HTTP_201_CREATED)
async def user_create(user: UserBase, db: db_dependency):
    try:
        if not re.match("^[a-zA-Z0-9]*$", user.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username must be alphanumeric and cannot contain special characters.")
        
        existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
        if existing_user:
            if existing_user.username == user.username:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is already taken.")
            if existing_user.email == user.email:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already in use.")

        hashed_password = get_password_hash(user.password)

        new_user = User(
            username=user.username,
            email=user.email,
            password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User created successfully", "user": new_user.username}
    except HTTPException as e:
        raise e

@router.get('/user/', status_code=status.HTTP_200_OK)
async def get_user(current_user: TokenData = Depends(get_current_user)):
    db = db_dependency
    try:
        user = db.query(User).filter(User.username == current_user.username).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return {"user_id": user.id, "username": user.username, "email": user.email}
    except HTTPException as e:
        raise e

@router.put('/user/{user_id}', status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserBase, db: db_dependency):
    try:
        existing_user = db.query(User).filter(User.id == user_id).first()

        if existing_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        if not re.match("^[a-zA-Z0-9]*$", user.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username must be alphanumeric and cannot contain special characters.")
        
        conflicting_user = db.query(User).filter(
            (User.username == user.username) | (User.email == user.email)
        ).first()
        
        if conflicting_user and conflicting_user.id != user_id:
            if conflicting_user.username == user.username:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already in use.")
            if conflicting_user.email == user.email:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use.")
        salt = bcrypt.gensalt()
        existing_user.username = user.username
        existing_user.email = user.email
        existing_user.password = bcrypt.hashpw(user.password.encode('utf-8'), salt=salt).decode('utf-8')
        
        db.commit()
        db.refresh(existing_user)
        
        return {"message": "User updated successfully",
                "user": {"email"    : existing_user.email,
                         "username" : existing_user.username}}

    except HTTPException as e:
        raise e

@router.delete('/user/{user_id}', status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: db_dependency):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        db.delete(user)
        db.commit()
        
        return {"message": "User deleted successfully"}

    except HTTPException as e:
        raise e

@router.post('/login', status_code=status.HTTP_202_ACCEPTED, response_model=Token)
async def login_user(user: UserLogin, db: db_dependency):
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username atau Password Salah")
        
        if authenticate_user(user.password, existing_user.password) is False:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username atau Password Salah")
        else:
            access_token = create_access_token(data={"sub": existing_user.username})

            return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e 