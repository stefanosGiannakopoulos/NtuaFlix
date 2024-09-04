from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from functools import wraps
from typing import Annotated, Optional
from .oauth2_custom import OAuth2PasswordCustomHeader 

oauth2_scheme = OAuth2PasswordCustomHeader(tokenUrl="token", header_name="X-OBSERVATORY-AUTH")
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user_id
        

token_dependency = Annotated[int ,Depends(get_current_user)]

def authorize_user(func):
    @wraps(func)
    async def wrapper(*args, user_id: int, session_id: token_dependency, **kwargs):
        if user_id == None: 
            raise credentials_exception
        if user_id != session_id:
            raise HTTPException(status_code=401, detail="Permission denied: Cross user validation failed")
        return await func(*args, user_id=user_id, session_id=session_id, **kwargs)
    return wrapper


#admin validation
  
def get_user_role(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        role: str = payload.get("role")
        if role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return role

role_dependency = Annotated[str, Depends(get_user_role)]

def admin_required(func):
    @wraps(func)
    async def admin_wrapper(*args, role:role_dependency, **kwargs):
        if (role!="admin") :
            raise HTTPException(status_code=401, detail=f"Permission Denied: Only admin can access this source!")
        return await func(*args, role=role, **kwargs)
    return admin_wrapper
 
 
#   is_adult validation

def get_user_is_adult(token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    is_adult = False
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        is_adult: bool = payload.get("is_adult", False)
    except JWTError as e:
        pass
    return is_adult

is_adult_dependency = Annotated[bool, Depends(get_user_is_adult)]
