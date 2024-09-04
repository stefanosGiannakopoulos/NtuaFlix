from typing import List
from sqlalchemy import create_engine, Sequence,Column, Integer, String, Date, Boolean, ForeignKey, Float, CHAR, REAL, Index, Table
from sqlalchemy import UniqueConstraint, CheckConstraint, DDL, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Mapped
import os
from datetime import datetime
from db_type import *

env_path = '.env'
load_dotenv(dotenv_path=env_path)

DB_USERSNAME = str(os.getenv('DB_USERNAME'))
DB_PASSWORD = str(os.getenv('DB_PASSWORD'))
DB_HOST = str(os.getenv('DB_HOST'))
DB_DATABASE = str(os.getenv('DB_DATABASE'))

DB_TYPE, DATABASE_URL = db_type_url(DB_USERSNAME, DB_PASSWORD, DB_HOST, DB_DATABASE)

#print(DATABASE_URL)
# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

Base = declarative_base()

# Define the User class
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=True)
    password = Column(String(500), nullable=False)
    dob = Column(Date, nullable=False)
    is_admin = Column(Boolean, default=False)

class Watchlist(Base):
    __tablename__ = 'watchlists'
    
    id = Column(Integer,Sequence('watchlist_id_seq'),primary_key=True, index=True)
    library_name = Column(String, nullable=False, index=True)
    # DIFFERENT
    if DB_TYPE == 'mysql': 
        library_name = Column(String(255), nullable=False, index=True)
    item_count = Column(Integer,nullable=False,default=0)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # DIFFERENT
    if DB_TYPE != 'mysql': 
        __table_args__ = (
            UniqueConstraint(library_name,user_id, name='unique_user_library'),
        )

# DIFFERENT   
if DB_TYPE == 'mysql': 
    Index('unique_user_library', Watchlist.library_name, Watchlist.user_id, unique=True)    
    
    
class WatchlistContent(Base):
    __tablename__ = 'watchlist_content'
    
    id = Column(Integer, Sequence('watchlist_content_id_seq'),primary_key=True, index=False)
    title_id = Column(CHAR(9),ForeignKey("title.tconst"))
    watchlist_id = Column(Integer, ForeignKey("watchlists.id"))
    
    if DB_TYPE != 'mysql': 
        __table_args__ = (
            UniqueConstraint(title_id,watchlist_id, name='movie_occurs_once'),
        )
    
#create different index here  
Index('watchlist_idx', WatchlistContent.watchlist_id)

#add triggers to handle insertions and deletions automatically 
#hmm or handle this in backend...?
trigger_ddl_insert = DDL("""
CREATE OR REPLACE FUNCTION inc_item_count()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE watchlists
    SET item_count = item_count + 1
    WHERE id = NEW.watchlist_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER inc_trigger
AFTER INSERT ON watchlist_content
FOR EACH ROW
EXECUTE FUNCTION inc_item_count();
""")
# DIFFERENT
if DB_TYPE == 'mysql':
    # Modify DDL triggers for MySQL syntax
    trigger_ddl_insert = DDL("""
CREATE TRIGGER inc_trigger
AFTER INSERT ON watchlist_content
FOR EACH ROW
BEGIN
    UPDATE watchlists
    SET item_count = item_count + 1
    WHERE id = NEW.watchlist_id;
END;
""")

event.listen(
    WatchlistContent.__table__,
    'after_create',
    trigger_ddl_insert
)

trigger_ddl_delete = DDL("""
CREATE OR REPLACE FUNCTION dec_item_count()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE watchlists
    SET item_count = item_count - 1
    WHERE id = OLD.watchlist_id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER dec_trigger
AFTER DELETE ON watchlist_content
FOR EACH ROW
EXECUTE FUNCTION dec_item_count();
""")

# DIFFERENT 
if DB_TYPE == 'mysql':
    trigger_ddl_delete = DDL("""
CREATE TRIGGER dec_trigger
AFTER DELETE ON watchlist_content
FOR EACH ROW
BEGIN
    UPDATE watchlists
    SET item_count = item_count - 1
    WHERE id = OLD.watchlist_id;
END;
""")

