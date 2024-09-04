import os
import pytest

from fastapi.testclient import TestClient
from app_factory import create_app

import httpx
from urllib.parse import urljoin

from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
import database

test_dbms = factories.postgresql_proc(port=None, dbname="test_db", user="ntuaflix")

@pytest.fixture(scope="session")
def db_sessionmaker(request, use_existing_dbms):
    if use_existing_dbms:
        DB_USERSNAME = os.getenv('DB_USERNAME')
        DB_PASSWORD = os.getenv('DB_PASSWORD')
        DB_HOST = os.getenv('DB_HOST')
        DB_DATABASE = os.getenv('DB_DATABASE')
        DATABASE_URL = f"postgresql://{DB_USERSNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"
        engine = create_engine(DATABASE_URL)
        models.Base.metadata.create_all(engine)
        yield sessionmaker(bind=engine)
        return

    test_dbms = request.getfixturevalue('test_dbms')

    pg_host = test_dbms.host
    pg_port = test_dbms.port
    pg_user = test_dbms.user
    pg_password = test_dbms.password
    pg_db = test_dbms.dbname
    
    with DatabaseJanitor(
        pg_user, pg_host, pg_port, pg_db, test_dbms.version, pg_password
    ):
        connection_str = f"postgresql+psycopg2://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
        engine = create_engine(connection_str)
        models.Base.metadata.create_all(engine)
        yield sessionmaker(bind=engine)

@pytest.fixture(scope="session")
def client(db_sessionmaker):
    def override_get_db():
        with db_sessionmaker() as test_db:
            yield test_db

    def factory(relative_url = None, **kwargs):
        app = create_app()
        app.dependency_overrides[database.get_db] = override_get_db
        res = TestClient(app, **kwargs)

        BASE_RELATIVE_URL = "ntuaflix_api/"
        if relative_url is not None:
            relative_url = urljoin(BASE_RELATIVE_URL, relative_url)
        else:
            relative_url = BASE_RELATIVE_URL
        base_url = urljoin(str(res.base_url), relative_url)
        
        res.base_url = httpx.URL(base_url)
        return res

    return factory

