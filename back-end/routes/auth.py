from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, status, Form
from datetime import datetime, timedelta
from sqlalchemy.orm import  Session
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, constr
from models import User
from database import get_db
from datetime import date
from sqlalchemy import exc
import os
from fastapi import BackgroundTasks
from utils import check_is_adult, get_current_user, FormatType
import pandas as pd
from fastapi.responses import StreamingResponse
import io

# Authentication Router

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
FORGET_PWD_SECRET_KEY = os.getenv("FORGET_PWD_SECRET_KEY")


pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    if username and username in db:
        user_dict = db[username]
        return user_dict


def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_password_hash(password):
    return pwd_context.hash(password)


@router.post('/login')
async def login(username: Annotated[str, Form()],
                password: Annotated[str, Form()],
                db:Session = Depends(get_db),
                format: FormatType = FormatType.json):
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.password):
        token_data = {
            'username': user.username,
            'role': 'admin' if user.is_admin else 'user',
            'user_id': user.id,
            'is_adult': check_is_adult(user.dob)
        }
        token = create_jwt_token(token_data)

        if format == FormatType.csv:

            df = pd.DataFrame({'token': token}, index=[token])
            stream = io.StringIO()
            df.to_csv(stream, index=False, encoding='utf-8')
            response = StreamingResponse(iter([stream.getvalue()]),
                                     media_type="text/csv")
            response.headers["Content-Disposition"] = "attachment; filename=user_token.csv"

            return response

        return {'token': token}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )

@router.post('/logout')
async def logout(user_id: int = Depends(get_current_user)):
    pass

class UserRegisterRequirements(BaseModel):
    username: constr(min_length=4)
    first_name: constr(min_length=4)
    last_name: constr(min_length=4)
    email: EmailStr
    dob: date
    password: constr(min_length=4)
    password_confirm: constr(min_length=4)

@router.post('/register')
async def register(payload: UserRegisterRequirements, db:Session = Depends(get_db)):
    if (payload.password != payload.password_confirm):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords don't match.",
        )
    try:
        payload.password = get_password_hash(payload.password)
        new_user = User(**payload.model_dump(mode='json', exclude=['password_confirm']))
        db.add(new_user)
        db.commit()
        db.refresh
        return JSONResponse(content={"message": "This is where you register!"}, status_code=200)
    
    except exc.IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Unable to register account. Username or Email are probably being already used.'
        )


class ForgetPasswordRequest(BaseModel):
    email: str

def create_reset_password_token(email: str):
    data = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(minutes=60)
    }
    token = jwt.encode(data, FORGET_PWD_SECRET_KEY, ALGORITHM)
    return token

@router.get('/forget-password')
async def forget_password(
                email: str,
                background_tasks: BackgroundTasks,
                db: Session = Depends(get_db)
            ):
        user = db.query(User).filter_by(email = email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                  detail="Invalid Email address")
        
        # this normally would be sent in the form of a link to
        # the user's email address. For now we will print it and
        # go to the address manually.

        forget_url_token = create_reset_password_token(email)
        

        success_message = {
            'err': False,
            'msg': 'A password reset link was sent tou your email. Check your spam!',
            'forget_url_token': forget_url_token,
        }
        return JSONResponse(status_code=status.HTTP_200_OK, 
                            content=success_message)


class ResetForgetPassword(BaseModel):
    secret_token: str
    new_password: str
    confirm_password: str


def decode_reset_password_token(token: str):
    try:
        payload = jwt.decode(token, FORGET_PWD_SECRET_KEY, algorithms=[ALGORITHM])
        email = str(payload.get('email'))
        return email
    except JWTError:
        return None
        

@router.post("/reset-password")
async def reset_password(
                rfp: ResetForgetPassword,
                db: Session = Depends(get_db),
            ):
    try:
        info = decode_reset_password_token(token=rfp.secret_token)
        if info is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                   detail="Invalid Password Reset Payload or Reset Link Expired")
        if rfp.new_password != rfp.confirm_password:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                   detail="New password and confirm password are not same.")
        hashed_password = pwd_context.hash(rfp.new_password)
        user = db.query(User).filter_by(email=info).first()
        user.password = hashed_password
        db.add(user)
        db.commit()
        
        success_message = {
            'err': False,
            'msg': 'Password reset!'
        }
        return JSONResponse(status_code=status.HTTP_200_OK, 
                            content=success_message)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something unexpected happened!")
