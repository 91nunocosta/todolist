from unittest.mock import patch
import pytest


from todolist.run import app


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def db():
    with app.app_context():
        return app.data.driver.db


@pytest.fixture
def user():
    return "91nunocosta@gmail.com"


@pytest.fixture
def another_user():
    return "william.dev@example.com"


@pytest.fixture
def token(user):
    # the fixture is evaluated before each test who depend on it
    # then it is injected in the test (dependency injection)
    # in this case, after the test ends the context returns here
    # and continues after the yield expression

    # a patch for mocking the check_token function is started before the test
    # it is finished when the test stops
    token_payload = {"sub": user}

    patcher = patch("todolist.run.check_token", lambda _: token_payload)

    patcher.start()

    yield token_payload

    patcher.stop()