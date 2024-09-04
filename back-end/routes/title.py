from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func 
from database import get_db
from typing import Union, List
from pydantic import BaseModel
from models import Title, Genre
from schemas import TitleObject, TqueryObject, GqueryObject
from utils import CSVResponse, FormatType, is_adult_dependency
from math import ceil

router = APIRouter()

@router.get("/title/{titleID}", responses = {200: {"content": {"text/csv": {}}, "description": "CSV analogue of JSON"}})
async def get_title(
        titleID: str,
        format: FormatType = FormatType.json,
        db: Session = Depends(get_db)
        ) -> Optional[TitleObject]:
    title = db.query(Title).filter_by(tconst=titleID).first()
    if not title:
        raise HTTPException(status_code=404, detail=f"Movie with tconst {titleID} doesn't exist")
    if format == FormatType.csv: return CSVResponse([TitleObject.model_validate(title)] if title is not None else [])
    return title

@router.get("/searchtitle", responses = {200: {"content": {"text/csv": {}}, "description": "CSV analogue of JSON"}})
@router.post("/searchtitle", responses = {200: {"content": {"text/csv": {}}, "description": "CSV analogue of JSON"}})
async def search_title_name(
        query: TqueryObject,
        format: FormatType = FormatType.json,
        db: Session = Depends(get_db)) -> list[TitleObject]:
    titles = db.query(Title).filter(Title.original_title.contains(query.titlePart)).all()
    if titles==[]:
        raise HTTPException(status_code=204, detail=f"titlePart didn't match!")
    if format == FormatType.csv: return CSVResponse(map(TitleObject.model_validate, titles))
    return titles

@router.get("/bygenre", responses = {200: {"content": {"text/csv": {}}, "description": "CSV analogue of JSON"}})
async def search_title_genre(
        query: GqueryObject,
        format: FormatType = FormatType.json,
        db: Session = Depends(get_db)) -> list[TitleObject]:
    titles = db.query(Title).filter(Title.genres.any(name=query.qgenre)).filter(Title.average_rating >= query.minrating)
    if query.yrFrom is not None and query.yrTo is not None:
        titles = titles.filter(query.yrFrom <= Title.start_year).filter(Title.start_year <= query.yrTo)
    if format == FormatType.csv: return CSVResponse(map(TitleObject.model_validate, titles))
    return titles


class GetMoviesResponse(BaseModel):
    titles: List[TitleObject]
    total_pages: int

TITLES_PER_PAGE = 15
TITLES_PER_PAGE_SEARCH = 8
@router.get('/search-titles-autocomplete')
async def search_titles_autocomplete(
                    is_adult: is_adult_dependency,
                    search_title: str,
                    db: Session = Depends(get_db)) -> list[TitleObject]:
    titles = db.query(Title).filter(Title.original_title.ilike(f"%{search_title}%"))
    if not is_adult:
        titles = titles.filter_by(is_adult=False)
    return titles.limit(TITLES_PER_PAGE_SEARCH)

@router.get("/get-movies", response_model=GetMoviesResponse)
async def get_movies(is_adult: is_adult_dependency,
                     page: int or None = 1, 
                     qgenre: Union[int, None] = Query(None, alias="qgenre"), 
                     db: Session = Depends(get_db)):    
    titles = db.query(Title).order_by(Title.image_url)
    
    if qgenre:
        titles = titles.filter(Title.genres.any(id=qgenre))
    
    if not is_adult:
        titles = titles.filter(Title.is_adult == False)

    total_titles = titles.count()
    total_pages = ceil(total_titles / TITLES_PER_PAGE)
    
    titles = titles.offset((page-1) * TITLES_PER_PAGE).limit(TITLES_PER_PAGE)
    return {"titles": titles, "total_pages": total_pages}

@router.get('/get-genres')
async def get_genres(db:Session =  Depends(get_db)):
    genres = db.query(Genre).all()
    return genres

@router.get("/recommend-movie")
async def recommend_movie(is_adult: is_adult_dependency, db: Session = Depends(get_db)) -> TitleObject:
    count_query = db.query(func.count(Title.tconst)).filter(Title.image_url != None)
    if not is_adult:
        count_query = count_query.filter_by(is_adult = False)
    
    total_count = count_query.scalar()
    random_index = func.floor(func.random() * total_count)
    random_title_query = db.query(Title).filter(Title.image_url != None)

    if not is_adult:
        random_title_query = random_title_query.filter_by(is_adult = False) 

    random_title = random_title_query.offset(random_index).limit(1).first()

    return random_title
