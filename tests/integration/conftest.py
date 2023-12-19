import pytest
from starlette.testclient import TestClient

from pdf_service.main import app


@pytest.fixture(scope="module")
def test_app():
    # need to run inside 'with' so startup and shutdown event registers
    with TestClient(app) as client:
        yield client

