from typing import Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, Delete, Update, exc
from sqlalchemy.orm import Session
from database import get_db
from datetime import date
from pydantic import BaseModel
from utils import CSVResponse, FormatType
from fastapi.responses import JSONResponse

from models import User
from schemas import TitleObject, TqueryObject, GqueryObject
from utils import authorize_user, token_dependency

router = APIRouter()

db_dependency = Annotated[Session,Depends(get_db)]

@router.get("/user-profile")
async def profile(
    user_id: token_dependency,
    db: db_dependency,
    format: FormatType = FormatType.json):
    """"Get user profile"""
    # exclude password
    user_profile = db.query(User).filter(User.id == user_id).first()
    print(f'User profile: {user_profile}')
    if user_profile==None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    else:
        return { "username" : user_profile.username, "first_name" : user_profile.first_name, "last_name" : user_profile.last_name, "email" : user_profile.email, "dob" : user_profile.dob,}

@router.post("/update-profile")
async def update_profile(
    user_id: token_dependency,
    payload : dict,
    db: db_dependency,
    format: FormatType = FormatType.json):
    """"Update user profile"""
    print(f'Payload: {payload}')
    user_profile = db.query(User).filter(User.id == user_id).first()
    print(f'User profile: {user_profile}')
    if user_profile==None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    else:
        user_profile.first_name = payload.get("first_name", user_profile.first_name)
        user_profile.last_name = payload.get("last_name", user_profile.last_name)
        user_profile.email = payload.get("email", user_profile.email)
        user_profile.dob = payload.get("dob", user_profile.dob)

        db.add(user_profile)
        db.commit()