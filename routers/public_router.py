from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
import re
from models.users_model import UserBase, User
from services.database import db
from typing import Annotated
from services.auth import Token, UserLogin, get_password_hash, authenticate_user, create_access_token, get_current_user

router = APIRouter()

db_dependency = Annotated[Session, Depends(db.get_db)]

@router.get('/', status_code=status.HTTP_200_OK)
def home():
    return { "message": "Hello You!" }

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def user_create(user: UserBase, db: db_dependency):
    try:
        if not re.match("^[a-zA-Z0-9.]*$", user.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username must be alphanumeric and cannot contain special characters.")
        
        existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
        if existing_user:
            if existing_user.username == user.username:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is already taken.")
            if existing_user.email == user.email:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already in use.")
        
        if len(user.password) < 6:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must contain 6 Letter or Numbers")
        
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
    
@router.post('/login', status_code=status.HTTP_202_ACCEPTED, response_model=Token)
async def login_user(user: UserLogin, db: db_dependency):
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username atau Password Salah", headers={"WWW-Authenticate": "Bearer"})
        
        if authenticate_user(user.password, existing_user.password) is False:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username atau Password Salah", headers={"WWW-Authenticate": "Bearer"})
        else:
            access_token = create_access_token(data={"sub": existing_user.username})

            return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e 