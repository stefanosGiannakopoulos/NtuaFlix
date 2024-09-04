from typer.testing import CliRunner
import pytest
import pathlib
import json
import random
from ntuaflix_cli import app
from .config import *
from .utils import json_compare2

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

runner = CliRunner(mix_stderr=False)

@pytest.mark.parametrize("title", random.sample(TITLES, 5))
def test_title(login, title):
    result = runner.invoke(app, ['title', '--titleID', title['titleID']])
    assert result.exit_code == 0, result.exit_code
    assert not result.stderr
    assert json_compare2(result.stdout, title)

def test_searchtitle(login):
    result = runner.invoke(app, ["searchtitle", '--titlepart', TITLE_SUBSTRING])
    assert result.exit_code == 0, result.exit_code
    assert not result.stderr
    assert json_compare2(result.stdout, TITLES)

def test_bygenre(login):
    result = runner.invoke(app, ["bygenre",
        "--genre", TITLE_GENRE,
        "--min", TITLE_MINR,
        "--from", TITLE_YRFROM,
        "--to", TITLE_YRTO,
        ])
    assert result.exit_code == 0, result.exit_code
    assert not result.stderr
    assert json_compare2(result.stdout, TITLES_GENRE)

