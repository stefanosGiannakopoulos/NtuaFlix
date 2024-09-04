from fastapi import APIRouter, Depends, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text, MetaData
import codecs
from datetime import date
import pandas as pd
import io

from utils import admin_required, role_dependency
from passlib.context import CryptContext

from models import *
from database import get_db
from utils import FormatType, CSVResponse
from utils import parse_title_basics, parse_title_ratings, parse_title_principals,\
        parse_title_crew, parse_title_akas, parse_name_basics, parse_title_episode, resetall
from schemas import HealthCheckObject, ResetAllObject, UploadFileObject, UserDetails

router = APIRouter()

db_dependency = Annotated[Session,Depends(get_db)]

@router.get("/healthcheck", responses = {200: {"content": {"text/csv": {}}, "description": "CSV analogue of JSON"}})
@admin_required
async def connection_status(
    role: role_dependency, 
    db: db_dependency,
    format: FormatType = FormatType.json) -> HealthCheckObject:
    response = {"status":"failed", "dataconnection": str(db.bind.url)}
    try:
        db.execute(text('SELECT 1'))
        response["status"] = "OK"
    except Exception as e:
        pass
    finally:
        if format == FormatType.csv : return CSVResponse([HealthCheckObject.model_validate(response)])
        return response

@router.post('/resetall', responses = {200: {"content": {"text/csv": {}}, "description": "CSV analogue of JSON"}})
@admin_required
async def reset_all(
        role: role_dependency,
        db: db_dependency,
        format: FormatType = FormatType.json) -> ResetAllObject:
    """Resets database to initial state."""
    resetall(db)
    #TODO: what about failure? why would it fail in a manner that is not a bug, so that we would want the user to know?
    ret = {"status": "OK"}
    if format == FormatType.csv: return CSVResponse([ResetAllObject.model_validate(ret)])
    return ret

class UploadFileAdapter:
    def __init__(self, file):
        self.file = file
        self.decoder = codecs.getincrementaldecoder("utf-8")()

    async def read(self, n):
        data = await self.file.read(max(4,n))
        data = self.decoder.decode(data)
        return data

@router.post('/upload/titlebasics', responses = {200: {"content": {"text/csv": {}}, "description": "CSV analogue of JSON"}})
@admin_required
async def upload_title_basics(
    role: role_dependency,
    db: db_dependency,
    file: UploadFile,
    format: FormatType = FormatType.json,
    ) -> UploadFileObject:
    """Upload .tsv file for Title Basics."""
    if db.query(db.query(Title).exists()).scalar():
        ret = {"status": "failed", "reason": "Titles table is not empty."}
        if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
        return ret
    await parse_title_basics(UploadFileAdapter(file), db)
    ret = {"status": "OK"}
    if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
    return ret

@router.post('/upload/titleakas', responses = {200: {"content": {"text/csv": {}}, "description": "CSV analogue of JSON"}})
@admin_required
async def upload_title_akas(
        role: role_dependency,
        db: db_dependency,
        file: UploadFile,
        format: FormatType = FormatType.json
        ) -> UploadFileObject:
    """Upload .tsv file for Title Aliases."""
    if db.query(db.query(TitleAlias).exists()).scalar():
        ret = {"status": "failed", "reason": "Titles Alias table is not empty."}
        if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
        return ret
    await parse_title_akas(UploadFileAdapter(file), db)
    ret = {"status": "OK"}
    if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
    return ret

@router.post('/upload/namebasics', responses = {200: {"content": {"text/csv": {}}, "description": "CSV analogue of JSON"}})
@admin_required
async def upload_name_basics(
        role: role_dependency,
        db: db_dependency,
        file: UploadFile,
        format: FormatType = FormatType.json
        ) -> UploadFileObject:
    """Upload .tsv file for Name Basics."""
    if db.query(db.query(Person).exists()).scalar():
        ret = {"status": "failed", "reason": "Person table is not empty."}
        if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
        return ret
    await parse_name_basics(UploadFileAdapter(file), db)
    ret = {"status": "OK"}
    if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
    return ret

