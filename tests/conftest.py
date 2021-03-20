import pytest

from todolist.run import app

@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def db():
    with app.app_context():
        return app.data.driver.db
