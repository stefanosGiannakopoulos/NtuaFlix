import os
import pathlib
import pytest

@pytest.fixture(scope="session")
def resetall(admin_client):
    response = admin_client().post("resetall/")
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload.keys() == {"status"}, payload
    assert payload["status"] == "OK", payload

def _upload_data_generic(admin_client, endpoint, fn):
    with open(fn, "rb") as f:
        files = {'file': (os.path.basename(f.name), f, 'text/tab-separated-values')}
        response = admin_client().post(f"upload/{endpoint}", files=files)
        assert response.status_code == 200, response.text
        payload = response.json()
        assert payload["status"] == "OK", payload

import urllib
import subprocess


@pytest.fixture(scope="session")
def upload_data(admin_client, db_sessionmaker, preload):
    if preload:
        with db_sessionmaker() as test_db:
            sql_fn = pathlib.Path(__file__).parent.parent / "testdata/test.sql"
            parsed = urllib.parse.urlparse(str(test_db.bind.url))
            cmd = ['psql', '-h', parsed.hostname, *(['-p', str(parsed.port)] if parsed.port is not None else []),
                    '-d', parsed.path.lstrip('/'), '-U', parsed.username,
                    '-f', str(sql_fn)]
            env = {}
            print(parsed.password)
            if os.getenv('DB_PASSWORD') is not None: env['PGPASSWORD'] = os.getenv('DB_PASSWORD') #ONLY IF USING EXISTING DBMS
            subprocess.run(cmd, check=True, env=env) #, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        _upload_data_generic(admin_client, "titlebasics", "truncated_data/truncated_title.basics.tsv")
        _upload_data_generic(admin_client, "titleakas", "truncated_data/truncated_title.akas.tsv")
        _upload_data_generic(admin_client, "namebasics", "truncated_data/truncated_name.basics.tsv")
        _upload_data_generic(admin_client, "titlecrew", "truncated_data/truncated_title.crew.tsv")
        _upload_data_generic(admin_client, "titleepisode", "truncated_data/truncated_title.episode.tsv")
        _upload_data_generic(admin_client, "titleprincipals", "truncated_data/truncated_title.principals.tsv")
        _upload_data_generic(admin_client, "titleratings", "truncated_data/truncated_title.ratings.tsv")

