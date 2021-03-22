from unittest.mock import patch, MagicMock

from todolist.run import replace_password_with_hash


def test_hash_password():
    password = "unsecurepassword"
    account = {"username": "91nunocosta@gmail.com", "password": password}

    fake_hash = "fake_hash"

    password_hash_mock = MagicMock(return_value=fake_hash)

    with patch("todolist.run.password_hash", password_hash_mock):
        replace_password_with_hash([account])

    password_hash_mock.assert_called_with(password)

    assert account["password"] == fake_hash