event.listen(
    WatchlistContent.__table__,
    'after_create',
    trigger_ddl_delete
)
class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, Sequence('review_id_seq'),primary_key=True, index=True)
    text = Column(String, nullable=True)
    # DIFFERENT
    if DB_TYPE == 'mysql':
        text = Column(String(255), nullable=True)
    stars = Column(Integer,nullable=False)
    date = Column(Date,default=datetime.utcnow)
    likes = Column(Integer,nullable=True)
    dislikes = Column(Integer, nullable=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    title_id = Column(CHAR(9), ForeignKey("title.tconst"))
    
    __table_args__ = (
        CheckConstraint('stars >= 1 AND stars <= 5', name='check_stars_range'),
    )
    
class ReviewReactions(Base):
    __tablename__ = 'reviews_reactions'
    
    id = Column(Integer, Sequence('review_reactions_id_seq'),primary_key=True, index=False)
    type = Column(Boolean, nullable=False) #like==1, dislike==0
    user_id = Column(Integer,ForeignKey("users.id"))
    review_id = Column(Integer, ForeignKey("reviews.id"))

#create triggers for likes and dislikes in Review -> is this really needed?

trigger_ddl_insert_like = DDL("""
CREATE OR REPLACE FUNCTION increment_like_count()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE reviews
    SET likes = likes + 1
    WHERE id = NEW.review_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER increment_like_trigger
AFTER INSERT ON reviews_reactions
FOR EACH ROW
WHEN (NEW.type = TRUE)
EXECUTE FUNCTION increment_like_count();
""")

trigger_ddl_insert_dislike = DDL("""
CREATE OR REPLACE FUNCTION increment_dislike_count()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE reviews
    SET dislikes = dislikes + 1
    WHERE id = NEW.review_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER increment_dislike_trigger
AFTER INSERT ON reviews_reactions
FOR EACH ROW
WHEN (NEW.type = FALSE)
EXECUTE FUNCTION increment_dislike_count();
""")

# Attach triggers 
event.listen(ReviewReactions.__table__, 'after_create', trigger_ddl_insert_like)
event.listen(ReviewReactions.__table__, 'after_create', trigger_ddl_insert_dislike)


table_person_known_for_titles = Table(
        "person_known_for_titles",
        Base.metadata,
        Column("tconst", ForeignKey("title.tconst"), primary_key=True),
        Column("nconst", ForeignKey("person.nconst"), primary_key=True),
        )

table_title_director = Table(
        "title_director",
        Base.metadata,
        Column("tconst", ForeignKey("title.tconst"), primary_key=True),
        Column("nconst", ForeignKey("person.nconst"), primary_key=True),
        )

table_title_writer = Table(
        "title_writer",
        Base.metadata,
        Column("tconst", ForeignKey("title.tconst"), primary_key=True),
        Column("nconst", ForeignKey("person.nconst"), primary_key=True),
        )

table_title_genre = Table(
        "title_genre",
        Base.metadata,
        Column("genre", ForeignKey("genre.id"), primary_key=True),
        Column("tconst", ForeignKey("title.tconst"), primary_key=True),
        )



# Creating the tables and the indexes ...
class Title(Base):
    __tablename__ = 'title'
    
    tconst = Column(CHAR(9), primary_key=True)
    end_year = Column(Integer)
    primary_title = Column(String(100), nullable=False)
    original_title = Column(String(100), nullable=False)
    title_type = Column(String(10), nullable=False)
    runtime_minutes = Column(Integer, nullable=True)
    start_year = Column(Integer, nullable=False)
    is_adult = Column(Boolean, nullable=False)
    image_url = Column(String(100))
    principals = Column(Integer, nullable=False)
    average_rating = Column(Float)
    num_votes = Column(Integer)

    known_for_by: Mapped[List['Person']] = relationship(secondary=table_person_known_for_titles, back_populates="known_for_titles")
    principals: Mapped[List['Principals']] = relationship(back_populates="title")
    directors: Mapped[List['Person']] = relationship(secondary=table_title_director, back_populates="titles_as_director")
    writers: Mapped[List['Person']] = relationship(secondary=table_title_writer, back_populates="titles_as_writer")
    aliases: Mapped[List['TitleAlias']] = relationship(back_populates="title")
    genres: Mapped[List['Genre']] = relationship(secondary=table_title_genre, back_populates="titles")

    episodes: Mapped[List['TitleEpisode']] = relationship(back_populates="parent", foreign_keys="TitleEpisode.parent_tconst")

# Add the index
Index('idx_title_type', Title.title_type)

class TitleEpisode(Base):
    __tablename__ = 'title_episode'
    
    episode_tconst = Column(CHAR(9), ForeignKey('title.tconst'), primary_key=True)
    episode: Mapped['Title'] = relationship(foreign_keys=[episode_tconst])

    parent_tconst = Column(CHAR(9), ForeignKey('title.tconst'), nullable=False)
    parent: Mapped['Title'] = relationship(foreign_keys=[parent_tconst], back_populates="episodes")
    
    season_number = Column(Integer)
    episode_number = Column(Integer)

# Add the title_episode index
Index('idx_parent_tconst',TitleEpisode.parent_tconst) 

class TitleAlias(Base):
    __tablename__ = 'title_alias'
    
    id = Column(Integer, primary_key=True)
    tconst = Column(CHAR(9), ForeignKey('title.tconst'), nullable=False)
    title: Mapped['Title'] = relationship(back_populates="aliases")
    
    title_name = Column(String(255), nullable=False)
    ordering = Column(Integer, nullable=False)
    region = Column(String(10), nullable=True)
    language = Column(String(10), nullable=True)
    types = Column(String(255))
    attributes = Column(String(255))
    is_original_title = Column(Boolean, nullable=False)

# Index for tilte_alias
Index('idx_tconst_alias', TitleAlias.tconst)


class Genre(Base):
    __tablename__ = 'genre'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    titles: Mapped[List['Title']] = relationship(secondary=table_title_genre, back_populates="genres")



table_person_profession = Table(
        "person_profession",
        Base.metadata,
        Column("profession", ForeignKey("profession.id"), primary_key=True),
        Column("nconst", ForeignKey("person.nconst"), primary_key=True),
        )


class Person(Base):
    __tablename__ = 'person'
    
    nconst = Column(String(10), primary_key=True)
    image_url = Column(String(255))
    primary_name = Column(String(100), nullable=False)
    birth_year = Column(Integer)
    death_year = Column(Integer)

    primary_professions: Mapped[List['Profession']] = relationship(secondary=table_person_profession, back_populates="people")
    known_for_titles: Mapped[List['Title']] = relationship(secondary=table_person_known_for_titles, back_populates="known_for_by")

    image_url = Column(String(100))

    titles_as_principal: Mapped[List['Principals']] = relationship(back_populates="person")

    titles_as_director: Mapped[List['Title']] = relationship(secondary=table_title_director, back_populates="directors")
    titles_as_writer: Mapped[List['Title']] = relationship(secondary=table_title_writer, back_populates="writers")



class Profession(Base):
    __tablename__ = 'profession'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True, nullable=False)
    people: Mapped[List['Person']] = relationship(secondary=table_person_profession, back_populates="primary_professions")


class Principals(Base):
    __tablename__ = 'principals'
    
    id = Column(Integer, primary_key=True)
    tconst = Column(CHAR(9), ForeignKey('title.tconst'), nullable=False)
    title: Mapped['Title'] = relationship(back_populates="principals")
    nconst = Column(String(10), ForeignKey('person.nconst'), nullable=False)
    person: Mapped['Person'] = relationship(back_populates="titles_as_principal")
    
    category_id = Column(Integer, ForeignKey('profession.id'), nullable=False)
    category: Mapped['Profession'] = relationship(foreign_keys=[category_id])

    job_id = Column(Integer, ForeignKey('profession.id'))
    job: Mapped['Profession'] = relationship(foreign_keys=[job_id])

    ordering = Column(Integer)
    characters = Column(String(255))
    image_url = Column(String(255))

# Indexes for principals
Index('idx_tconst_principals', Principals.tconst)
Index('idx_nconst_principals', Principals.nconst)
Index('idx_category_id_principals', Principals.category_id)
Index('idx_job_id_principals', Principals.job_id)

Base.metadata.create_all(engine)