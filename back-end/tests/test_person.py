import pytest
import pathlib
import json
import random
from .utils import json_compare

random.seed(42)

PERSON_SUBSTRING = "da"
with open(pathlib.Path(__file__).parent / "testdata/people.json", "r") as f:
    PEOPLE = json.load(f)

@pytest.mark.parametrize("person", random.sample(PEOPLE, 5))
def test_name(client, upload_data, person):
    response = client().get(f"name/{person['nameID']}")
    assert response.status_code == 200, response.text
    assert json_compare(response.json(), person)

def test_searchtitle(client, upload_data):
    response = client().request("GET", "searchname", json={"namePart": PERSON_SUBSTRING})
    assert response.status_code == 200, response.text
    assert json_compare(response.json(), PEOPLE)

