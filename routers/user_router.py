from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
import re
import bcrypt
from models.users_model import UserBase, User
from services.database import db
from typing import Annotated
from services.auth import TokenData, get_current_user, get_password_hash, create_access_token

router = APIRouter(prefix="/api")

db_dependency = Annotated[Session, Depends(db.get_db)]

@router.get('/user/', status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency, current_user: TokenData = Depends(get_current_user)):
    try:
        if current_user is False:
            print(current_user)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token", headers={"WWW-Authenticate": "Bearer"})
        
        user = db.query(User).filter(User.id == current_user.userId).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found", headers={"WWW-Authenticate": "Bearer"})

        return {"user_id": user.id, "fullname": user.fullname ,"username": user.username, "email": user.email}
    except HTTPException as e:
        raise e

@router.put('/user/', status_code=status.HTTP_200_OK)
async def update_user(db: db_dependency, user: UserBase, current_user: TokenData = Depends(get_current_user)):
    try:
        if current_user is False:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token", headers={"WWW-Authenticate": "Bearer"})
        
        existing_user = db.query(User).filter(User.id == current_user.userId).first()

        if existing_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        if not re.match("^[a-zA-Z0-9.]*$", user.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username must be alphanumeric and cannot contain special characters.")
        
        conflicting_user = db.query(User).filter(
            (User.username == user.username) | (User.email == user.email)
        ).first()
        
        if conflicting_user and conflicting_user.id != existing_user.id:
            if conflicting_user.username == user.username:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already in use.")
            if conflicting_user.email == user.email:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use.")

        existing_user.username = user.username
        existing_user.fullname = user.fullname
        existing_user.email = user.email
        existing_user.password = get_password_hash(user.password)
        
        db.commit()
        db.refresh(existing_user)
        
        return {"message": "User updated successfully",
                "user": {"email"    : existing_user.email,
                         "username" : existing_user.username,
                         "fullname" : existing_user.fullname}}

    except HTTPException as e:
        raise e

@router.delete('/user/', status_code=status.HTTP_200_OK)
async def delete_user(db: db_dependency, current_user: TokenData = Depends(get_current_user)):
    try:
        if current_user is False:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token", headers={"WWW-Authenticate": "Bearer"})
        
        user = db.query(User).filter(User.id == current_user.userId).first()
        
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        db.delete(user)
        db.commit()
        
        return {"message": "User deleted successfully", "user": user.username}

    except HTTPException as e:
        raise e