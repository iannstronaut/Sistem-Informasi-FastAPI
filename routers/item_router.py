from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
import re
from models.users_model import User
from models.items_model import Item, ItemBase
from services.database import db
from typing import Annotated
from services.auth import TokenData, get_current_user, get_password_hash, create_access_token

router = APIRouter(prefix="/api", tags=["Items Private Route"])

db_dependency = Annotated[Session, Depends(db.get_db)]

@router.get('/item/', status_code=status.HTTP_200_OK)
async def get_items_all(db: db_dependency, current_user: TokenData = Depends(get_current_user)):
    try:
        if current_user is False:
            print(current_user)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token", headers={"WWW-Authenticate": "Bearer"})
        
        item = db.query(Item).filter(Item.user_id == current_user.userId).first()
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found", headers={"WWW-Authenticate": "Bearer"})

        return item
    except HTTPException as e:
        raise e
    
@router.get('/item/{item_id}', status_code=status.HTTP_200_OK)
async def get_item(db: db_dependency, item_id: int, current_user: TokenData = Depends(get_current_user)):
    try:
        if current_user is False:
            print(current_user)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token", headers={"WWW-Authenticate": "Bearer"})
        
        item = db.query(Item).filter(Item.user_id == current_user.userId, Item.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found", headers={"WWW-Authenticate": "Bearer"})

        return item
    except HTTPException as e:
        raise e

@router.post('/item/', status_code=status.HTTP_201_CREATED)
async def item_create(item: ItemBase, db: db_dependency, current_user: TokenData = Depends(get_current_user)):
    try:
        if current_user is False:
            print(current_user)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token", headers={"WWW-Authenticate": "Bearer"})

        new_item = Item(
            title   = item.title,
            content = item.content,
            user_id = current_user.userId
        )

        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return {"message": "Item created successfully", "item": new_item.title}
    except HTTPException as e:
        raise e

@router.put('/item/{item_id}', status_code=status.HTTP_200_OK)
async def update_item(db: db_dependency, item: ItemBase, item_id: int, current_user: TokenData = Depends(get_current_user)):
    try:
        if current_user is False:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token", headers={"WWW-Authenticate": "Bearer"})
        
        existing_item = db.query(Item).filter(Item.user_id == current_user.userId, Item.id == item_id).first()

        if existing_item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

        existing_item.title = item.title
        existing_item.content = item.content
        
        db.commit()
        db.refresh(existing_item)
        
        return {"message": "Item updated successfully",
                "Item": {"Title"    : existing_item.title,
                         "Content" : existing_item.content}}

    except HTTPException as e:
        raise e

@router.delete('/item/{item_id}', status_code=status.HTTP_200_OK)
async def delete_item(db: db_dependency, item_id: int,current_user: TokenData = Depends(get_current_user)):
    try:
        if current_user is False:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token", headers={"WWW-Authenticate": "Bearer"})
        
        item = db.query(Item).filter(Item.user_id == current_user.userId, Item.id == item_id).first()
        
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        
        db.delete(item)
        db.commit()
        
        return {"message": "Item deleted successfully", "item": item.title}

    except HTTPException as e:
        raise e