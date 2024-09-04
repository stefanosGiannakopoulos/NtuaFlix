from typer.testing import CliRunner
import pytest
import pathlib
import json
import random
from ntuaflix_cli import app
from .config import *
from .utils import json_compare2

random.seed(42)

PERSON_SUBSTRING = "da"
with open(pathlib.Path(__file__).parent / "testdata/people.json", "r") as f:
    PEOPLE = json.load(f)

runner = CliRunner(mix_stderr=False)

@pytest.mark.parametrize("person", random.sample(PEOPLE, 5))
def test_title(login, person):
    result = runner.invoke(app, ['name', '--nameid', person['nameID']])
    assert result.exit_code == 0, result.exit_code
    assert not result.stderr
    assert json_compare2(result.stdout, person), (result.stdout, person)

def test_searchname(login):
    result = runner.invoke(app, ["searchname", '--namepart', PERSON_SUBSTRING])
    assert result.exit_code == 0, result.exit_code
    assert not result.stderr
    assert json_compare2(result.stdout, PEOPLE), result.stdout


