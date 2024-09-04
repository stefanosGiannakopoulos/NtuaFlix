from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date

class HealthCheckObject(BaseModel):
    status: str
    dataconnection: str

class ResetAllObject(BaseModel):
    status: str

class UploadFileObject(BaseModel):
    status: str
    reason: Optional[str] = None

class UserDetails(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    password: str
    dob: date
    is_admin: bool