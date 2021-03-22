from typing import Any, Dict
from datetime import datetime

from unittest.mock import MagicMock, patch

import pytest

from freezegun import freeze_time

from todolist.auth.tokens import check_token, generate_token


FAKE_JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5MW51bm9jb3N0YUBnbWFpbC5jb20iLCJpYXQiOjE1MTYyMzkwMjJ9.UURXWQ_jcg5V8OmdeyA6quk7-9HMNntUmm4JWsiS-0U"
FAKE_SECRET = "fake_secret"


@freeze_time("2012-01-14 12:00:01")
def test_generate_token():
    username = "91nunocosta@gmail.com"

    jwt_encode_mock = MagicMock(return_value=FAKE_JWT_TOKEN)
    with patch("todolist.auth.tokens.encode", jwt_encode_mock):
        # the JWT secret is passed set by through an environment variable JWT_SECRET
        with patch.dict("os.environ", {"JWT_SECRET": FAKE_SECRET}):
            token = generate_token(username)

    assert token == FAKE_JWT_TOKEN

    expected_token_payload = {
        "sub": username,
        "iat": datetime(2012, 1, 14, 12, 0, 1),
    }

    jwt_encode_mock.assert_called_with(expected_token_payload, FAKE_SECRET)


def test_check_valid_token():
    expected_payload = {
        "sub": "91nunocosta@gmail.com",
        "iat": datetime(2012, 1, 14, 12, 0, 1),
    }

    jwt_decode_mock = MagicMock(return_value=expected_payload)
    with patch("todolist.auth.tokens.decode", jwt_decode_mock):
        # the JWT secret is passed set by through an environment variable JWT_SECRET
        with patch.dict("os.environ", {"JWT_SECRET": FAKE_SECRET}):
            payload = check_token(FAKE_JWT_TOKEN)

        assert payload == expected_payload

        jwt_decode_mock.assert_called_with(FAKE_JWT_TOKEN, FAKE_SECRET)


def test_check_empty_token():
    with pytest.raises(ValueError):
        check_token("")