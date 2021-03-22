from datetime import datetime

from unittest.mock import patch

from freezegun import freeze_time

from todolist.auth.tokens import check_token, generate_token


FAKE_JWT_SECRET = "fake_secret"


@freeze_time("2021-03-22 15:30:00")
def test_generate_and_check_token():

    username = "91nunocosta@gmail.com"

    # the JWT secret is set in the environment variable JWT_SECRET
    with patch.dict("os.environ", {"JWT_SECRET": FAKE_JWT_SECRET}):
        token = generate_token(username)

        payload = check_token(token)

    assert payload == {
        "sub": username,
        "iat": datetime(2021, 3, 22, 15, 30, 0, 0).timestamp(),
    }