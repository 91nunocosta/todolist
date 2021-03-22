from unittest.mock import patch


def test_non_existing_account_login(db, client):
    db.accounts.drop()

    data = {"username": "91nunocosta@gmail.com", "password": "notsecurepassword"}

    response = client.post("login/", json=data)

    assert response.status_code == 401


def test_invalid_password_login(db, client):
    db.accounts.drop()

    data = {"username": "91nunocosta@gmail.com", "password": "notsecurepassword"}

    db.accounts.insert_one(dict(data))

    with patch("todolist.login.check_password", lambda _a, _b: False):
        response = client.post("login/", json=data)

    assert response.status_code == 401


def test_valid_login(db, client):
    db.accounts.drop()

    data = {"username": "91nunocosta@gmail.com", "password": "notsecurepassword"}

    db.accounts.insert_one(dict(data))

    fake_token = "this_is_a_fake_token"

    with patch("todolist.login.generate_token", lambda _: fake_token):
        with patch("todolist.login.check_password", lambda _a, _b: True):
            response = client.post("login/", json=data)

    assert response.status_code == 200

    data = response.json
    assert data["token"] == fake_token
