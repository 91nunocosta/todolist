from todolist import __version__


def test_version():
    assert __version__ == "0.1.0"


def test_get_root(client):
    response = client.get("/")

    assert response.status_code == 200