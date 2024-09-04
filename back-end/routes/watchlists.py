from typing import Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy import and_, delete, exc
from sqlalchemy.orm import Session
from database import get_db
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from models import Watchlist, WatchlistContent,Title, User
from schemas import TitleObject, TqueryObject, GqueryObject
from utils import CSVResponse, FormatType

from utils import authorize_user, token_dependency


router = APIRouter()

db_dependency = Annotated[Session,Depends(get_db)]

class WatchlistObj(BaseModel):
    library_name: str
    items: int
    
#----------------> WATCHLISTS NAV <-----------------

@router.get("/watchlists/{user_id}")
@authorize_user
async def view_watchlists(
    db: db_dependency,
    user_id: int,
    session_id: token_dependency,
    format: FormatType = FormatType.json) -> list[WatchlistObj]:
    results = db.query(Watchlist).filter(Watchlist.user_id==user_id).all()
    if not results:
        raise HTTPException(status_code=204, detail=f"You haven't created any watchlist so far")
    user_libs = []
    for result in results:
        user_libs.append(WatchlistObj(library_name=result.library_name, items=result.item_count))
    if format==FormatType.csv: pass
    else: return user_libs

@router.get("/watchlists/{user_id}/{lib_name}")
@authorize_user
async def view_watchlist_contents(
    user_id:int, session_id: token_dependency, lib_name: str, db: db_dependency,
    format: FormatType = FormatType.json) -> list[TitleObject]:
    db_watchlist = db.query(Watchlist).filter(and_(Watchlist.library_name==lib_name),Watchlist.user_id==user_id).first()
    if not db_watchlist:
        raise HTTPException(status_code=404, detail=f"Watchlist {lib_name} doesn't exist")
    if db_watchlist.item_count==0 :  
        raise HTTPException(status_code=204, detail=f"Watchlist {lib_name} is empty!")    
    else:  
        watchlist_id = db_watchlist.id
        contents = []
        results = db.query(Title).join(WatchlistContent).filter(WatchlistContent.watchlist_id==watchlist_id).all()
        for result in results:
            contents.append(result)   
        if format==FormatType.csv: pass
        else: return contents
 


@router.post("/watchlists/{user_id}/create")
@authorize_user
async def create_watchlist(lib_name: str, user_id: int, session_id: token_dependency, db: db_dependency, contents: list[TitleObject] = []):
    db_watchlist = Watchlist(library_name = lib_name, item_count = 0, user_id=user_id)
    try:
        db.add(db_watchlist)
        db.commit()
        db.refresh
        if contents is not []:
            for content in contents:
                db_content = WatchlistContent(watchlist_id=db_watchlist.id, title_id=content.tconst)
                db.add(db_content)
                db_watchlist.item_count+=1
            db.commit()
            db.refresh
        return JSONResponse(content={"message": "New Watchlist added successfully!"}, status_code=200)
    except exc.IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Unable to create watchlist. Maybe {lib_name} already exists!')



        
        
@router.delete("/watchlists/{user_id}/{lib_name}")  
@authorize_user            
async def remove_watchlist(lib_name: str, user_id: int, session_id: token_dependency, db: db_dependency):
    db_watchlist = db.query(Watchlist).filter(and_(Watchlist.library_name == lib_name),Watchlist.user_id==user_id).first()
    if not db_watchlist:
        raise HTTPException(status_code=404, detail=f"You have not created a watchlist with name {lib_name}")
    watchlist_id = db_watchlist.id
    #remove references 
    db.query(WatchlistContent).filter(WatchlistContent.watchlist_id == watchlist_id).delete()
    #trigger for item_count-=1 not needed as watchlist will be finally completely removed 
    db.commit()
    #remove watchlist
    db.delete(db_watchlist)
    db.commit()
    return JSONResponse(content={"message": " Watchlist removed successfully!"}, status_code=200)
 
@router.post("/watchlists/{user_id}/{lib_name}/add")
@authorize_user 
async def add_contents(user_id: int, lib_name: str,  movie_tconst: str, session_id: token_dependency, db: db_dependency):
    db_watchlist = db.query(Watchlist).filter(and_(Watchlist.library_name == lib_name),Watchlist.user_id==user_id).first()
    watchlist_id = db_watchlist.id
    db_movie = db.query(Title).filter(Title.tconst==movie_tconst).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail=f"This movie doesnt't exist")
    db_link = WatchlistContent(title_id=movie_tconst, watchlist_id=watchlist_id)
    try:
        db.add(db_link)
        db.commit()
        db.refresh
        return JSONResponse(content={"message": " movie added successfully!"}, status_code=200)
    except exc.IntegrityError as e:
        db.rollback()
        error_msg = {
            'error': True,
            'msg': 'This movies is already in the watchlist.' # probably :)
        }
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_msg)
 
        
@router.delete("/watchlists/{user_id}/{lib_name}/remove") 
@authorize_user 
async def remove_contents(movie_tconst: str, lib_name: str, db: db_dependency, user_id: int, session_id: token_dependency):
    db_watchlist = db.query(Watchlist).filter(and_(Watchlist.library_name == lib_name),Watchlist.user_id==user_id).first()
    watchlist_id = db_watchlist.id

    db_link = db.query(WatchlistContent).filter(and_(WatchlistContent.title_id==movie_tconst),WatchlistContent.watchlist_id==watchlist_id).first()
    if db_link:
        db.delete(db_link)
    else:
        raise HTTPException(status_code=400, detail=f"Movie {movie_tconst} is not in this watchlist")
    db.commit()
    return JSONResponse(content={"message": " Movie removed successfully from watchlist!"}, status_code=200)
    
