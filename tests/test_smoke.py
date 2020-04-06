import pytest

import lep_web


@pytest.fixture
def client():
    with lep_web.app.test_client() as client:
        yield client


def test_smoke(client):
    assert '<a href="https://elpais.com/' in client.get("/").data.decode("utf-8")
