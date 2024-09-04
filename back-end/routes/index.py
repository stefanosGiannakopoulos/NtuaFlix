from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Genre
from sqlalchemy.orm import joinedload
import json
from schemas import TitleObject
from models import Title, Genre
from sqlalchemy import func

router = APIRouter()

# Index Route File


# INEFFICIENT MUST CHANGE LATER
# @router.get('/index-movies')
# async def index(db: Session = Depends(get_db)):
#     # Assuming Genre and Title are your SQLAlchemy models
#     genres = db.query(Genre).limit(5).all()
#     movies = []

#     for genre in genres:
#         # Use joinedload to eager load the Genre relationship
#         genre_with_movies = db.query(Genre).filter_by(id=genre.id).options(joinedload(Genre.titles)).first()
        
#         if genre_with_movies:
#             # Assuming Genre.titles is the relationship between Genre and Title
#             genre_movies = genre_with_movies.titles
#             non_adult_movies = [movie for movie in genre_movies if not movie.is_adult][:20]
#             movies.append({
#                 'genre': genre.name,
#                 'genre_id': genre.id,
#                 'movies': non_adult_movies,
#             })

#     return movies
# Define a function to get genres with at least 20 non-adult movies
def get_popular_genres(db: Session):
    popular_genres = (
        db.query(Genre)
        .join(Title, Genre.titles)
        .filter(Title.is_adult.is_(False))
        .group_by(Genre.id)
        .having(func.count(Title.tconst) >= 20)
        .limit(5)
        .all()
    )
    return popular_genres

# Define a function to get 20 movies from each selected genre ordered by image_url
def get_movies_by_genre(db: Session, genre_id: int):
    movies = (
        db.query(Title)
        .join(Genre, Title.genres)
        .filter(Genre.id == genre_id, Title.is_adult.is_(False))
        .order_by(Title.image_url)
        .limit(20)
        .all()
    )
    return movies

# Create the main route
@router.get('/index-movies')
async def get_popular_movies(db: Session = Depends(get_db)):
    popular_genres = get_popular_genres(db)
    result = []

    for genre in popular_genres:
        genre_movies = get_movies_by_genre(db, genre.id)
        result.append({
            'genre': genre.name,
            'genre_id': genre.id,
            'movies': genre_movies
        })

    return result