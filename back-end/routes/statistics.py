from fastapi import APIRouter, Depends
from schemas import WatchlistStatistics, OverallStatistics, ReviewStatistics
from sqlalchemy import distinct, text
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from database import engine, get_db
from utils import FormatType, token_dependency
import pandas as pd
from fastapi.responses import StreamingResponse
import io
from starlette import status
from models import WatchlistContent, Title, Watchlist, Review

router = APIRouter()

# Τα endpoints /user_stats_watchlists και /top_genres_overall είναι για τη
# λειτουργική απαίτηση του requirements workshop 2023:
# "Υπολογισμός προφιλ χρηστη με βαση τις ταινιες που αυτος εχει ηδη δει.
# Πχ στο προφιλ αρεσουν 20% ταινιες δρασης, 15% θριλερ, 40% κωμωδίες κτλ."

@router.get("/user_stats_watchlists", response_model=list[WatchlistStatistics], status_code=status.HTTP_200_OK)
async def genres_per_watchlist(user_id: token_dependency,
                               format: FormatType = FormatType.json):
    
    query = f"""select watchlists.library_name, watchlists.item_count, genre_name, title_count
            from (
                select watchlists.id as w_id, genre.name as genre_name, count(genre.id) as title_count
                from genre
                inner join title_genre on title_genre.genre = genre.id
                inner join watchlist_content on watchlist_content.title_id = title_genre.tconst
                inner join watchlists on watchlists.id = watchlist_content.watchlist_id
                where watchlists.user_id = {user_id}
                group by genre.id, watchlists.id
                ) as subquery
            inner join watchlists on watchlists.id = w_id
            order by watchlists.library_name asc, title_count desc, genre_name asc;
        """
        
    with engine.connect() as connection:
        result = connection.execute(text(query))
        connection.close()
    
    if format == FormatType.csv:

        df = pd.DataFrame(result, columns=["Your Library Name",
                                           "Number of Titles in the Library",
                                           "Genre",
                                           "Number of Titles Belonging to Genre"])
        stream = io.StringIO()
        df.to_csv(stream, index=False, encoding='utf-8')
        response = StreamingResponse(iter([stream.getvalue()]),
                                     media_type="text/csv"
                                     )
        response.headers["Content-Disposition"] = "attachment; filename=statistics_per_watchlist.csv"

        return response

    WatchlistsStatistics_json = []
    GenreStatistics_json = []
    prev_row = None

    for row in result:

        if prev_row is None or prev_row.library_name == row.library_name:
            GenreStatistics_json.append(
                {
                    "genre_name": row.genre_name,
                    "title_count": row.title_count
                })
            prev_row = row
        else:
            WatchlistsStatistics_json.append(
                {
                    "library_name": prev_row.library_name,
                    "item_count": prev_row.item_count,
                    "items_per_genre": GenreStatistics_json
                })
            GenreStatistics_json = [
                {
                    "genre_name": row.genre_name,
                    "title_count": row.title_count
                }
            ]
            prev_row = None

    # Append the last WatchlistsStatistics Object after the loop
    if prev_row is not None:
        WatchlistsStatistics_json.append(
            {
                "library_name": prev_row.library_name,
                "item_count": prev_row.item_count,
                "items_per_genre": GenreStatistics_json
            })

    return WatchlistsStatistics_json


@router.get('/top_genres_overall', response_model=OverallStatistics, status_code=status.HTTP_200_OK)
async def genres_overall(user_id: token_dependency,
                               format: FormatType = FormatType.json):
    
    query_top_genres = f"""select genre.name as genre_name, count(genre.id) as title_count
                    from genre
                    inner join title_genre on title_genre.genre = genre.id
                    inner join watchlist_content on watchlist_content.title_id = title_genre.tconst
                    inner join watchlists on watchlists.id = watchlist_content.watchlist_id
                    where watchlists.user_id = {user_id}
                    group by genre.id
                    order by title_count desc, genre_name asc
                """
    
    query_total_number = f"""select sum(item_count) as total_number
                        from watchlists
                        where user_id = {user_id}
                        group by user_id;
                    """

    with engine.connect() as connection:
        result_top_genres = connection.execute(text(query_top_genres))
        result_total_number = connection.execute(text(query_total_number))
        connection.close()
    
    row_total_number = result_total_number.fetchone()
    if row_total_number is None:
        total_number = 0
    else:
        total_number = row_total_number.total_number

    if format == FormatType.csv:
        # Dataframe containing only the top genres
        df = pd.DataFrame(result_top_genres, columns=["Genre",
                                                      "Total Number of Titles Belonging to Genre"])

        # Create a column containing the result_total_number to insert into the dataframe
        df.insert(0, "Total Number of Titles in All Libraries", total_number, True)

        stream = io.StringIO()
        df.to_csv(stream, index=False, encoding='utf-8')
        response = StreamingResponse(iter([stream.getvalue()]),
                                     media_type="text/csv"
                                     )
        response.headers["Content-Disposition"] = "attachment; filename=top_genres_overall.csv"

        return response
    
    GenreStatistics_json = []

    for row in result_top_genres:
        GenreStatistics_json.append({
            "genre_name": row.genre_name,
            "title_count": row.title_count
        })

    OverallStatistics_json = {
        "total_number": total_number,
        "items_per_genre": GenreStatistics_json
    }

    return OverallStatistics_json


