import pytest
from typer.testing import CliRunner
from ntuaflix_cli import app
from .config import *


runner = CliRunner(mix_stderr=False)

@pytest.fixture
def login():
    result = runner.invoke(app, [
        'login',
        '--username', ADMIN_USERNAME,
        '--passw', ADMIN_PASSWORD,
        ])
    assert result.exit_code == 0, result.exit_code
    assert not result.stderr 
    assert "You have been successfully authenticated" in result.stdout

    yield
    
    result = runner.invoke(app, ['logout'])
    assert result.exit_code == 0, result.exit_code
    assert not result.stderr 
    assert "You have been successfully logged out" in result.stdout

