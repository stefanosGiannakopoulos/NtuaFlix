import pandas as pd 
from typing import Annotated
from sqlalchemy import create_engine, exc, text
from sqlalchemy.orm import Session, sessionmaker
from fastapi import Depends,HTTPException,status
from models import User, Watchlist, WatchlistContent, Review, ReviewReactions  
from passlib.context import CryptContext
import asyncio
from database import get_db
import random 

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
db_dependency = Annotated[Session,Depends(get_db)]

#change titlr_id to be valid... chatGPT messed this up
"""
titles = pd.read_csv("truncated_data/truncated_title.basics.tsv", sep='\t')
tconst_to_title_id = list(titles['tconst'])

reviews = pd.read_csv("mock_data/mock_reviews.csv")
for index, row in reviews.iterrows():
    reviews.at[index, 'title_id'] = random.choice(tconst_to_title_id)
    
print ("saving updating values")
reviews.to_csv("mock_data/mock_reviews.csv", index=False)

watchlist_content = pd.read_csv("mock_data/mock_watchlist_contents.csv")
for index, row in watchlist_content.iterrows():
    watchlist_content.at[index, 'title_id'] = random.choice(tconst_to_title_id)
    
print ("saving updating values")
watchlist_content.to_csv("mock_data/mock_watchlist_contents.csv", index=False)
"""


def user_parser(users, db: db_dependency):
    for index, row in users.iterrows():
        user_data = {
            'id': row["id"],
            'username': row["username"],
            'first_name': row["first_name"],
            'last_name': row["last_name"],
            'email': row["email"],
            'password': pwd_context.hash(row["password"]),
            'dob': row["dob"],
            'is_admin': row["is_admin"]
        }
        user = User(**user_data)
        try:
            db.add(user)
            db.commit()
            db.refresh
        except exc.IntegrityError as e:
            db.rollback()
            print(f"Unable to insert user {user.id}")
            
def watchlist_parser(watchlist, db:db_dependency):
    for index, row in watchlist.iterrows():
        watchlist_data = {
            'id': row["id"],
            'library_name': row["library_name"],
            'item_count': 0,
            'user_id': row["user_id"]
        }
        watchlist = Watchlist(**watchlist_data)

        try:
            db.add(watchlist)
            db.commit()
            db.refresh
        except exc.IntegrityError as e:
            db.rollback()
            print(f"Unable to insert watchlist {watchlist.id}")
            
def watchlist_content_parser(watchlist_contents, db:db_dependency):
    for index, row in watchlist_contents.iterrows():
        content_data = {
            'id': row["id"],
            'watchlist_id': row["watchlist_id"],
            'title_id': row["title_id"]
        }
        watchlist_content = WatchlistContent(**content_data)
        try:
            db.add(watchlist_content)
            db.commit()
            db.refresh
        except exc.IntegrityError as e:
            db.rollback()
            print(f"Unable to insert watchlist content with id = {watchlist_content.id}")
            
def review_parser(reviews, db:db_dependency):
    for index,row in reviews.iterrows():
        review_data = {
            'id': row["id"],
            'text': row["text"],
            'stars': row["stars"],
            'likes': 0,
            'dislikes':0,
            'date': row["date"],
            'title_id': row["title_id"],
            'user_id': row["user_id"]      
        }
        review = Review(**review_data)
        try:
            db.add(review)
            db.commit()
            db.refresh
        except exc.IdentifierError as e:
            db.rollback()
            print(f"Unable to insert review with id = {review.id}")
            
def review_reaction_parser(review_reactions, db: db_dependency):
    for index, row in review_reactions.iterrows():
        reaction_data = {
        'id': row["id"],
        'type': bool(row["type"]),
        'user_id': row["user_id"],
        'review_id': row["review_id"]
        }
        rev_reaction = ReviewReactions(**reaction_data)
        try:
            db.add(rev_reaction)
            db.commit()
            db.refresh
        except exc.IntegrityError as e:
            db.rollback()
            print(f"Unable to insert reaction with id = {rev_reaction.id}")
            
          
async def main():
    db=next(get_db())
    users = pd.read_csv("mock_data/mock_users.csv")
    watchlists = pd.read_csv("mock_data/mock_watchlists.csv")
    watchlist_contents = pd.read_csv("mock_data/mock_watchlist_contents.csv")
    reviews = pd.read_csv("mock_data/mock_reviews.csv")
    review_reactions = pd.read_csv("mock_data/mock_review_reactions.csv")

    user_parser(users, db)
    watchlist_parser(watchlists,db)
    watchlist_content_parser(watchlist_contents, db)
    review_parser(reviews, db)
    review_reaction_parser(review_reactions, db)

    #Restart auto_increments so that no integrity error occurs when trying to insert from the app
    sql = f"SELECT setval('user_id_seq', (SELECT MAX(id) FROM users) + 1);"
    db.execute(text(sql))
    sql = f"SELECT setval('watchlist_id_seq', (SELECT MAX(id) FROM watchlists) + 1);"
    db.execute(text(sql))
    sql = f"SELECT setval('watchlist_content_id_seq', (SELECT MAX(id) FROM watchlist_content) + 1);"
    db.execute(text(sql))
    sql = f"SELECT setval('review_id_seq', (SELECT MAX(id) FROM reviews) + 1);"
    db.execute(text(sql))
    sql = f"SELECT setval('review_reactions_id_seq', (SELECT MAX(id) FROM reviews_reactions) + 1);"
    db.execute(text(sql))
    
    
asyncio.run(main())
print("Mock Data import complete.")