# This endpoint returns the number of users having added the
# title to one of their watchlists and the number of watchlists
# containing a specific title

@router.get('/number_watchlists_title/{titleID}', status_code=status.HTTP_200_OK)
async def num_of_watchlists_containing_title(titleID: str,
                                                format: FormatType = FormatType.json,
                                                db: Session = Depends(get_db)):
    
    title = db.query(Title).get(titleID)

    if title is None:
        if format == FormatType.csv:
            df = pd.DataFrame()
            stream = io.StringIO()
            df.to_csv(stream, index=False, encoding='utf-8', header=None)
            response = StreamingResponse(iter([stream.getvalue()]),
                                     media_type="text/csv")
            response.headers["Content-Disposition"] = "attachment; filename=num_of_watchlists_containing_title.csv"

            return response
        return None

    watchlist = (db.query(func.count(WatchlistContent.title_id))
                .filter(WatchlistContent.title_id == titleID).scalar())
    
    users = (db.query(func.count(distinct(Watchlist.user_id)))
             .join(WatchlistContent, WatchlistContent.watchlist_id == Watchlist.id)
             .filter(WatchlistContent.title_id == titleID).scalar())

    result_watchlists = 0
    result_users = 0
    if watchlist: result_watchlists = watchlist
    if users: result_users = users

    if format == FormatType.csv:
        df = pd.DataFrame({'tconst': titleID,
                           'Original Title': title.original_title,
                           'Number of Watchlists Containing Title': result_watchlists,
                           'Number of Users who have added the Title to their Watchlists': result_users},
                           index=[titleID])
        stream = io.StringIO()
        df.to_csv(stream, index=False, encoding='utf-8')
        response = StreamingResponse(iter([stream.getvalue()]),
                                     media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=num_of_watchlists_containing_title.csv"

        return response

    return {"tconst": titleID, "num_of_watchlists" : result_watchlists, "num_of_users": result_users}


# Some statistics based on the user's reviews

@router.get('/user_stats_reviews', response_model=ReviewStatistics, status_code=status.HTTP_200_OK)
async def reviews_statistics(user_id: token_dependency,
                             format: FormatType = FormatType.json,
                             db: Session = Depends(get_db)):

    # Find the total number of reviews posted and the number of users who have posted them
    result = db.query(func.count(Review.id), func.count(distinct(Review.user_id))).first()
    num_total_reviews = 0
    num_total_users = 0
    if result:
        num_total_reviews, num_total_users = result 
    
    # Find the average number of stars in all the reviews
    result = db.query(func.avg(Review.stars)).scalar()
    avg_stars_all = None
    if result:
        avg_stars_all = round(result, 1)

    # Find the total number of reviews the user has posted
    result = (db.query(func.count(Review.id))
               .filter(Review.user_id == user_id).scalar())
    
    user_num_reviews = 0
    if result:
        user_num_reviews = result

    # Find the average number of stars in all the reviews
    # posted by the current user
    result = (db.query(func.avg(Review.stars))
               .group_by(Review.user_id)
               .filter(Review.user_id == user_id).scalar())
    
    user_avg_stars_all = None
    if result: user_avg_stars_all = round(result, 1)
    
    # Find the titles the user has given the highest rating
    result = (db.query(Review.title_id, Title.original_title, Review.date, Review.stars)
               .join(Title, Title.tconst == Review.title_id)
               .filter(Review.user_id == user_id)
               .order_by(Review.stars.desc(), Review.date.asc(), Title.original_title.asc()))
    
    highest_ranking = None
    highest_ranked_titles = []
    if result:
        for row in result:
            if highest_ranking is None:
                highest_ranking = row.stars
            if highest_ranking and row.stars == highest_ranking:
                highest_ranked_titles.append({
                    "date_posted": row.date,
                    "tconst": row.title_id,
                    "original_title": row.original_title
                })
            else: break

    # Find the titles the user has given the lowest rating
    result = (db.query(Review.title_id, Title.original_title, Review.date, Review.stars)
               .join(Title, Title.tconst == Review.title_id)
               .filter(Review.user_id == user_id)
               .order_by(Review.stars.asc(), Review.date.asc(), Title.original_title.asc()))
    
    lowest_ranking = None
    lowest_ranked_titles = []
    if result:
        for row in result:
            if lowest_ranking is None:
                lowest_ranking = row.stars
            if lowest_ranking and row.stars == lowest_ranking:
                lowest_ranked_titles.append({
                    "date_posted": row.date,
                    "tconst": row.title_id,
                    "original_title": row.original_title
                })
            else: break

    # Find the user's reviews that have received the most likes
    result = (db.query(Review.likes, Review.stars, Review.title_id, Title.original_title, Review.date)
               .join(Title, Title.tconst == Review.title_id)
               .filter(Review.user_id == user_id)
               .order_by(Review.likes.desc(), Review.date.asc(), Title.original_title.asc()))
    
    count_likes = None
    most_liked_reviews = []
    if result:
        for row in result:
            if row.likes and row.likes == 0:
                break
            if count_likes is None and row.likes:
                count_likes = row.likes
            if row.likes and row.likes == count_likes:
                most_liked_reviews.append({
                    "date_posted": row.date,
                    "stars": row.stars,
                    "tconst": row.title_id,
                    "original_title": row.original_title
                })
            else: break

    # Find the user's reviews that have received the most dislikes
    result = (db.query(Review.dislikes, Review.stars, Review.title_id, Title.original_title, Review.date)
               .join(Title, Title.tconst == Review.title_id)
               .filter(Review.user_id == user_id)
               .order_by(Review.dislikes.desc(), Review.date.asc(), Title.original_title.asc()))
    
    count_dislikes = None
    most_disliked_reviews = []
    if result:
        for row in result:
            if row.dislikes and row.dislikes == 0:
                break
            if count_dislikes is None and row.dislikes:
                count_dislikes = row.dislikes
            if row.dislikes and row.dislikes == count_dislikes:
                most_disliked_reviews.append({
                    "date_posted": row.date,
                    "stars": row.stars,
                    "tconst": row.title_id,
                    "original_title": row.original_title
                })
            else: break
    
    if format == FormatType.csv:
        stream = io.StringIO()

        general_stats_df = pd.DataFrame({'Total number of Reviews': num_total_reviews,
                                         'Number of Users Who Have Posted Reviews': num_total_users,
                                         'Average User Rating (out of 5)': avg_stars_all,
                                         'The Number of The Reviews You Have Posted': user_num_reviews,
                                         'Your Average Rating (out of 5)': user_avg_stars_all},
                                         index=[num_total_reviews])
        
        general_stats_df.to_csv(stream, index=False, encoding='utf-8')
        
        if highest_ranked_titles:
            highest_ranked_titles_df = (pd.DataFrame(highest_ranked_titles)
                                    .rename(columns={'date_posted': 'Date Posted',
                                                     'original_title': 'Your Highest Rated Titles'}))
            highest_ranked_titles_df.insert(0, "Stars (out of 5)", highest_ranking, True)
            highest_ranked_titles_df.to_csv(stream, index=False, encoding='utf-8')

        if lowest_ranked_titles:
            lowest_ranked_titles_df = (pd.DataFrame(lowest_ranked_titles)
                                    .rename(columns={'date_posted': 'Date Posted',
                                                     'original_title': 'Your Lowest Rated Titles'}))
            lowest_ranked_titles_df.insert(0, "Stars (out of 5)", lowest_ranking, True)
            lowest_ranked_titles_df.to_csv(stream, index=False, encoding='utf-8')

        if most_liked_reviews:
            most_liked_reviews_df = (pd.DataFrame(most_liked_reviews)
                                 .rename(columns={'date_posted': 'Date Posted',
                                                  'stars': 'Stars (out of 5)',
                                                  'original_title': 'Titles You Reviewed And Received the Most Likes'}))
            most_liked_reviews_df.insert(0, "Likes", count_likes, True)
            most_liked_reviews_df.to_csv(stream, index=False, encoding='utf-8')

        if most_disliked_reviews:
            most_disliked_reviews_df = (pd.DataFrame(most_disliked_reviews)
                                 .rename(columns={'date_posted': 'Date Posted',
                                                  'stars': 'Stars (out of 5)',
                                                  'original_title': 'Titles You Reviewed And Received the Most Disikes'}))
            most_disliked_reviews_df.insert(0, "Dislikes", count_dislikes, True)
            most_disliked_reviews_df.to_csv(stream, index=False, encoding='utf-8') 

        response = StreamingResponse(iter([stream.getvalue()]),
                                     media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=user_reviews_stats.csv"

        return response

    return {
                "num_total_reviews": num_total_reviews,
                "num_total_users": num_total_users,
                "average_stars": avg_stars_all,
                "user_num_reviews": user_num_reviews,
                "user_avg_stars": user_avg_stars_all,
                "highest_ranking": highest_ranking,
                "lowest_ranking": lowest_ranking,
                "count_most_likes": count_likes,
                "count_most_dislikes": count_dislikes,
                "highest_ranked_titles": highest_ranked_titles,
                "lowest_ranked_titles": lowest_ranked_titles,
                "most_liked": most_liked_reviews,
                "most_disliked": most_disliked_reviews
            }