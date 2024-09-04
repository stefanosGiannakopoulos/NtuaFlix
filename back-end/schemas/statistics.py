from typing import Optional
from pydantic import BaseModel, Field
from datetime import date

class GenreStatistics(BaseModel):
    genre_name: str
    title_count: int

class TitleStattistics(BaseModel):
    date_posted: date
    tconst: str
    original_title: str

class ReactionStatistics(BaseModel):
    date_posted: date
    stars: int
    tconst: str
    original_title: str

class WatchlistStatistics(BaseModel):
    library_name: str
    item_count: int
    items_per_genre: list[GenreStatistics]

class OverallStatistics(BaseModel):
    total_number: int
    items_per_genre: list[GenreStatistics]

class ReviewStatistics(BaseModel):
    num_total_reviews: int
    num_total_users: int
    average_stars: Optional[float] = None
    user_num_reviews: int
    user_avg_stars: Optional[float] = None
    highest_ranking: Optional[int] = None
    lowest_ranking: Optional[int] = None
    count_most_likes: Optional[int] = None
    count_most_dislikes: Optional[int] = None
    highest_ranked_titles: list[TitleStattistics]
    lowest_ranked_titles: list[TitleStattistics]
    most_liked: list[ReactionStatistics]
    most_disliked: list[ReactionStatistics]