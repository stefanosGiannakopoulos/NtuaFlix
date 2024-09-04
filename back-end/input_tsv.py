from sqlalchemy.orm import Session
import aiofiles
import asyncio
from database import get_db

from utils import parse_title_basics, parse_title_ratings, parse_title_principals,\
        parse_title_crew, parse_title_akas, parse_name_basics, parse_title_episode, resetall

import cProfile

async def main():
    db = next(get_db())

    resetall(db)

    async with aiofiles.open('truncated_data/truncated_title.basics.tsv', 'r', encoding='utf-8') as afp:
        await parse_title_basics(afp, db)

    async with aiofiles.open('truncated_data/truncated_title.ratings.tsv', 'r', encoding='utf-8') as afp:
        await parse_title_ratings(afp, db)

    async with aiofiles.open('truncated_data/truncated_title.akas.tsv', 'r', encoding='utf-8') as afp:
        await parse_title_akas(afp, db)

    async with aiofiles.open('truncated_data/truncated_name.basics.tsv', 'r', encoding='utf-8') as afp:
        await parse_name_basics(afp, db)

    async with aiofiles.open('truncated_data/truncated_title.crew.tsv', 'r', encoding='utf-8') as afp:
        await parse_title_crew(afp, db)

    async with aiofiles.open('truncated_data/truncated_title.episode.tsv', 'r', encoding='utf-8') as afp:
        await parse_title_episode(afp, db)

    async with aiofiles.open('truncated_data/truncated_title.principals.tsv', 'r', encoding='utf-8') as afp:
        await parse_title_principals(afp, db)
    
asyncio.run(main())
print("Data import complete.")
