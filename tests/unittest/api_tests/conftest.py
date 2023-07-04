import pytest

from server import app


@pytest.fixture(scope="session")
def client():
    test_client = app.test_client()
    yield test_client


@pytest.fixture()
def runner():
    return app.test_cli_runner()
