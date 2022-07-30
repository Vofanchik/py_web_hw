import asyncio

import more_itertools
import aiohttp
import requests as requests

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL = 'https://swapi.dev/api/people/'
CHUNK = 10

BaseModel = declarative_base()
engine = create_async_engine('sqlite+aiosqlite:///SW.db')


class StarWarsPerson(BaseModel):
    __tablename__ = 'sw'

    id = Column(Integer, nullable=False, unique=True,
                primary_key=True, autoincrement=True)
    birth_year = Column(Integer)
    eye_color = Column(String)
    films = Column(String)
    gender = Column(String)
    hair_color = Column(String)
    height = Column(Integer)
    homeworld = Column(String)
    mass = Column(Integer)
    name = Column(String)
    skin_color = Column(String)
    species = Column(String)
    starships = Column(String)
    vehicles = Column(String)


async def init_async_session(drop=False, create=False):
    async with engine.begin() as conn:
        if drop:
            await conn.run_sync(BaseModel.metadata.drop_all)
        if create:
            await conn.run_sync(BaseModel.metadata.create_all)
    async_session_maker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    return async_session_maker


async def get_person(index, session):
    async with session.get(f'{URL}{index}/') as response:
        json_data = await response.json()
        json_data.update({'id': index})
        return json_data


async def get_nested_info(url, session):
    async with session.get(url) as response:
        json_data = await response.json()
        return json_data.get('title') or json_data.get('name')


async def parse_response(response_json, session):
    [response_json.pop(field) for field in ['created', 'edited', 'url']
        if field in response_json]

    parsed_data = {}
    for k, v in response_json.items():
        if isinstance(v, list) and len(v) > 0 and v[0].startswith('http'):
            nested_data_coros = (get_nested_info(url, session) for url in v)
            result = await asyncio.gather(*nested_data_coros)
            parsed_data.update({k: ', '.join(result)})
        elif isinstance(v, str) and v.startswith('http'):
            result = await get_nested_info(v, session)
            parsed_data.update({k: result})
        else:
            parsed_data.update({k: v if v else '_'})
    return parsed_data


async def insert(session, *param):
    res = [await parse_response(person, session) for person in param]
    session = await init_async_session(False, False)
    async with session() as db:
        for pers_data in res:
            if 'detail' in pers_data:
                continue
            swp = StarWarsPerson(**pers_data)
            db.add(swp)
            await db.commit()


async def main():
    response_json = requests.get(URL).json()
    person_count = response_json['count']

    await init_async_session(True, True)

    async with aiohttp.ClientSession() as session:
        person_coros = (
            get_person(index, session) for index in range(1, person_count + 1)
        )

        for per in more_itertools.chunked(person_coros, CHUNK):
            result = await asyncio.gather(*per)
            await insert(session, *result)

if __name__ == '__main__':
    asyncio.run(main())
