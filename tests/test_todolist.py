import pytest

from todolist import __version__

from todolist.run import app

def test_version():
    assert __version__ == '0.1.0'


@pytest.fixture
def client():
    return app.test_client()

def test_get_root(client):
    response = client.get('/')

    assert response.status_code == 200
