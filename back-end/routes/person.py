from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from models import Person, Principals, Title
from schemas import NameObject, NqueryObject
from utils import CSVResponse, FormatType
from sqlalchemy.orm import joinedload

router = APIRouter()

@router.get("/name/{nameID}", responses = {200: {"content": {"text/csv": {}}, "description": "CSV analogue of JSON"}})
async def get_person(
        nameID: str,
        format: FormatType = FormatType.json,
        db: Session = Depends(get_db)) -> Optional[NameObject]:
    person = db.query(Person).filter_by(nconst=nameID).first()
    if format == FormatType.csv: return CSVResponse([NameObject.model_validate(person)] if person is not None else [])
    return person

@router.get("/searchname", responses = {200: {"content": {"text/csv": {}}, "description": "CSV analogue of JSON"}})
@router.post("/searchname", responses = {200: {"content": {"text/csv": {}}, "description": "CSV analogue of JSON"}})
async def search_person_name(
        query: NqueryObject,
        format: FormatType = FormatType.json,
        db: Session = Depends(get_db)) -> list[NameObject]:
    people = db.query(Person).filter(Person.primary_name.contains(query.namePart))
    if format == FormatType.csv: return CSVResponse(map(NameObject.model_validate, people))
    return people

@router.get('/name_whole/{nameID}')
async def get_person_name(
        nameID: str,
        format: FormatType = FormatType.json,
        db: Session = Depends(get_db)):
    person = (
        db.query(Person)
        .filter(Person.nconst == nameID)
        .options(joinedload(Person.titles_as_principal).joinedload(Principals.title))
        .first()
    )

    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")

    # Convert the person and titles to dictionaries
    person_info = {
        "nconst": person.nconst,
        "image_url": person.image_url,
        "primary_name": person.primary_name,
        "birth_year": person.birth_year,
        "death_year": person.death_year,
        "profession": person.primary_professions,
        "titles_participated": [
            {
                "title_id": title.title.tconst,
                "title_name": title.title.primary_title,
                "image_url": title.title.image_url,
                "end_year": title.title.end_year,
                "average_rating": title.title.average_rating,
            }
            for title in person.titles_as_principal
        ],
    }

    return person_info
