import pytest
import pathlib
import json
import random
from .utils import json_compare

random.seed(42)

TITLE_SUBSTRING = "and"
with open(pathlib.Path(__file__).parent / "testdata/titles.json", "r") as f:
    TITLES = json.load(f)

TITLE_MINR      = "3"
TITLE_YRFROM    = "1991"
TITLE_YRTO      = "1992"
TITLE_GENRE     = "Comedy"
with open(pathlib.Path(__file__).parent / "testdata/titles_genre.json", "r") as f:
    TITLES_GENRE = json.load(f)


@pytest.mark.parametrize("title", random.sample(TITLES, 5))
def test_title(client, upload_data, title):
    response = client().get(f"title/{title['titleID']}")
    assert response.status_code == 200, response.text
    assert json_compare(response.json(), title)

def test_searchtitle(client, upload_data):
    response = client().request("GET", "searchtitle", json={"titlePart": TITLE_SUBSTRING})
    assert response.status_code == 200, response.text
    assert json_compare(response.json(), TITLES)

def test_bygenre(client, upload_data):
    response = client().request("GET", "bygenre", json={
        "qgenre": TITLE_GENRE,
        "minrating": TITLE_MINR,
        "yrFrom": TITLE_YRFROM,
        "yrTo": TITLE_YRTO,
        })
    assert response.status_code == 200, response.text
    assert json_compare(response.json(), TITLES_GENRE)