@router.post('/upload/titlecrew', responses = {200: {"content": {"text/csv": {}}, "description": "CSV analogue of JSON"}})
@admin_required
async def upload_title_crew(
        role: role_dependency,
        db: db_dependency,
        file: UploadFile,
        format: FormatType = FormatType.json
        ) -> UploadFileObject:
    """Upload .tsv file for Crew Basics."""
    if db.query(db.query(Title).join(Title.directors).exists()).scalar():
        ret = {"status": "failed", "reason": "Title Directors table is not empty."}
        if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
        return ret
    if db.query(db.query(Title).join(Title.writers).exists()).scalar():
        ret = {"status": "failed", "reason": "Title Writers table is not empty."}
        if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
        return ret
    await parse_title_crew(UploadFileAdapter(file), db)
    ret = {"status": "OK"}
    if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
    return ret

@router.post('/upload/titleepisode', responses = {200: {"content": {"text/csv": {}}, "description": "CSV analogue of JSON"}})
@admin_required
async def upload_title_episode(
        role: role_dependency,
        db: db_dependency,
        file: UploadFile,
        format: FormatType = FormatType.json
        ) -> UploadFileObject:
    """Upload .tsv file for Title Episode."""
    if db.query(db.query(TitleEpisode).exists()).scalar():
        ret = {"status": "failed", "reason": "Title Episodes table is not empty."}
        if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
        return ret
    await parse_title_episode(UploadFileAdapter(file), db)
    ret = {"status": "OK"}
    if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
    return ret


@router.post('/upload/titleprincipals', responses = {200: {"content": {"text/csv": {}}, "description": "CSV analogue of JSON"}})
@admin_required
async def upload_title_principals(
        role: role_dependency,
        db: db_dependency,
        file: UploadFile,
        format: FormatType = FormatType.json
        ) -> UploadFileObject:
    """Upload .tsv file for Title Principals."""
    if db.query(db.query(Principals).exists()).scalar():
        ret = {"status": "failed", "reason": "Principals table is not empty."}
        if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
        return ret
    await parse_title_principals(UploadFileAdapter(file), db)
    ret = {"status": "OK"}
    if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
    return ret

@router.post('/upload/titleratings', responses = {200: {"content": {"text/csv": {}}, "description": "CSV analogue of JSON"}})
@admin_required
async def upload_title_ratings(
        role: role_dependency,
        db: db_dependency,
        file: UploadFile,
        format: FormatType = FormatType.json
        ) -> UploadFileObject:
    """Upload .tsv file for Title Ratings."""
    await parse_title_ratings(UploadFileAdapter(file), db)
    ret = {"status": "OK"}
    if format == FormatType.csv: return CSVResponse([UploadFileObject.model_validate(ret)])
    return ret

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

@router.post("/usermod/{username}/{password}")
@admin_required
async def user_credentials(
    role: role_dependency, 
    db: db_dependency, 
    username: str, password: str):
    user = db.query(User).filter(User.username==username).first()
    if user:
        user.password = pwd_context.hash(password) 
        db.commit()
    else:
        new_user = User(
            username=username,
            first_name='First Name',
            last_name='Last Name',
            password=pwd_context.hash(password),
            dob=date.today(),
            is_admin=False)
        
        db.add(new_user)
        db.commit()


@router.get("/users/{username}", response_model=Optional[UserDetails])
@admin_required
async def view_user_details(
    role: role_dependency, 
    db: db_dependency, 
    username:str,
    format: FormatType = FormatType.json):
    values = db.query(User).filter(User.username==username).first()
    #if user doesnt exist returns the json null
    if format==FormatType.csv:
        values_for_csv = None
        if values:
            values_for_csv = [[values.id, values.username, values.first_name,
                              values.last_name, values.email, values.password,
                              values.dob, values.is_admin]]
    
        df = pd.DataFrame(values_for_csv,
                            columns=["id", "username", "first_name",
                                    "last_name", "email", "password",
                                    "dob", "is_admin"],)

        stream = io.StringIO()
        if values:
            df.to_csv(stream, index=False, encoding='utf-8')
        else: df.to_csv(stream, index=False, encoding='utf-8', header=None)
        response = StreamingResponse(iter([stream.getvalue()]),
                                     media_type="text/csv"
                                     )
        response.headers["Content-Disposition"] = "attachment; filename=user_details.csv"

        return response
    
    return values
