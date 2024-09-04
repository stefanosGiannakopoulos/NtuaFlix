from .fixtures import *
import dotenv
dotenv.load_dotenv('.env')

def pytest_addoption(parser):
    parser.addoption(
            "--preload", action="store", default="yes",
            help="If no load files from .tsv (SLOW). If yes loads from preloaded test.sql. (yes/no)")
    parser.addoption(
            "--use-existing-dbms", action="store", default="no",
            help="If yes uses existing dbms from .env. If no starts a testing dbms. (yes/no)")


@pytest.fixture(scope="session")
def preload(pytestconfig):
    val = pytestconfig.getoption("--preload")
    assert val in ["yes", "no"]
    return val == "yes"


@pytest.fixture(scope="session")
def use_existing_dbms(pytestconfig):
    val = pytestconfig.getoption("--use-existing-dbms")
    assert val in ["yes", "no"]
    return val == "yes"

