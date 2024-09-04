from typer.testing import CliRunner
import pytest
import os
from ntuaflix_cli import app

from .config import *
from .utils import stdout_to_json

runner = CliRunner(mix_stderr=False)

def test_admin_login(login):
    pass

def test_health_check(login):
    result = runner.invoke(app, ["healthcheck"])
    assert result.exit_code == 0, result_exit_code
    assert not result.stderr, result.stderr

    result_json = stdout_to_json(result.stdout)

    assert result_json["status"] == "OK", result_json
    assert "dataconnection" in result_json, result_json
    assert isinstance(result_json["dataconnection"], str), result_json

@pytest.fixture
def resetall(login):
    result = runner.invoke(app, ["resetall"])
    assert result.exit_code == 0, result_exit_code
    assert not result.stderr, result.stderr

    result_json = stdout_to_json(result.stdout)

    assert result_json["status"] == "OK", result_json

def test_resetall(login, resetall):
    pass

def _upload_data_generic(command, fn):
    result = runner.invoke(app, [command, "--filename", fn])
    assert result.exit_code == 0, result_exit_code
    assert not result.stderr, result.stderr

    result_json = stdout_to_json(result.stdout)

    assert result_json["status"] == "OK", result_json

def test_upload(login, resetall):
    _upload_data_generic("newtitles",       "truncated_data/truncated_title.basics.tsv")
    _upload_data_generic("newakas",         "truncated_data/truncated_title.akas.tsv")
    _upload_data_generic("newnames",        "truncated_data/truncated_name.basics.tsv")
    _upload_data_generic("newcrew",         "truncated_data/truncated_title.crew.tsv")
    _upload_data_generic("newepisode",      "truncated_data/truncated_title.episode.tsv")
    _upload_data_generic("newprincipals",   "truncated_data/truncated_title.principals.tsv")
    _upload_data_generic("newratings",      "truncated_data/truncated_title.ratings.tsv")

def test_user(login):
    result = runner.invoke(app, ["user", "--username", ADMIN_USERNAME])
    assert result.exit_code == 0, result_exit_code
    assert not result.stderr, result.stderr

    assert "User found with following details" in result.stdout, result.stdout

    result_json = stdout_to_json(result.stdout)

    assert result_json["username"] == ADMIN_USERNAME

def test_adduser(login):
    result = runner.invoke(app, ["adduser", "--username", ADMIN_USERNAME, "--passw", "654321"])
    assert result.exit_code == 0, result.exit_code
    assert not result.stderr, result.stderr
    assert "User successfully created/modified" in result.stdout, result.stdout

    result = runner.invoke(app, ["logout"])
    assert result.exit_code == 0, result_exit_code
    assert not result.stderr, result.stderr
    assert "You have been successfully logged out" in result.stdout

    result = runner.invoke(app, ["login", "--username", ADMIN_USERNAME, "--passw", ADMIN_PASSWORD])
    assert result.exit_code == 0, result_exit_code
    assert not result.stderr, result.stderr
    assert "Unfortunately you were not authenticated (possibly due to wrong credentials)" in result.stdout

    result = runner.invoke(app, ["login", "--username", ADMIN_USERNAME, "--passw", "654321"])
    assert result.exit_code == 0, result_exit_code
    assert not result.stderr, result.stderr
    assert "You have been successfully authenticated" in result.stdout

    #CLEANUP

    result = runner.invoke(app, ["adduser", "--username", ADMIN_USERNAME, "--passw", ADMIN_PASSWORD])
    assert result.exit_code == 0, result_exit_code
    assert not result.stderr, result.stderr
    assert "User successfully created/modified" in result.stdout, result.stdout

    result = runner.invoke(app, ["logout"])
    assert result.exit_code == 0, result_exit_code
    assert not result.stderr, result.stderr
    assert "You have been successfully logged out" in result.stdout

    result = runner.invoke(app, ["login", "--username", ADMIN_USERNAME, "--passw", ADMIN_PASSWORD])
    assert result.exit_code == 0, result_exit_code
    assert not result.stderr, result.stderr
    assert "You have been successfully authenticated" in result.stdout

